import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    BAND = 2.0
    TOL = 1e-12

    def get_component(df, cid, field="last_history_value"):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].tolist():
                val = np.nan
                try:
                    if isinstance(v, dict) and cid in v and isinstance(v[cid], dict):
                        x = v[cid].get(field, np.nan)
                        val = float(x) if x is not None else np.nan
                except Exception:
                    val = np.nan
                out.append(val)
            return pd.Series(out, dtype=float)
        return pd.Series(np.nan, index=range(len(df)), dtype=float)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rmax = close.rolling(H, min_periods=H).max()
            at_high = close >= rmax * (1 - 1e-9)
            computable_high = rmax.notna()
            sr = get_component(df, "scaled_rise")
            ret7 = close / close.shift(H) - 1
            rise = pd.Series(np.where(sr.notna(), sr > 0, ret7 > 0), index=df.index)
            rise_comp = sr.notna() | ret7.notna()
            active = fc.abs() > TOL
            usable = active & computable_high & rise_comp
            n_active += int(usable.sum())
            n_agree += int((usable & at_high & rise & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    main_name = "mean unusual 7-bar move per long case (day-pooled)"
    thr = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of active bars are long bars where the close is at its 7-bar closing high "
                           "with a positive 7-bar rise, as the plan's situation requires."),
            "reading": ("Active bars whose 7-bar high or 7-bar rise cannot be computed inside the window are left out "
                        "of the agreement share."),
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        # normal drift: non-overlapping 7-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            base = 0.0
            bets = []
            for i in range(len(fc)):
                f = fc[i]
                if f <= TOL:
                    base = 0.0
                    continue
                if f - base >= BAND - 1e-12:
                    bets.append(i)
                    base = f
                else:
                    base = min(base, f)
            seen_cells = set()
            for i in bets:
                cell = i // H
                if cell in seen_cells:
                    continue
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1
                if not np.isfinite(r):
                    continue
                seen_cells.add(cell)
                cases.append((ts.iloc[i].strftime("%Y-%m-%d"), r - drift, fc[i]))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct case days": n_days}

    mean_u = None
    t_main = None
    if n_cases > 0:
        x = np.array([u for _, u, _ in cases])
        mean_u = float(x.mean())
        if n_days >= 2:
            dev = pd.Series(x - mean_u).groupby([d for d, _, _ in cases]).sum().to_numpy()
            var_mean = (dev ** 2).sum() * n_days / (n_days - 1) / n_cases ** 2
            if var_mean > 0:
                t_main = float(mean_u / np.sqrt(var_mean))

    diff = None
    t_sup = None
    sup_pass = None
    if n_cases >= 4:
        f = np.array([fv for _, _, fv in cases])
        u = np.array([uv for _, uv, _ in cases])
        med = np.median(f)
        up = u[f > med]
        lo = u[f <= med]
        if len(up) >= 2 and len(lo) >= 2:
            diff = float(up.mean() - lo.mean())
            tt = stats.ttest_ind(up, lo, equal_var=False).statistic
            t_sup = float(tt) if np.isfinite(tt) else None
            sup_pass = bool(t_sup is not None and t_sup >= 1 and diff > 0)
        else:
            sup_pass = False

    reading = ("A case is the first long bet (forecast rise of >= 2 points from its lowest level since the last bet, "
               "from 0 after a flat) in each 7-bar grid cell of a window with a full 7-bar forward return; the halves "
               "split at the median case forecast (above vs at-or-below); the plan's minimum of 30 distinct case days "
               "is applied as 'not observable'; active bars without a computable 7-bar high or rise are left out of "
               "the agreement share.")

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days over all coins and windows ({n_days})."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t could not be computed, so the t is not outside -2..2."
    elif t_main >= 2 and mean_u > 0:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and upper-minus-lower half difference with Welch t >= 1."
        else:
            status = "inconclusive"
            decided = "Main t >= 2 but the supporting check (upper minus lower half, Welch t >= 1) failed."
    elif t_main <= -2 and mean_u < 0:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2: a giveback after scaled weekly rises at the high."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_main}
                          if t_main is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "unusual move upper half minus lower half of forecast (Welch t >= 1)",
            "value": diff,
            "passed": sup_pass,
            "welch_t": t_sup,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

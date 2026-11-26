import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    BAND = 2.0
    MIN_DAYS = 30
    COMP = "scaled_rise"

    def comp_series(df, comp_id, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (comp_id, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(comp_id)
                    if isinstance(c, dict) and c.get(field) is not None:
                        try:
                            val = float(c.get(field))
                        except Exception:
                            val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def recompute_rise(close):
        r7 = close / close.shift(7) - 1.0
        base = r7.abs().rolling(30, min_periods=30).mean()
        v = r7 / base
        return v.where(base > 0)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = comp_series(df, COMP)
            raw = raw.where(raw.notna(), recompute_rise(close))
            regime = df["regime"].astype(str).str.lower()
            active = fc != 0
            situation = (regime == "trending") & (raw >= 1.0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean 14-bar unusual move of the long cases (return minus the coin's normal 14-bar drift)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of the 14-bar unusual move on the forecast at the signal bar"
    reading_base = ("The choppy calm profile is read from the recorded regime ('trending' only when the detector's "
                    "trend and swing vetoes did not fire, since its components are not recorded and its 365-bar "
                    "lookback is not in the record) and the rise from scaled_rise's last_history_value >= 1 "
                    "(recomputed from prices where missing); a case is the first long bet of each 14-bar grid cell "
                    "counted from each window's first row, with a 14-bar return inside the window; the day-clustered "
                    "standard error is sqrt(sum of squared per-day sums of deviations)/n without small-sample correction.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"cases": 0, "cases on distinct days": 0},
            "decided_by": "The forecast is never active, so there are fewer than 30 cases on distinct days.",
            "reading": reading_base,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Only %.1f%% of active bars are long bars in the choppy calm regime with a scaled 7-day "
                           "rise of at least 1 usual swing, under the 90%% required." % (100 * agreement)),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean non-overlapping 14-bar return over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            # long bets
            low = 0.0
            bet = np.zeros(len(fc), dtype=bool)
            for i, f in enumerate(fc):
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND - 1e-12:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            seen_cells = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= len(c):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                u = (c[i + H] / c[i] - 1.0) - d
                cases.append((ts.iloc[i].floor("D"), float(u), float(fc[i])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)

    mean_u = None
    t = None
    slope = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        f = np.array([x[2] for x in cases])
        dkeys = [x[0] for x in cases]
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(pd.Series(dkeys)).sum().values
        se = np.sqrt(np.sum(dev ** 2)) / n_cases
        t = float(mean_u / se) if se > 0 else None
        if n_cases >= 2 and np.var(f) > 0:
            slope = float(np.sum((f - f.mean()) * (u - mean_u)) / np.sum((f - f.mean()) ** 2))

    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 cases on distinct days (%d), the minimum needed for any verdict." % n_days
    elif t is not None and mean_u > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the supporting slope is above 0."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is not positive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t is None else {"name": "t of the mean, cases of one day taken together", "value": t},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": {"cases": int(n_cases), "cases on distinct days": int(n_days)},
        "decided_by": decided,
        "reading": reading_base,
    }

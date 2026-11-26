import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    PROFILE_PERIOD = 60
    PROFILE_LEVEL = -10.0  # percent change over 60 bars; veto (chop) when >= -10
    RAW = "debug_info.components.scaled_rise.last_history_value"
    POST = "debug_info.components.scaled_rise.post_pipeline_value"

    def to_dt(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            # falling market: 60-bar price evolution (percent) below -10, recomputed from prices
            evo = (close / close.shift(PROFILE_PERIOD) - 1.0) * 100.0
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            falling = pd.Series(np.where(evo.notna(), evo < PROFILE_LEVEL, reg == "unknown"), index=df.index)
            # up day: raw scaled return > 0 where recorded, else the bar's close-to-close return
            px_ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                up = pd.Series(np.where(raw.notna(), raw > 0, px_ret > 0), index=df.index)
            else:
                up = px_ret > 0
            active = fc.notna() & (fc != 0)
            ok = active & falling.astype(bool) & up.astype(bool) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading_base = ("The falling market is the 60-bar close change (in percent) below -10, recomputed from prices, "
                    "falling back to the recorded regime ('unknown' = not vetoed) on a window's first 60 bars; "
                    "an up day is a positive raw scaled return; the plan's 'fewer than 30 case days' is treated as "
                    "a minimum count (not observable); the per-day t uses deviations from the mean summed per day "
                    "(cluster standard error with D/(D-1)); the slope t is the ordinary OLS t.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are falling-market up days with a "
                           "short forecast, so the config does not short exactly the plan's situation."
                           if n_active > 0 else "The record has no active bar, so the situation cannot be matched."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, day, fwd_ret, drift, post)
    for coin, wins in bars.items():
        # coin's normal 3-bar drift over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            ts = to_dt(df["timestamp"])
            post = pd.to_numeric(df[POST], errors="coerce").values if POST in df.columns else np.full(len(df), np.nan)

            # bets on the short side: rise of -forecast by >= band from its lowest level since last bet
            ref = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                s = -fc[i] if fc[i] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = s
                else:
                    ref = min(ref, s)

            seen_cells = set()
            for i in range(len(df)):
                if not bet[i]:
                    continue
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= len(df):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                day = ts.iloc[i].floor("D")
                case_rows.append((coin, day, r, drift, post[i]))

    n_cases = len(case_rows)
    if n_cases > 0:
        cdf = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "drift", "post"])
        cdf["adj"] = cdf["ret"] - cdf["drift"]
        cdf["unusual_short"] = -cdf["adj"]
        n_days = int(cdf["day"].nunique())
    else:
        cdf = None
        n_days = 0

    mean_u = None
    t_main = None
    if n_cases > 0:
        x = cdf["unusual_short"].values
        mean_u = float(np.mean(x))
        dev = pd.Series(x - mean_u).groupby(cdf["day"].values).sum().values
        D = len(dev)
        if D >= 2:
            var = np.sum(dev ** 2) * D / (D - 1)
            se = np.sqrt(var) / n_cases
            t_main = float(mean_u / se) if se > 0 else None

    slope = None
    t_slope = None
    if n_cases > 0:
        sub = cdf[np.isfinite(cdf["post"].values) & np.isfinite(cdf["adj"].values)]
        if len(sub) >= 3:
            xs = np.abs(sub["post"].values.astype(float))
            ys = sub["adj"].values.astype(float)
            if np.std(xs) > 0:
                lr = stats.linregress(xs, ys)
                slope = float(lr.slope)
                t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    slope_pass = None if t_slope is None else bool(slope < 0 and t_slope <= -2)

    main = {
        "name": "mean unusual 3-bar move after cases, short direction",
        "value": mean_u,
        "statistic": None if t_main is None else {"name": "t of the mean, cases of one day summed", "value": t_main},
        "threshold": "confirm: mean > 0 with t >= 2 (and slope t <= -2); reject: mean < 0 with t <= -2",
    }
    support = {"name": "slope of drift-adjusted 3-bar return on |post_pipeline_value| (t)",
               "value": t_slope, "passed": slope_pass}
    counts = {"distinct case days": int(n_days), "cases": int(n_cases)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days across all coins and windows, below the plan's minimum of 30."
    elif t_main is None or mean_u is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_main >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean unusual move in the short direction is above 0 with t >= 2 and the size slope has t <= -2."
        else:
            status = "inconclusive"
            decided = "The main t is >= 2 but the size slope's t is above -2 (or not computable), which the plan calls inconclusive."
    elif mean_u < 0 and t_main <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction is below 0 with t <= -2: falling-market up days were followed by further rises beyond drift."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"
    PPV = "debug_info.components.range_pos.post_pipeline_value"

    # ---------- 1. situation check ----------
    # Fidelity: graded position of the close in its 20-close range; long high in the range, short low.
    # Expected side = sign of (2*pos - 1), i.e. sign of the raw component value.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            hi = close.rolling(20, min_periods=20).max()
            lo = close.rolling(20, min_periods=20).min()
            rng = hi - lo
            pos = (close - lo) / rng.replace(0, np.nan)
            recomputed = (2 * pos - 1) * 20
            if RAW in df.columns:
                raw = df[RAW].astype(float).where(df[RAW].notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            exp_side = np.sign(raw)
            agree = active & raw.notna() & (exp_side != 0) & (np.sign(fc) == exp_side)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of drift-removed 5-bar forward return on post_pipeline_value, grid cases pooled"
    threshold = "confirm: slope > 0 with t >= 2 and top-minus-bottom fifth > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "The forecast's sign does not follow the sign of the close's position around the middle "
                          "of its 20-close range on at least 90% of active bars (long high, short low).",
            "reading": "Expected side taken as the sign of the raw range-position value (recomputed from closes where missing).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            ppv = df[PPV].astype(float).values if PPV in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, ppv[i]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "f"])
    # coin's mean 5-bar return over all windows (non-overlapping grid)
    if len(g):
        drift = g.groupby("coin")["ret"].transform("mean")
        g["ex"] = g["ret"] - drift
    else:
        g["ex"] = []
    g = g.dropna(subset=["ex", "f"])
    n_cases = int(len(g))

    slope = t = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3 and g["f"].nunique() > 1:
        lr = stats.linregress(g["f"].values, g["ex"].values)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else (0.0)
    n_top = n_bot = 0
    if n_cases > 0:
        q80 = g["f"].quantile(0.8)
        q20 = g["f"].quantile(0.2)
        top = g.loc[g["f"] >= q80, "ex"]
        bot = g.loc[g["f"] <= q20, "ex"]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top and n_bot:
            sup_val = float(top.mean() - bot.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"grid cases across the coins": n_cases, "top fifth cases": n_top, "bottom fifth cases": n_bot}

    if n_cases < 500 or slope is None:
        status = "not observable"
        decided = f"Only {n_cases} grid cases across the coins, fewer than the 500 the plan requires."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-minus-bottom fifth difference is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "A confirming slope (t >= 2) whose supporting check (top minus bottom fifth > 0) fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS t of slope", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean drift-removed 5-bar return, top fifth minus bottom fifth of forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid = rows 0,5,10,... of each window with close[t+5] in the same window; drift = coin's mean grid "
                   "5-bar return over all windows; fifths = pooled 20th/80th percentiles of post_pipeline_value "
                   "(inclusive); fewer than 500 grid cases is reported as not observable.",
    }

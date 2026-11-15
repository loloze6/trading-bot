import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    FC = "forecast"

    # ---------- 1. Situation check: r60 > 0 and r20 > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            r60 = close / close.shift(60) - 1.0
            r20 = close / close.shift(20) - 1.0
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            reg_ok = reg.str.lower().eq("trending")
            price_known = r60.notna() & r20.notna()
            price_ok = (r60 > 0) & (r20 > 0)
            # Where both returns can be computed from the window's prices, require them;
            # always require the detector's own label.
            situ = reg_ok & (~price_known | price_ok)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "pooled mean 20-bar forward excess return over the coin's mean 20-bar return, active bars, non-overlapping"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 non-overlapping active blocks"
    reading_base = ("Situation checked on the regime label 'trending' plus both 60- and 20-bar close returns > 0 where "
                    "computable inside the window, long side = forecast > 0; the coin's mean 20-bar return and the "
                    "active samples use the same non-overlapping grid (positions 0, 20, 40, ... of each window), "
                    "an active block is a grid bar with forecast > 0 and a full 20-bar forward return, and the "
                    "supporting slope is an OLS of excess return on forecast over those same blocks.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with non-zero forecast are long bars where both the 60-bar and "
                           "20-bar returns are positive (regime 'trending'), so the config does not trade the plan's situation."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    samples = []  # (coin, fwd, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                samples.append((coin, c1 / c0 - 1.0, fc[p]))

    s = pd.DataFrame(samples, columns=["coin", "fwd", "fc"])
    if len(s):
        coin_mean = s.groupby("coin")["fwd"].mean()
        s["excess"] = s["fwd"] - s["coin"].map(coin_mean)
        act = s[np.isfinite(s["fc"]) & (s["fc"] > 0)].copy()
    else:
        act = pd.DataFrame(columns=["coin", "fwd", "fc", "excess"])

    n_blocks = int(len(act))
    counts = {"non-overlapping 20-bar active blocks pooled across coins and windows": n_blocks}

    mean_ex = float(act["excess"].mean()) if n_blocks > 0 else None
    t_val = None
    if n_blocks >= 2:
        sd = float(act["excess"].std(ddof=1))
        if sd > 0:
            t_val = mean_ex / (sd / np.sqrt(n_blocks))

    slope = None
    if n_blocks >= 3 and act["fc"].nunique() > 1:
        lr = stats.linregress(act["fc"].astype(float).values, act["excess"].astype(float).values)
        slope = float(lr.slope)
    sup_passed = None if slope is None else bool(slope > 0)

    if n_blocks < 30:
        status = "not observable"
        decided = f"Only {n_blocks} non-overlapping 20-bar active blocks, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), which meets neither confirm nor reject."
    elif mean_ex > 0 and t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean 20-bar excess return on active bars is above 0 with t >= 2, and the slope on forecast is positive."
        else:
            status = "inconclusive"
            decided = "Mean excess is above 0 with t >= 2, but the supporting slope on forecast is not positive."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean 20-bar excess return on active bars is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": float(t_val)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of 20-bar excess return on forecast level, active non-overlapping blocks",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }

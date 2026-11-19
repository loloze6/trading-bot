import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    COMP = "debug_info.components.jump_share.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            past_ret = close / close.shift(H) - 1.0  # inside the window only
            active = fc.notna() & (fc != 0)
            computable = past_ret.notna()
            mask = active & computable
            n_active += int(mask.sum())
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce").reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=close.index)
            situation = (past_ret < 0) & (raw > 0)
            n_agree += int((mask & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("The situation is taken as a 72-bar close-to-close fall inside the window with a positive "
               "raw top-3-losses share, on the long side, and active bars within a window's first 72 rows "
               "(where the fall cannot be recomputed) are left out of the check; the coin's mean 72-bar "
               "return is the mean over all its grid bars in all windows, the regression is pooled OLS of "
               "excess return on forecast with its ordinary t, and terciles are equal-count thirds of the "
               "fallen cases ranked by forecast (ties broken by order).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars where the coin is down over 72 bars "
                           "with a long forecast, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i], reg[i]))

    grid = pd.DataFrame(rows, columns=["coin", "fwd", "forecast", "regime"])
    if len(grid) > 0:
        coin_mean = grid.groupby("coin")["fwd"].mean()
        grid["excess"] = grid["fwd"] - grid["coin"].map(coin_mean)
        fallen = grid[(grid["regime"] == "mean_reversion")].dropna(subset=["excess", "forecast"])
    else:
        fallen = pd.DataFrame(columns=["coin", "fwd", "forecast", "regime", "excess"])

    n_cases = int(len(fallen))
    counts = {"fallen grid cases": n_cases}

    slope = None
    t = None
    top_mean = None
    if n_cases >= 3 and fallen["forecast"].nunique() > 1:
        x = fallen["forecast"].astype(float).to_numpy()
        y = fallen["excess"].astype(float).to_numpy()
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cases >= 3:
        ranks = fallen["forecast"].rank(method="first")
        terc = pd.qcut(ranks, 3, labels=False)
        top = fallen.loc[terc == 2, "excess"]
        if len(top) > 0:
            top_mean = float(top.mean())
        counts["top tercile cases"] = int(len(top))

    main = {
        "name": "pooled slope of 72-bar excess return on forecast (fallen grid bars)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 fallen grid cases",
    }
    sup_pass = None if top_mean is None else bool(top_mean > 0)
    supporting = {
        "name": "top forecast tercile mean excess 72-bar return > 0",
        "value": top_mean,
        "passed": sup_pass,
    }

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} fallen grid cases, below the plan's minimum of 300."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top tercile's mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top tercile's mean excess return is not above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

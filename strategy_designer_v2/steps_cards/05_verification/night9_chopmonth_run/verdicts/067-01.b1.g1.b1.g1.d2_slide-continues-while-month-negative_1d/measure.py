import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RET30_COL = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            # 30-bar return: the recorded raw value, else recomputed from the window's prices
            ret30_px = (close / close.shift(30) - 1.0) * 100.0
            if RET30_COL in d.columns:
                ret30 = pd.to_numeric(d[RET30_COL], errors="coerce")
                ret30 = ret30.where(ret30.notna(), ret30_px)
            else:
                ret30 = ret30_px

            # 60-bar return: not recorded (detector component), recomputed from the prices
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            chop_px = (ret60 >= -10.0) & (ret60 <= 10.0)
            # where the window lacks 60 earlier bars, the detector's own decision stands in
            chop = chop_px.where(ret60.notna(), regime == "chop").astype(bool)

            situation = chop & (ret30 < 0).fillna(False)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    reading = ("60-bar return recomputed in percent from each window's closes (bounds inclusive), with the "
               "recorded regime used where fewer than 60 earlier bars exist in the window; 30-bar return taken "
               "from month_fall's raw value; grid at positions 0,10,20,... of each window, coin mean 10-bar return "
               "over all grid bars of all its windows; the fewer-than-100 rule treated as a minimum count "
               "(not observable); short grid cases counted only where the 10-bar return exists.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars of the plan's "
                           "situation (60-bar return in -10..+10 % and 30-bar return below 0)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, float(fc[i]) if np.isfinite(fc[i]) else np.nan, c1 / c0 - 1.0))

    grid = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    if len(grid):
        grid["coin_mean"] = grid.groupby("coin")["ret"].transform("mean")
        grid["excess"] = grid["ret"] - grid["coin_mean"]
        shorts = grid[(grid["forecast"] < 0) & grid["excess"].notna()]
    else:
        shorts = pd.DataFrame(columns=["forecast", "excess"])

    n_short = int(len(shorts))
    counts = {"short grid cases": n_short}
    threshold = "slope > 0 with t >= 2 confirms (with mean excess < 0); slope < 0 with t <= -2 rejects"

    slope = None
    tval = None
    mean_ex = None
    if n_short >= 3 and shorts["forecast"].nunique() > 1:
        lr = stats.linregress(shorts["forecast"].values, shorts["excess"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_short > 0:
        mean_ex = float(shorts["excess"].mean())

    main = {"name": "slope of excess 10-bar return on forecast (short grid bars)",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold}
    sup_pass = (mean_ex < 0) if mean_ex is not None else None
    support = {"name": "mean excess 10-bar return on short grid bars below 0",
               "value": mean_ex, "passed": sup_pass}

    if n_short < 100:
        status = "not observable"
        decided = f"Only {n_short} short grid cases, fewer than the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean excess 10-bar return is below 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope (t >= 2) but the mean excess 10-bar return is at or above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

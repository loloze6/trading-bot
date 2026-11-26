import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    PP = "debug_info.components.range_swing.post_pipeline_value"
    LH = "debug_info.components.range_swing.last_history_value"
    MIN_CASES = 300

    # ---------- 1. Situation check: down close (close < prior close), long side ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            prev = close.shift(1)
            down = (close < prev)
            # first bar of a window: its prior close is not in the record; use the detector's recorded decision
            if len(df) > 0 and "regime" in df.columns:
                down.iloc[0] = str(df["regime"].iloc[0]) == "mean_reversion"
            # the component must have been computed (recorded) and be a positive range in swing units
            if LH in df.columns:
                lh = pd.to_numeric(df[LH], errors="coerce")
                comp_ok = lh.notna() & (lh > 0)
            else:
                comp_ok = pd.Series(False, index=df.index)
            active = fc != 0
            agree = active & down & comp_ok & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("The first bar of each window has no recorded prior close, so its down close is read from the recorded "
               "regime; the coin's mean daily return is the mean of all its within-window 1-bar close-to-close returns "
               "over all windows; every forecast>0 bar with a next close in the same window is a case, pooled across "
               "coins in one OLS of next-day excess return on post_pipeline_value, slope t = slope / its standard error; "
               "fewer than 300 cases gives 'not observable' as the workflow requires for unmet minimum counts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are down-closing days with a long "
                           "forecast sized by the range in swing units, as the plan's Fidelity requires"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin in sorted(bars.keys()):
        # coin's mean daily return over all its windows
        all_rets = []
        frames = []
        for w in bars[coin].keys():
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            frames.append((df, nxt))
        if not all_rets:
            continue
        allr = np.concatenate(all_rets)
        if allr.size == 0:
            continue
        mu = float(np.mean(allr))
        for df, nxt in frames:
            fc = pd.to_numeric(df[FC], errors="coerce")
            pp = pd.to_numeric(df[PP], errors="coerce") if PP in df.columns else pd.Series(np.nan, index=df.index)
            m = (fc > 0) & nxt.notna() & pp.notna()
            xs.append(pp[m].values.astype(float))
            ys.append((nxt[m] - mu).values.astype(float))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_cases = int(len(x))

    slope = None
    t_slope = None
    mean_ex = float(np.mean(y)) if n_cases > 0 else None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_pass = (mean_ex > 0) if mean_ex is not None else None

    main = {
        "name": "t of the slope of next-day excess return on the range_swing forecast",
        "value": t_slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if slope t >= +2 (with mean excess > 0); reject if slope t <= -2",
    }
    supporting = {"name": "mean next-day excess return over the cases", "value": mean_ex,
                  "passed": None if sup_pass is None else bool(sup_pass)}
    counts = {"cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases across coins and windows, fewer than the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast over the cases)."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is >= +2 and the mean next-day excess return over the cases is > 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2: the rebound shrinks or reverses as the range widens."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is >= +2 but the mean next-day excess return is <= 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    DD = "debug_info.components.down_day.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1_px = close / close.shift(1) - 1.0
            if DD in df.columns:
                drop = pd.to_numeric(df[DD], errors="coerce")
                drop = drop.where(drop.notna(), ret1_px)
            else:
                drop = ret1_px
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = fc.notna() & (fc != 0)
            situation = (regime == "trending") & (drop < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess next-bar return (forecast > 0 bars minus coin holding mean)"
    threshold = "confirm if mean > 0 with t >= 2.0; reject if mean < 0 with t <= -2.0; else inconclusive; at least 200 forecast > 0 bars"
    reading = ("Uptrend checked on the recorded regime label 'trending' and the drop as a negative 1-day return "
               "(down_day raw value, else close-to-close); the holding mean is each coin's mean next-bar return over all "
               "windows present in the record (12 here, not 24); fewer than 200 bars is reported as not observable "
               "per the minimum-count rule; the supporting slope passes if positive.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": None},
            "decided_by": ("Fewer than 90% of active bars are long bars in the 'trending' regime (20- and 60-day returns "
                           "positive) on a down day, as the plan's situation requires."
                           if n_active > 0 else "No active bars: the config never takes the plan's position."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess_list = []
    fc_list = []
    for coin, wins in bars.items():
        all_next = []
        per_win = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            all_next.append(nxt.dropna().values)
            per_win.append((nxt, fc))
        allv = np.concatenate(all_next) if all_next else np.array([])
        if allv.size == 0:
            continue
        hold_mean = float(np.mean(allv))
        for nxt, fc in per_win:
            m = (fc > 0) & nxt.notna() & fc.notna()
            excess_list.append((nxt[m] - hold_mean).values)
            fc_list.append(fc[m].values)

    ex = np.concatenate(excess_list) if excess_list else np.array([])
    fcv = np.concatenate(fc_list) if fc_list else np.array([])
    n = int(ex.size)

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(ex, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None

    slope = None
    if n > 2 and np.std(fcv) > 0:
        slope = float(stats.linregress(fcv, ex).slope)
    supporting = {
        "name": "OLS slope of excess next-bar return on forecast size",
        "value": slope,
        "passed": (bool(slope > 0) if slope is not None else None),
    }

    counts = {"bars with forecast > 0": n}

    if n < 200:
        status = "not observable"
        decided = f"Only {n} bars with forecast > 0 pooled across coins and windows, below the plan's minimum of 200."
    elif t is not None and mean_ex > 0 and t >= 2.0:
        status = "confirmed"
        decided = "The mean excess next-bar return is positive with t >= 2.0."
    elif t is not None and mean_ex < 0 and t <= -2.0:
        status = "rejected"
        decided = "The mean excess next-bar return is negative with t <= -2.0."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2.0 and 2.0, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

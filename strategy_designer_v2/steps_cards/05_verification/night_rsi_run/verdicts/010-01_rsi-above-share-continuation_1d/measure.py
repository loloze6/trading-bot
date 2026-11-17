import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    MIN_SAMPLES = 300
    COMP = "debug_info.components.rsi_share.last_history_value"
    EPS = 1e-9

    # ---------- 1. Situation check ----------
    # Collect the raw component values, so the scale (share vs share-0.5) is read once
    raw_all = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if COMP in df.columns:
                raw_all.append(pd.to_numeric(df[COMP], errors="coerce").dropna().values)
    raw_all = np.concatenate(raw_all) if raw_all else np.array([])

    # Decide how the raw value relates to the plan's situation (share of 30 days RSI > 50)
    if raw_all.size and raw_all.min() >= -EPS and raw_all.max() <= 1 + EPS:
        offset = 0.5          # raw is the share itself in [0, 1]; midpoint at 0.5
        scale_note = "share in [0,1], centred at 0.5"
    else:
        offset = 0.0          # raw is already share - 0.5 (or a scale-only transform of it)
        scale_note = "value already centred at 0"

    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if COMP not in df.columns or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            s = pd.to_numeric(df[COMP], errors="coerce") - offset
            ok = f.notna() & s.notna()
            f = f[ok].values
            s = s[ok].values
            active = np.abs(f) > 0
            n_active += int(active.sum())
            in_situation = np.abs(s) > EPS
            # expected side: larger share (above one half) -> long; smaller -> short
            same_side = np.sign(f) == np.sign(s)
            n_agree += int((active & in_situation & same_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation check uses debug_info.components.rsi_share.last_history_value read as "
               + scale_note + ", expected side long when the share is above one half and short below; "
               "the coin's mean 14-bar return is taken over that coin's non-overlapping samples pooled across all its windows, "
               "the slope t is the OLS t of excess return on forecast over all pooled samples, "
               "and the plan's three-coin count is applied as written to the coins present in the record.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Only {:.1%} of active bars have a forecast whose sign matches the side of the "
                           "30-day RSI-above-50 share relative to one half, below the required 90%.").format(agreement),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    samples = []  # (coin, forecast, return)
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, ft = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(ft)) or c0 == 0:
                    continue
                samples.append((coin, float(ft), float(c1 / c0 - 1.0)))

    sdf = pd.DataFrame(samples, columns=["coin", "forecast", "ret"])
    n_samples = int(len(sdf))
    counts = {"independent 14-bar samples": n_samples}

    if n_samples > 0:
        sdf["excess"] = sdf["ret"] - sdf.groupby("coin")["ret"].transform("mean")

    # slope t-statistic
    t_slope = None
    slope = None
    if n_samples >= 3 and sdf["forecast"].nunique() > 1:
        lr = stats.linregress(sdf["forecast"].values, sdf["excess"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # supporting check
    diff = None
    check_passed = None
    if n_samples > 0:
        pos = sdf.loc[sdf["forecast"] > 0, "excess"]
        neg = sdf.loc[sdf["forecast"] < 0, "excess"]
        counts["samples with forecast > 0"] = int(len(pos))
        counts["samples with forecast < 0"] = int(len(neg))
        if len(pos) > 0 and len(neg) > 0:
            diff = float(pos.mean() - neg.mean())
            check_passed = bool(diff > 0)
        else:
            check_passed = False

    main = {
        "name": "t-statistic of the slope of next 14-bar excess return on forecast",
        "value": t_slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if t >= +2 with the check passing; reject if t <= -2; otherwise inconclusive",
    }
    support = {
        "name": "mean excess 14-bar return, forecast > 0 minus forecast < 0",
        "value": diff,
        "passed": check_passed,
    }

    if n_samples < MIN_SAMPLES:
        status = "not observable"
        decided = "Only {} independent 14-bar samples, below the plan's minimum of 300.".format(n_samples)
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and check_passed:
        status = "confirmed"
        decided = "The slope t-statistic is >= +2 and the forecast>0 minus forecast<0 excess-return difference is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t-statistic is <= -2: returns run against the side RSI has held."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t-statistic is >= +2 but the supporting difference is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope t-statistic lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

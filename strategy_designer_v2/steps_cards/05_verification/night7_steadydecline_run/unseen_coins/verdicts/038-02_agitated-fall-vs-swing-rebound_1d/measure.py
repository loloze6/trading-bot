import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the falling agitated profile (no veto hit)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            situation = (raw < 0) & (reg == PROFILE_REGIME)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of the slope of next-day excess return on forecast, bars with forecast > 0"
    main_threshold = "confirm: slope t >= 2 (with mean excess > 0 and >= 100 cases); reject: slope t <= -2 or mean excess t <= -2 (>= 100 cases)"
    reading = ("Profile read from the recorded regime ('unknown' = no veto, i.e. falling agitated) since the detector's "
               "components are not recorded; the fall is a raw scaled return below 0 and the expected side long; "
               "the regression pools all coins' bars with forecast > 0, each coin's mean daily return taken over all its "
               "windows, and the cases are those bars with a next bar in the same window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days (raw scaled return < 0) "
                           "inside the falling agitated profile with a long forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            nxt = close[1:] / close[:-1] - 1.0
            all_r.append(nxt)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)[:-1]
            per_win.append((fc, nxt))
        if not all_r:
            continue
        allr = np.concatenate(all_r)
        allr = allr[np.isfinite(allr)]
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for fc, nxt in per_win:
            m = np.isfinite(fc) & np.isfinite(nxt) & (fc > 0)
            xs.append(fc[m])
            ys.append(nxt[m] - mu)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(len(x))

    slope = None
    slope_t = None
    if n >= 3 and np.var(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_ex = float(np.mean(y)) if n > 0 else None
    mean_t = None
    if n >= 2:
        sd = float(np.std(y, ddof=1))
        if sd > 0:
            mean_t = float(mean_ex / (sd / np.sqrt(n)))
    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    counts = {"cases with forecast > 0": n}

    if n < 100:
        status = "not observable"
        decided = "Fewer than 100 cases with forecast > 0: the plan's minimum count is not reached."
    elif (slope_t is not None and slope_t <= -2) or (mean_t is not None and mean_t <= -2):
        status = "rejected"
        if slope_t is not None and slope_t <= -2:
            decided = "Reject: the slope's t is -2 or less with at least 100 cases."
        else:
            decided = "Reject: the mean next-day excess return has a t of -2 or less (falls followed by further declines)."
    elif slope_t is not None and slope_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope's t is 2 or more, the mean next-day excess return is above 0, with at least 100 cases."
    else:
        status = "inconclusive"
        if slope_t is not None and slope_t >= 2:
            decided = "Inconclusive: slope t of 2 or more but the mean next-day excess return is 0 or less."
        else:
            decided = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": slope_t} if slope_t is not None else None,
            "threshold": main_threshold,
        },
        "supporting_check": {
            "name": "mean next-day excess return on forecast > 0 bars above 0 (t of mean given)",
            "value": mean_ex,
            "passed": sup_pass,
            "t": mean_t,
        } if False else {
            "name": "mean next-day excess return on forecast > 0 bars above 0",
            "value": mean_ex,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided + (f" (mean excess t = {mean_t:.3f})" if mean_t is not None else ""),
        "reading": reading,
    }

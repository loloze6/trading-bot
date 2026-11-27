import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: a one-day rise (up day) in the falling-calm profile, side short.
    # Profile: regime detector vetoes to "chop" when the 60-bar trend >= -10 or the swing percentile > 0.5,
    # otherwise default "unknown". So the profile holds where regime == "unknown".
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            up = np.where(raw.notna(), raw > 0, ret1 > 0)
            profile = df["regime"].astype(str).str.lower().eq("unknown").values
            situation = profile & up
            active = (fc.fillna(0).values != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc.fillna(0).values < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 3-bar excess return on forecast (forecast < 0 grid cases)"
    main_thr = "slope > 0 with t >= 2 confirms; t <= -2 rejects"
    sup_name = "mean unusual move in short direction, day-clustered t"
    reading = ("The falling-calm profile is read from the recorded regime ('unknown' = no veto, since the detector's "
               "components are not recorded), an up day is a positive raw scaled return (or a positive close-to-close "
               "return where it is not recorded), all coins in the record are used, the coin's mean 3-bar return is "
               "the mean over the non-overlapping grids of all its windows, the day-clustered t sums each day's "
               "deviations from the mean, and the plan's 'below the minimum counts it is inconclusive' is reported "
               "as 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"grid cases with forecast < 0": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of active bars are up days in the falling-calm profile with a short forecast "
                           f"(agreement {agreement}), so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_rows.append((coin, ts.iloc[i].floor("D"), fc[i], r))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for (c, d, f, r) in coin_rows:
            rows.append({"coin": c, "day": d, "forecast": f, "excess": r - mu})

    cases = pd.DataFrame(rows, columns=["coin", "day", "forecast", "excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases with forecast < 0": n_cases, "distinct days": n_days}

    slope = slope_t = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        lr = stats.linregress(cases["forecast"].values, cases["excess"].values)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_mean = sup_t = None
    if n_cases >= 2:
        x = -cases["excess"].values  # unusual move in the short direction
        sup_mean = float(np.mean(x))
        dev = pd.Series(x - sup_mean, index=cases.index).groupby(cases["day"].values).sum()
        se = float(np.sqrt(np.sum(dev.values ** 2)) / n_cases)
        sup_t = float(sup_mean / se) if se > 0 else None
    sup_passed = None if sup_t is None else bool(sup_mean > 0 and sup_t >= 2)

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "OLS slope t", "value": slope_t} if slope_t is not None else None,
            "threshold": main_thr}
    sup = {"name": sup_name, "value": sup_mean, "passed": sup_passed,
           "t": sup_t} if True else None
    sup = {"name": sup_name + (f" (t = {sup_t:.3f})" if sup_t is not None else ""),
           "value": sup_mean, "passed": sup_passed}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum of 100 grid cases with forecast < 0 over 60 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif (slope_t is not None and slope_t <= -2) or (sup_t is not None and sup_t <= -2):
        status = "rejected"
        decided = "Reject rule met: the slope's t is <= -2 or the short-direction unusual move has t <= -2."
    elif slope is not None and slope_t is not None and slope > 0 and slope_t >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm rule met: the slope is positive with t >= 2 and the short-direction unusual move is positive with t >= 2."
    else:
        status = "inconclusive"
        if slope is not None and slope_t is not None and slope > 0 and slope_t >= 2:
            decided = "The slope meets the confirm rule but the supporting check fails, so the result is inconclusive."
        else:
            decided = "Neither the confirm nor the reject rule is met (t values between -2 and 2), so it is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

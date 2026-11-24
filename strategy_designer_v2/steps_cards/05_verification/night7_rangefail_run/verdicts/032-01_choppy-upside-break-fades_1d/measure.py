import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.overshoot.last_history_value"

    def prep(df):
        df = df.copy().reset_index(drop=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        return df

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = prep(df)
            prepared[(coin, w)] = d
            prior_high = d["high"].shift(1).rolling(20, min_periods=20).max()
            dist_px = (d["close"] - prior_high) / prior_high * 100.0
            if LHV in d.columns:
                dist = pd.to_numeric(d[LHV], errors="coerce").where(lambda s: s.notna(), dist_px)
            else:
                dist = dist_px
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            choppy = d["regime"].astype(str) != "chop"
            situation = (dist > 0) & choppy
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual move in the short direction over 5 bars, t clustered by day"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("The choppy profile is read from the recorded regime (bars not vetoed to 'chop'), the 20-day "
               "distance from the overshoot component's raw value or else recomputed from prices; a case is the "
               "first short bet (forecast rising in size by >= 2 points from its lowest level since the last bet, "
               "from 0 after a flat) in each 5-bar grid cell, the normal drift is the mean of the coin's "
               "non-overlapping 5-bar grid returns over all windows, the clustered t uses per-day summed "
               "deviations with no small-sample correction, and the plan's '<30 cases or days' rule is "
               "reported as 'not observable' as the workflow requires for minimum counts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy bars with the close "
                           "above the prior 20-day high and a short forecast, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w in wins:
            c = prepared[(coin, w)]["close"].to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    vals, sizes, days = [], [], []
    for coin, wins in bars.items():
        for w in wins:
            d = prepared[(coin, w)]
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy()
            c = d["close"].to_numpy(dtype=float)
            ts = d["timestamp"]
            n = len(d)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            side = 0
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s != side:
                    ref = 0.0
                    side = s
                if s == 0:
                    continue
                mag = abs(f)
                if mag - ref >= BAND:
                    bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, n, H):
                for i in range(start, min(start + H, n)):
                    if bet[i] and fc[i] < 0:
                        if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 \
                                and np.isfinite(drift[coin]):
                            r = c[i + H] / c[i] - 1.0
                            vals.append(-(r - drift[coin]))
                            sizes.append(abs(fc[i]))
                            days.append(ts.iloc[i].floor("D"))
                        break

    vals = np.asarray(vals, dtype=float)
    sizes = np.asarray(sizes, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        dev = pd.Series(vals - mean, index=pd.Index(days))
        per_day = dev.groupby(level=0).sum().to_numpy()
        se = np.sqrt(np.sum(per_day ** 2)) / n_cases
        t = float(mean / se) if se > 0 else None
    slope = None
    if n_cases > 1 and np.ptp(sizes) > 0:
        slope = float(np.polyfit(sizes, vals, 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    stat = {"name": "t of the mean, cases clustered by day", "value": t} if t is not None else None
    main = {"name": main_name, "value": mean, "statistic": stat, "threshold": threshold}
    supp = {"name": "OLS slope of unusual move on |forecast|", "value": slope, "passed": slope_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum is not reached: {n_cases} cases on {n_days} distinct days, "
                   "against at least 30 cases and 30 distinct days.")
    elif t is not None and mean > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the slope on the overshoot size is above 0."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2: the breaks keep rising beyond the coin's drift."
    else:
        status = "inconclusive"
        if t is not None and t >= 2:
            decided = "t >= 2 but the slope on the overshoot size is at or below 0 (or undefined): inconclusive."
        else:
            decided = "The t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

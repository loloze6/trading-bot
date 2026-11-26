import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    ER_P, ER_S, ER_MAX = 60, 5, 0.3
    DFH_P = 60
    OV_COL = "debug_info.components.overshoot.last_history_value"

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return x if np.isfinite(x) else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_active_checkable = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0)
            # Kaufman efficiency ratio over 60 bars, smoothed by a 5-bar mean
            change = (close - close.shift(ER_P)).abs()
            path = close.diff().abs().rolling(ER_P).sum()
            er = (change / path.replace(0, np.nan)).rolling(ER_S).mean()
            # percent distance of the close above the highest high of the 60 prior bars
            prior_high = high.shift(1).rolling(DFH_P).max()
            dfh_px = (close / prior_high - 1.0) * 100.0
            if OV_COL in d.columns:
                dfh = d[OV_COL].astype(float).where(d[OV_COL].notna(), dfh_px)
            else:
                dfh = dfh_px
            active = fc != 0
            n_active += int(active.sum())
            checkable = active & er.notna() & dfh.notna()
            n_active_checkable += int(checkable.sum())
            situ = (er <= ER_MAX) & (dfh > 0) & (fc < 0)
            n_agree += int((checkable & situ).sum())

    agreement = (n_agree / n_active_checkable) if n_active_checkable > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading_check = ("the efficiency ratio is rebuilt from closes as |close change over 60 bars| / sum of 60 "
                     "absolute daily changes, smoothed by a 5-bar mean, and only active bars with enough "
                     "in-window history to compute it enter the agreement share")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-side unusual 10-bar move", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None, "active bars": n_active,
                       "active bars checked": n_active_checkable},
            "decided_by": ("fewer than 90% of the active bars are short bars on a trendless (ER<=0.3) close "
                           "above the prior 60-bar high, as the Fidelity's situation and side require"),
            "reading": reading_check,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual_short, overshoot)
    for coin, wins in bars.items():
        # coin's normal 10-bar drift over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            fc = d["forecast"].astype(float).fillna(0.0).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            ov = d[OV_COL].astype(float).to_numpy() if OV_COL in d.columns else np.full(len(d), np.nan)
            side, low = 0, 0.0
            bet = np.zeros(len(d), dtype=bool)
            for i in range(len(d)):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    side, low = 0, 0.0
                    continue
                if s != side:
                    side, low = s, 0.0
                mag = abs(f)
                if mag - low >= BAND:
                    if s < 0:
                        bet[i] = True
                    low = mag
                else:
                    low = min(low, mag)
            # one case per 10-bar grid cell: the cell's first short bet
            for start in range(0, len(d), H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= len(d):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                cases.append((ts.iloc[t], -(r - drift), ov[t]))

    n_cases = len(cases)
    vals = np.array([x[1] for x in cases], dtype=float)
    days = [x[0] for x in cases]
    n_days = len(set(days))

    mean_val, t_stat = None, None
    if n_cases >= 2 and n_days >= 2:
        m = float(vals.mean())
        dev = pd.Series(vals - m).groupby(pd.Series(days)).sum().to_numpy()
        G = len(dev)
        var_mean = (G / (G - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
        se = np.sqrt(var_mean)
        mean_val = m
        t_stat = float(m / se) if se > 0 else None
    elif n_cases >= 1:
        mean_val = float(vals.mean())

    ov_arr = np.array([x[2] for x in cases], dtype=float)
    ok = np.isfinite(ov_arr) & np.isfinite(vals)
    slope = None
    if ok.sum() >= 2 and np.var(ov_arr[ok]) > 0:
        slope = float(np.polyfit(ov_arr[ok], vals[ok], 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"the plan's minimum of 30 cases and 30 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days)")
    elif t_stat is None:
        status = "inconclusive"
        decided = "the t of the mean short-side unusual move could not be computed (zero spread)"
    elif t_stat >= 2 and slope_pass:
        status = "confirmed"
        decided = "the mean short-side unusual move has t >= 2 and the slope on the overshoot is above 0"
    elif t_stat <= -2:
        status = "rejected"
        decided = "the mean short-side unusual move has t <= -2: the breakouts keep rising beyond the drift"
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope of the unusual move on the overshoot is at or below 0 (or not computable)"
    else:
        status = "inconclusive"
        decided = "the t of the mean short-side unusual move lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "mean short-side unusual 10-bar move (return minus coin drift, fall positive)",
            "value": mean_val,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases summed per day",
                                                      "value": t_stat},
            "threshold": "t >= 2 (with slope > 0) confirms, t <= -2 rejects, otherwise inconclusive",
        },
        "supporting_check": {"name": "OLS slope of unusual move on raw overshoot",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": int(n_cases), "distinct days": int(n_days)},
        "decided_by": decided,
        "reading": (reading_check + "; a case is the first short bet (forecast rise of at least 2 points on "
                    "the short side) in each 10-bar grid cell counted from each window's first row, cases "
                    "without 10 later bars in their window are dropped, the drift is the mean of the coin's "
                    "non-overlapping 10-bar grid returns over all windows, and fewer than 30 cases or days "
                    "gives 'not observable' as the workflow's minimum-count rule requires"),
    }

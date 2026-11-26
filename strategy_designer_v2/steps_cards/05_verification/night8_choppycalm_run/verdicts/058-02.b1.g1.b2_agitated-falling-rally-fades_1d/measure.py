import numpy as np
import pandas as pd


def measure(bars):
    LH = "debug_info.components.scaled_rise.last_history_value"
    PP = "debug_info.components.scaled_rise.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_frames = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            raw = d[LH].astype(float) if LH in d.columns else pd.Series(np.nan, index=d.index)
            rise_val = raw.where(raw.notna(), ret1)
            rise = rise_val > 0
            # The falling, agitated profile is what the detector leaves as 'unknown'
            # (neither veto to 'chop' fired: 60-bar evolution < -10 and vol percentile > 0.5).
            in_profile = d["regime"].astype(str) == "unknown"
            fc = d["forecast"].astype(float).fillna(0.0)
            active = fc != 0
            situ = in_profile & rise & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
            # next-bar return inside the window
            d["_next_ret"] = close.shift(-1) / close - 1.0
            d["_ret1"] = ret1
            coin_frames.setdefault(coin, []).append(d)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90% of the active bars are up days inside the falling, agitated profile "
                           "with a short forecast" if n_active > 0 else "no active bars: the forecast is never non-zero"),
            "reading": "the profile is read from the recorded regime ('unknown' = neither chop veto fired); "
                       "the rise is the recorded raw scaled return > 0, or the 1-bar return when not recorded",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, frames in coin_frames.items():
        allr = pd.concat([f["_next_ret"] for f in frames]).dropna()
        mu = float(allr.mean()) if len(allr) else np.nan
        for f in frames:
            if PP not in f.columns:
                continue
            fc = f["forecast"].astype(float)
            m = (fc < 0) & f["_next_ret"].notna() & f[PP].notna()
            sub = f.loc[m]
            for ts, x, r in zip(sub["timestamp"], sub[PP].astype(float), sub["_next_ret"].astype(float)):
                rows.append((ts.floor("D"), x, r - mu))
    if rows:
        data = pd.DataFrame(rows, columns=["day", "x", "y"])
    else:
        data = pd.DataFrame(columns=["day", "x", "y"])

    n_bars = int(len(data))
    n_days = int(data["day"].nunique()) if n_bars else 0
    counts = {"bars with a forecast below 0": n_bars, "distinct days": n_days}

    slope = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_bars >= 3:
        x = data["x"].values.astype(float)
        y = data["y"].values.astype(float)
        X = np.column_stack([np.ones(n_bars), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            resid = y - X @ beta
            meat = np.zeros((2, 2))
            codes = pd.factorize(data["day"])[0]
            G = codes.max() + 1
            for g in range(G):
                idx = codes == g
                s = X[idx].T @ resid[idx]
                meat += np.outer(s, s)
            K = 2
            corr = (G / (G - 1)) * ((n_bars - 1) / (n_bars - K)) if G > 1 else 1.0
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if se and np.isfinite(se) else None
        sup_val = float(np.mean(-y))
        sup_pass = bool(sup_val > 0)

    main = {
        "name": "slope of demeaned next-day return on post_pipeline_value (forecast < 0)",
        "value": slope,
        "statistic": {"name": "t, errors clustered by day", "value": tval} if tval is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2",
    }
    supporting = {"name": "mean unusual move in the short direction", "value": sup_val, "passed": sup_pass}

    reading = ("the profile is read from the recorded regime ('unknown' = neither chop veto fired) and the rise from the "
               "recorded raw value (1-bar return when unrecorded); the coin's mean daily return is the mean of all its "
               "within-window next-day returns; the slope is OLS with intercept and CR1 day-clustered errors; "
               "the plan's 'fewer is inconclusive' minimum is reported as 'not observable' as the workflow requires")

    if n_bars < 100 or n_days < 60:
        status = "not observable"
        decided = ("the minimum of 100 bars with a forecast below 0 on at least 60 distinct days is not reached "
                   f"({n_bars} bars, {n_days} days)")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "the slope or its t could not be computed"
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "the slope is positive with t >= 2 and the mean unusual move in the short direction is above 0"
        else:
            status = "inconclusive"
            decided = "the slope is positive with t >= 2 but the supporting check fails"
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "the slope is negative with t <= -2"
    else:
        status = "inconclusive"
        decided = "the t of the slope lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

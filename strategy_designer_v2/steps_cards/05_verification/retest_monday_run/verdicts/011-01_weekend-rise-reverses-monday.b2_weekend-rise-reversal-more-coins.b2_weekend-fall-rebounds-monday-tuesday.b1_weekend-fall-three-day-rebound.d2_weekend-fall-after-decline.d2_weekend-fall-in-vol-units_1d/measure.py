import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    COMP = "debug_info.components.weekend_fall.last_history_value"
    MIN_CASES = 200

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce")
            ret1 = (close / close.shift(1) - 1.0).values
            if COMP in d.columns:
                raw = pd.to_numeric(d[COMP], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            # raw value missing: its sign is the sign of the one-bar return
            raw_sign_src = np.where(np.isnan(raw), ret1, raw)
            sunday = (ts.dt.weekday == 6).values  # bar opening Sunday: next bar is Monday
            fall = raw_sign_src < 0
            situation = sunday & fall
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are Sunday bars after a one-bar fall with a long forecast"
                           if n_active > 0 else "No active bars: the config never takes the plan's position"),
            "reading": "Sunday bar = bar whose UTC start is a Sunday (its next bar is Monday); fall = negative raw component value, or negative one-bar return where the component is not recorded.",
        }

    # ---------- 2. per-coin normal 3-bar drift ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                a, b = c[i], c[i + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    F = []
    X = []
    for coin, wins in bars.items():
        dr = drift.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            c = pd.to_numeric(d["close"], errors="coerce").values
            reg = d["regime"].astype(str).values
            sunday = (ts.dt.weekday == 6).values
            for i in range(len(d) - H):
                if not sunday[i] or reg[i] != "mean_reversion":
                    continue
                if not np.isfinite(fc[i]) or fc[i] < 2:
                    continue
                a, b = c[i], c[i + H]
                if not (np.isfinite(a) and np.isfinite(b)) or a == 0:
                    continue
                F.append(float(fc[i]))
                X.append(b / a - 1.0 - dr)

    F = np.asarray(F, dtype=float)
    X = np.asarray(X, dtype=float)
    n = int(len(F))

    wmean = None
    tval = None
    slope = None
    if n >= 1 and F.sum() > 0:
        wmean = float(np.sum(F * X) / np.sum(F))
    if n >= 2:
        z = F * X
        sd = np.std(z, ddof=1)
        if sd > 0:
            tval = float(np.mean(z) / (sd / np.sqrt(n)))
        if np.std(F) > 0:
            slope = float(stats.linregress(F, X).slope)

    slope_passed = None if slope is None else bool(slope > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases (Sunday bars with forecast >= 2 and a full 3-bar return), fewer than the 200 the plan requires."
    elif wmean is not None and tval is not None and wmean > 0 and tval >= 2 and slope_passed:
        status = "confirmed"
        decided = "Confirm: weighted mean excess 3-bar return above 0 with t >= 2 and a positive slope on the forecast."
    elif wmean is not None and tval is not None and wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject: weighted mean excess 3-bar return below 0 with t <= -2."
    elif tval is not None and tval >= 2 and not slope_passed:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the slope of excess return on forecast is at or below 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t between -2 and 2 (or not computable)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "forecast-weighted mean excess 3-bar return after Sunday falls",
            "value": wmean,
            "statistic": None if tval is None else {"name": "ordinary t of the mean of forecast-scaled excess returns", "value": tval},
            "threshold": "confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "least-squares slope of excess 3-bar return on forecast > 0",
            "value": slope,
            "passed": slope_passed,
        },
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": "Every Sunday bar (UTC start on Sunday) in regime mean_reversion with forecast >= 2 and three later bars in its window is one case (Sundays are 7 bars apart, so their 3-bar returns never overlap), and the coin's drift is the mean of its 3-bar returns on the grid 0, 3, 6, ... of each window, pooled over all its windows.",
    }

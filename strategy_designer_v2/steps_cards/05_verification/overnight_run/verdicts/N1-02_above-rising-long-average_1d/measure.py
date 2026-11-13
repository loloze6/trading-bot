import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    DIST = "debug_info.components.dist.last_history_value"

    # ---------- Situation check ----------
    # Detect the units of the raw distance from its magnitude: percent if median |d| > 1, else a fraction.
    all_d = []
    for coin in bars:
        for w, df in bars[coin].items():
            if DIST in df.columns:
                all_d.append(pd.to_numeric(df[DIST], errors="coerce").values)
    all_d = np.concatenate(all_d) if all_d else np.array([])
    med = np.nanmedian(np.abs(all_d)) if np.isfinite(all_d).any() else 0.0
    scale = 100.0 if med > 1.0 else 1.0

    n_active_eval = 0
    n_agree = 0
    for coin in bars:
        for w, df in bars[coin].items():
            if DIST not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            d = pd.to_numeric(df[DIST], errors="coerce").values.astype(float)
            sma = close / (1.0 + d / scale)
            n = len(df)
            for t in range(n):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                if t < H or not (np.isfinite(sma[t]) and np.isfinite(sma[t - H]) and np.isfinite(d[t])):
                    continue
                n_active_eval += 1
                in_sit = (sma[t] - sma[t - H] > 0) and (d[t] > 0)
                if in_sit and fc[t] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active_eval) if n_active_eval > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = (
        "The SMA200 is rebuilt from the close and the raw distance (taken as percent if its median absolute value "
        "exceeds 1, else as a fraction) and its 20-bar slope is checked only on active bars at least 20 rows into "
        "their window; the main value pools all bars (overlapping) while its t is Welch's t between active and all "
        "bars on the 0,20,40,... grid of each window; the plan's '<30 non-overlapping active cases' rule is "
        "reported as not observable; the supporting slope uses 20-bar forward log returns on all active bars."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_eval)},
            "decided_by": "Fewer than 90% of active bars are long bars where the close is above a 200-day SMA that "
                          "has risen over 20 bars, so the config does not trade the plan's situation.",
            "reading": reading,
        }

    # ---------- Criterion ----------
    act_all, hold_all = [], []
    act_grid, hold_grid = [], []
    sup_x, sup_y = [], []
    for coin in bars:
        for w, df in bars[coin].items():
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(df)
            for t in range(n - H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0 and c1 > 0):
                    continue
                r = np.log(c1 / c0)
                hold_all.append(r)
                on_grid = (t % H == 0)
                if on_grid:
                    hold_grid.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    act_all.append(r)
                    sup_x.append(fc[t])
                    sup_y.append(r)
                    if on_grid:
                        act_grid.append(r)

    n_act_grid = len(act_grid)
    counts = {
        "non-overlapping 20-bar active cases": int(n_act_grid),
        "non-overlapping 20-bar holding cases": int(len(hold_grid)),
        "active bars": int(len(act_all)),
    }

    value = (float(np.mean(act_all) - np.mean(hold_all))
             if len(act_all) > 0 and len(hold_all) > 0 else None)

    tval = None
    if n_act_grid >= 2 and len(hold_grid) >= 2:
        tt = stats.ttest_ind(np.array(act_grid), np.array(hold_grid), equal_var=False)
        tval = float(tt.statistic) if np.isfinite(tt.statistic) else None

    slope = None
    if len(sup_x) >= 3 and np.std(sup_x) > 0:
        slope = float(stats.linregress(np.array(sup_x), np.array(sup_y)).slope)
    supporting = {
        "name": "OLS slope of 20-bar forward log return on forecast, active bars",
        "value": slope,
        "passed": (slope > 0) if slope is not None else None,
    }

    main = {
        "name": "mean 20-bar forward log return on forecast>0 bars minus mean over all bars (holding)",
        "value": value,
        "statistic": {"name": "Welch t, non-overlapping 20-bar blocks", "value": tval} if tval is not None else None,
        "threshold": "confirm if excess > 0 with t >= 2; reject if excess < 0 with t <= -2; otherwise inconclusive",
    }

    if n_act_grid < 30:
        status = "not observable"
        decided = f"Only {n_act_grid} non-overlapping 20-bar active cases pooled, below the plan's minimum of 30."
    elif tval is None or value is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tval >= 2:
        status = "confirmed"
        decided = "The excess mean forward return over holding is positive with t >= 2."
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = "The excess mean forward return over holding is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (or disagrees in sign with the excess), meeting neither rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    FC = "forecast"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df[FC].astype(float).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else None
            n = len(df)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if i >= 30 and close[i - 30] > 0:
                    in_sit = (close[i] / close[i - 30] - 1.0) < 0.0
                else:
                    in_sit = reg is not None and reg[i] == "mean_reversion"
                if in_sit and f < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    reading = ("Situation = 30-bar close return < 0 computed inside each window (falling back to the recorded "
               "regime 'mean_reversion' on the first 30 bars, where it cannot be computed) with a short forecast; "
               "a case is the first bar in each 5-bar grid cell (positions 0,5,10,... of each window) where the "
               "short forecast's size rises by >= 2 points from its smallest size since the last bet (reset to 0 "
               "at each window start, flat or side change), cases with no 5-bar return inside the window are "
               "dropped, drift is the coin's mean grid 5-bar return over all its windows, and fewer than 30 cases "
               "is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean drift-adjusted 5-bar move in the short direction",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms, t <= -2 rejects, over at least 30 cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars are short bars with a negative 30-bar return, "
                           "below the 90% the plan's situation (falling coin, short only) requires."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases and supporting regression ----------
    unusual = []
    sup_x, sup_y = [], []
    for coin, wins in bars.items():
        d = drift[coin]
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df[FC].astype(float).values
            n = len(df)
            # bets on the short side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            side = 0
            for i in range(n):
                f = fc[i] if np.isfinite(fc[i]) else 0.0
                s = int(np.sign(f))
                if s != side:
                    ref = 0.0
                    side = s
                if s < 0:
                    mag = -f
                    if mag - ref >= BAND:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0
            # one case per grid cell
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] <= 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                unusual.append(-(r - d))
            # supporting: grid bars with forecast < 0
            for i in range(0, n - H, H):
                f = fc[i]
                if np.isfinite(f) and f < 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    sup_x.append(f)
                    sup_y.append(c[i + H] / c[i] - 1.0 - d)

    n_cases = len(unusual)
    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases >= 2:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    if len(sup_x) >= 3 and np.var(sup_x) > 0:
        slope = float(stats.linregress(sup_x, sup_y).slope)
    slope_ok = (slope is not None and slope > 0) if slope is not None else None

    main = {"name": "mean drift-adjusted 5-bar move in the short direction",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "t >= 2 confirms, t <= -2 rejects, over at least 30 independent cases"}
    sup = {"name": "slope of drift-adjusted 5-bar return on forecast (grid bars, forecast < 0)",
           "value": slope, "passed": slope_ok}
    counts = {"independent cases": int(n_cases), "supporting grid bars": int(len(sup_x))}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no spread), so neither rule is met."
    elif t_u >= 2 and slope_ok:
        status = "confirmed"
        decided = "Mean unusual short move has t >= 2 over at least 30 cases and the supporting slope is positive."
    elif t_u >= 2:
        status = "inconclusive"
        decided = "A confirming t >= 2 but the supporting slope is not positive: inconclusive by the plan's rule."
    elif t_u <= -2:
        status = "rejected"
        decided = "Mean unusual short move has t <= -2 over at least 30 cases: choppy falls rebound beyond the drift."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

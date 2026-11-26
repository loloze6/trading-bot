import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    LHV = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            regime = df["regime"].astype(str)
            in_profile = regime == "unknown"
            situation = in_profile & (raw < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of drift-adjusted 7-bar forward return on the forecast (grid bars with negative forecast)"
    threshold = "confirm if slope t >= 2 (with mean unusual short move > 0); reject if slope t <= -2"
    reading = ("Situation bars are those in the choppy agitated profile (regime 'unknown', the detector's non-vetoed state) "
               "with a negative 30-day return; cases are the plan's grid bars (positions 0,7,14,... of each window) with a "
               "negative forecast and a full 7-bar forward return in the window; the coin's normal drift is the mean of its "
               "non-overlapping 7-bar returns over all its windows; the slope's t is the ordinary OLS t (n-2 dof); distinct "
               "days are the UTC dates of the cases; the plan's 'fewer than 30 cases on 20 days' is treated as a minimum count "
               "giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the choppy agitated "
                           "profile with a negative 30-day return, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys, short_moves, days = [], [], [], []
    for coin, wins in bars.items():
        # coin's normal 7-bar drift: non-overlapping grid of all its windows
        all_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        all_rets.append(r)
                        per_window.append((r, fc[i], ts.iloc[i]))
        if len(all_rets) == 0:
            continue
        drift = float(np.mean(all_rets))
        for r, f, t in per_window:
            if np.isfinite(f) and f < 0:
                u = r - drift
                xs.append(float(f))
                ys.append(float(u))
                short_moves.append(-u)
                days.append(t.date())

    n_cases = len(xs)
    n_days = len(set(days))
    counts = {"non-overlapping cases": int(n_cases), "distinct days": int(n_days)}

    slope = None
    t_slope = None
    if n_cases >= 3:
        x = np.array(xs)
        y = np.array(ys)
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            resid = y - (a + b * x)
            s2 = float(np.sum(resid ** 2) / (n_cases - 2))
            se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
            slope = b
            t_slope = float(b / se) if se > 0 else None

    mean_short = float(np.mean(short_moves)) if n_cases > 0 else None
    sup_pass = None if mean_short is None else bool(mean_short > 0)

    main = {"name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold}
    supporting = {"name": "mean unusual move in the short direction (net of drift, before costs)",
                  "value": mean_short, "passed": sup_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum of 30 non-overlapping cases on at least 20 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean unusual move in the short direction is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean unusual move in the short direction is at or below 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper falls are followed by weaker falls or rises relative to drift."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

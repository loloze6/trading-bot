import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 30
    FC = "forecast"
    RET10_COL = "debug_info.components.ret10.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            hi = df["high"].astype(float)
            lo = df["low"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce")

            # NetMoveToRange(30, high-low)
            hh30 = hi.rolling(30, min_periods=30).max()
            ll30 = lo.rolling(30, min_periods=30).min()
            rng = hh30 - ll30
            nmr = (c - c.shift(30)).abs() / rng.replace(0, np.nan)
            # close vs 30-day high-low midpoint (spans of 30, displacement 0)
            mid = (hh30 + ll30) / 2.0
            below_mid = c < mid
            # 10-day return and its scale by mean abs 10-day move over 60 bars
            r10 = c / c.shift(10) - 1.0
            scale = r10.abs().rolling(60, min_periods=60).mean()
            ext = r10 / scale.replace(0, np.nan)
            # 10-day return sign: recorded raw value where present, else from prices
            if RET10_COL in df.columns:
                rec = pd.to_numeric(df[RET10_COL], errors="coerce")
                r10_sign_src = rec.where(rec.notna(), r10)
            else:
                r10_sign_src = r10

            computable = nmr.notna() & mid.notna() & ext.notna() & r10_sign_src.notna()
            situation = (nmr <= 0.3) & below_mid & (ext > -2.0) & (r10_sign_src < 0)

            active = fc.notna() & (fc != 0)
            n_active_uncomputable += int((active & ~computable).sum())
            act_c = active & computable
            n_active += int(act_c.sum())
            n_agree += int((act_c & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation recomputed per window from prices (NMR = |close[t]-close[t-30]| over the 30-bar high-low "
               "range, midpoint of the 30-bar high and low, veto = 10-day return over the mean absolute 10-day return "
               "of the last 60 bars including t), with the 10-day return sign from the recorded ret10 value; active "
               "bars whose situation cannot be computed inside the window are left out of the agreement; the coin's "
               "mean 5-bar return is over its non-overlapping grid returns of all windows; for the supporting check "
               "cases are sorted by absolute forecast and split into two halves of n//2 (the middle case left out "
               "when n is odd).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "t of mean short-side unusual 5-bar move", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject, over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": None, "active bars checked": n_active,
                       "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90% of the active bars are flat-range (NMR <= 0.3), below-midpoint, "
                           "non-extreme negative 10-day-return bars with a short forecast, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, ret, forecast)
    coin_grid_rets = {}
    for coin in sorted(bars.keys()):
        rets_all = []
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                rets_all.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    case_rows.append((coin, r, float(fc[t])))
        coin_grid_rets[coin] = rets_all

    coin_mean = {k: (float(np.mean(v)) if len(v) else np.nan) for k, v in coin_grid_rets.items()}
    unusual = []
    absf = []
    for coin, r, f in case_rows:
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        unusual.append(-(r - m))
        absf.append(abs(f))
    unusual = np.array(unusual, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(unusual, ddof=1))
        if sd > 0:
            t_val = float(mean_u / (sd / np.sqrt(n_cases)))

    diff = None
    if n_cases >= 2:
        order = np.argsort(-absf, kind="mergesort")
        half = n_cases // 2
        large = unusual[order[:half]]
        small = unusual[order[n_cases - half:]]
        if len(large) > 0 and len(small) > 0:
            diff = float(np.mean(large) - np.mean(small))
    sup_passed = (diff > 0) if diff is not None else None

    if n_cases < MIN_CASES or t_val is None:
        status = "not observable"
        decided = f"Fewer than the plan's minimum of 30 cases ({n_cases}) on the non-overlapping 5-bar grid."
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main t is 2 or more over at least 30 cases and the larger-minus-smaller-forecast difference is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main t is -2 or less over at least 30 cases."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "A confirming t with a supporting difference at or below 0."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean short-side unusual 5-bar move", "value": mean_u,
                         "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
                         "threshold": "t >= 2 over at least 30 cases to confirm, t <= -2 to reject"},
        "supporting_check": {"name": "larger-|forecast| half minus smaller half mean unusual move",
                             "value": diff, "passed": (bool(sup_passed) if sup_passed is not None else None)},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    MIN_CASES = 200
    RAW = "debug_info.components.hour_move.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            r1 = close.pct_change()
            vol24 = r1.rolling(24, min_periods=24).std()
            vol720 = r1.rolling(720, min_periods=720).std()
            ratio = vol24 / vol720
            fc = d["forecast"].astype(float)
            if RAW in d.columns:
                raw = d[RAW].astype(float)
                move = raw.where(raw.notna(), r1)
            else:
                move = r1
            active = fc.notna() & (fc != 0)
            verifiable = active & ratio.notna() & move.notna()
            n_active_unverifiable += int((active & ~verifiable).sum())
            a = verifiable
            in_sit = ratio[a] < 1.0
            side_ok = np.sign(fc[a]) == np.sign(move[a])
            n_active += int(a.sum())
            n_agree += int((in_sit & side_ok).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("Volatility ratio recomputed per window from close-to-close hourly returns (rolling std, ddof 1, "
               "24 and 720 returns including the current bar), the expected side is the sign of the hour's move "
               "(raw component value, else the 1-bar price return), active bars without a computable ratio are left "
               "out of the agreement; the drift is each coin's mean 24-bar return over all grid cells of all its "
               "windows, the slope's t is the ordinary OLS t of a pooled regression with intercept, and the "
               "independent cases are the active grid cells with a 24-bar return inside their window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "pooled slope of 24-bar unusual return on forecast", "value": None,
                             "statistic": None, "threshold": "slope t >= 2 to confirm, <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars without computable ratio": n_active_unverifiable},
            "decided_by": ("Fewer than 90% of active bars are bars where the 24-bar return std is below the "
                           "720-bar std with the forecast on the side of the hour's move "
                           f"(agreement {agreement})."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        all_rets = []
        cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and f != 0:
                    cells.append((f, r))
        if not all_rets:
            continue
        drift = float(np.mean(all_rets))
        for f, r in cells:
            xs.append(f)
            ys.append(r - drift)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    sup_val = float(np.mean(np.sign(x) * y)) if n_cases > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {"name": "pooled OLS slope of next-24-bar return minus drift on forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "slope t >= 2 (with check mean > 0) to confirm, slope t <= -2 to reject"}
    support = {"name": "mean of sign(forecast) x (24-bar return - drift)", "value": sup_val,
               "passed": sup_pass}
    counts = {"independent cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 200."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and the supporting check's mean is above 0, with at least 200 independent cases."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2 (moves of quiet hours reverse) with at least 200 independent cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the supporting check's mean is not above 0."
    else:
        status = "inconclusive"
        decided = "Slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    MIN_CASES = 100
    RET_COL = "debug_info.components.weekend_move.last_history_value"

    # ---------- 1. situation check ----------
    n_active_eval = 0
    n_active_total = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            r1 = close.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std()
            sd60 = r1.rolling(60, min_periods=60).std()
            ratio = sd20 / sd60
            if RET_COL in d.columns:
                rec = pd.to_numeric(d[RET_COL], errors="coerce")
                wret = rec.where(rec.notna(), r1)
            else:
                wret = r1
            is_sun = ts.dt.dayofweek == 6
            active = fc != 0
            n_active_total += int(active.sum())
            for i in np.where(active.values)[0]:
                rt = ratio.iloc[i]
                wr = wret.iloc[i]
                if not np.isfinite(rt) or not np.isfinite(wr) or wr == 0:
                    continue
                n_active_eval += 1
                ok = bool(is_sun.iloc[i]) and (rt >= 1.0 - 1e-12) and \
                    (np.sign(fc.iloc[i]) == -np.sign(wr))
                if ok:
                    n_agree += 1

    agreement = float(n_agree / n_active_eval) if n_active_eval > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("A Sunday bar is the daily bar opening on Sunday UTC (its close is Sunday's close); the volatility "
               "ratio is recomputed from closes inside each window as rolling std (ddof 1) of 20 over 60 one-bar "
               "returns including the bar, and active bars where it cannot be computed (first 60 bars of a window) "
               "are left out of the agreement; the drift is each coin's mean 2-bar return on the grid 0,2,4,... "
               "of every window pooled; for the supporting check the larger half is |forecast| strictly above the "
               "median and the smaller half at or below it; fewer than 100 cases gives 'not observable' as the "
               "workflow requires.")

    main_name = "t of mean signed excess 2-bar move after Sunday forecasts"
    threshold = "confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total), "active bars evaluated": int(n_active_eval)},
            "decided_by": ("Fewer than 90% of the active bars are Sunday bars with 20/60-day volatility ratio >= 1 "
                           "and a forecast opposite to the Sunday move, so the config does not do what the "
                           "Fidelity states." if agreement is not None else
                           "No active bar could be checked against the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess, absf = [], []
    for coin, wins in bars.items():
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    grid_rets.append(b / a - 1.0)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for d in prepared:
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(close)
            is_sun = (ts.dt.dayofweek == 6).values
            for i in range(n - H):
                if fc[i] == 0 or not is_sun[i]:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b)) or a == 0:
                    continue
                excess.append(np.sign(fc[i]) * ((b / a - 1.0) - drift))
                absf.append(abs(fc[i]))

    excess = np.array(excess, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    supp_val, supp_pass = None, None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absf))
        large = absf > med
        small = ~large
        n_large, n_small = int(large.sum()), int(small.sum())
        if n_large > 0 and n_small > 0:
            supp_val = float(np.mean(excess[large]) - np.mean(excess[small]))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    counts = {"cases": n_cases, "larger half": n_large, "smaller half": n_small}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 100 cases."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero spread), meeting neither confirm nor reject."
    elif mean_ex > 0 and t_val >= 2 and supp_pass:
        status = "confirmed"
        decided = "Mean signed excess move positive with t >= 2 over at least 100 cases, and the larger-|forecast| half beats the smaller half."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean signed excess move negative with t <= -2 over at least 100 cases: weekend moves continue rather than reverse."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "ordinary t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean signed excess, larger |forecast| half minus smaller half",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

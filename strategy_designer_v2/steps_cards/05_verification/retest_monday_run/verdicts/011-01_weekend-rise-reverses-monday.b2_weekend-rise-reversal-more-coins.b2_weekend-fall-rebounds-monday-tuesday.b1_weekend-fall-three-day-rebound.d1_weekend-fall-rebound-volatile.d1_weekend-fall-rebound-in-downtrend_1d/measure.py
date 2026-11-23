import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.wkend_fall_x_20d_fall.last_history_value"

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.Series(s).astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    active_total = 0
    active_ok = 0
    cases = []  # (coin, unusual, forecast)

    for coin, wins in bars.items():
        prepared = []
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            d["_ts"] = to_ts(d["timestamp"])
            close = d["close"].astype(float).values
            n = len(d)
            # normal drift grid: positions 0, H, 2H, ... inside the window
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            prepared.append(d)
        drift = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan

        for d in prepared:
            close = d["close"].astype(float).values
            n = len(d)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            sunday = (d["_ts"].dt.dayofweek == 6).values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(n, np.nan)
            # situation from prices where possible
            r1 = np.full(n, np.nan)
            r20 = np.full(n, np.nan)
            r1[1:] = close[1:] / close[:-1] - 1.0
            if n > 20:
                r20[20:] = close[20:] / close[:-20] - 1.0
            for t in range(n):
                if fc[t] == 0:
                    continue
                active_total += 1
                if np.isfinite(raw[t]):
                    falls = raw[t] > 0
                elif np.isfinite(r1[t]) and np.isfinite(r20[t]):
                    falls = (r1[t] < 0) and (r20[t] < 0)
                else:
                    falls = False
                if sunday[t] and falls and fc[t] > 0:
                    active_ok += 1
            # cases: Sunday bars with forecast > 0 (one per coin-week)
            for t in range(n):
                if sunday[t] and fc[t] > 0 and t + H < n:
                    if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0 and np.isfinite(drift):
                        ret = close[t + H] / close[t] - 1.0
                        cases.append((coin, ret - drift, float(fc[t])))

    agreement = (active_ok / active_total) if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.9
    main_name = "mean unusual 3-bar return of Sunday cases (return minus coin's normal 3-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 100 cases"
    reading = ("Situation bars are Sunday-start daily bars (next bar Monday) whose recorded raw component is > 0 "
               "(or, where unrecorded, one-bar and 20-bar price returns both negative) with forecast > 0; cases need "
               "close[t+3] inside the same window; cases equal to the median forecast are left out of both supporting groups.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "cases": int(len(cases))},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are Sunday bars with a negative one-day and "
                           "negative 20-day return held long, as the plan's Fidelity requires."),
            "reading": reading,
        }

    u = np.array([c[1] for c in cases], dtype=float)
    f = np.array([c[2] for c in cases], dtype=float)
    n_cases = int(len(u))
    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = float(np.median(f))
        hi = u[f > med]
        lo = u[f < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than the plan's minimum of 100 cases ({n_cases})."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual 3-bar return positive with t >= 2 over at least 100 cases, and the supporting check above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting check is 0 or below (or not computable)."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual 3-bar return negative with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual 3-bar return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual 3-bar return above median forecast minus below median",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }

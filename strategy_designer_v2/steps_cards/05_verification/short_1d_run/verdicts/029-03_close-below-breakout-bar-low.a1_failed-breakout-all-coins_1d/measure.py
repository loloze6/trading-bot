import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.fail_depth.last_history_value"
    POST = "debug_info.components.fail_depth.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            close = d["close"].astype(float).values
            low = d["low"].astype(float).values
            n = len(d)
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                r = raw[t]
                in_sit = np.isfinite(r) and abs(r) > 0
                if in_sit and t >= 1:
                    # price cross-check: a bar of the last 3 days has its low above today's close
                    lo = max(0, t - 3)
                    in_sit = bool(np.nanmax(low[lo:t]) > close[t])
                if in_sit and fc[t] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-signed unusual 5-bar move after short bets"
    threshold = "mean > 0 with t >= 2 over >= 30 cases (confirm); mean < 0 with t <= -2 over >= 30 cases (reject)"
    reading = ("Situation bars are those where fail_depth's raw value is non-zero and a bar of the previous 3 days has a low "
               "above the close (short side = forecast < 0); a short bet is a rise of at least 2 points in -forecast from its "
               "lowest short level since the last bet (reset to 0 when the forecast is >= 0), the first bet in each 5-bar grid "
               "cell from each window's first row is the case, drift is the coin's mean non-overlapping 5-bar return over all "
               "its windows, and depth is abs(post_pipeline_value).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are short forecasts on bars where the close "
                           "sits below a recent 20-day-breakout low, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, ret, depth)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            for t in range(0, n - H, H):
                if close[t] > 0 and np.isfinite(close[t]) and np.isfinite(close[t + H]):
                    grid_rets.append(close[t + H] / close[t] - 1.0)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            post = pd.to_numeric(d[POST], errors="coerce").values if POST in d.columns else np.full(n, np.nan)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                m = -fc[t] if fc[t] < 0 else 0.0
                if fc[t] >= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    ref = m
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n and close[t] > 0 and np.isfinite(close[t + H]):
                        ret = close[t + H] / close[t] - 1.0
                        dep = abs(post[t]) if np.isfinite(post[t]) else np.nan
                        case_rows.append((coin, ret, dep))
                else:
                    ref = min(ref, m)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    unusual = []
    depths = []
    for coin, ret, dep in case_rows:
        dr = drift.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        unusual.append(-(ret - dr))
        depths.append(dep)
    unusual = np.array(unusual, dtype=float)
    depths = np.array(depths, dtype=float)
    n_cases = int(len(unusual))

    mean = float(np.mean(unusual)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    rho = None
    ok = np.isfinite(depths) & np.isfinite(unusual)
    if ok.sum() >= 3:
        r, _ = stats.spearmanr(depths[ok], unusual[ok])
        rho = float(r) if np.isfinite(r) else None
    sup_passed = None if rho is None else bool(rho > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif tval is not None and mean > 0 and tval >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean short-signed unusual move above 0 with t >= 2 over at least 30 cases, and depth correlation above 0."
        else:
            status = "inconclusive"
            decided = "Confirm-strength mean, but the depth correlation is 0 or below (or not computable), which the plan calls inconclusive."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean short-signed unusual move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or is not computable), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman(depth abs post_pipeline_value, short-signed unusual move) > 0",
            "value": rho,
            "passed": sup_passed,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }

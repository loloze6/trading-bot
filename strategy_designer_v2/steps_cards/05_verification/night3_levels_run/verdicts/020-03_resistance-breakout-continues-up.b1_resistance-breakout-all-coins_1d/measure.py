import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.break_touches.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            close = pd.to_numeric(df["close"], errors="coerce")
            prev_close = close.shift(1)
            active = fc.notna() & (fc != 0)
            # situation: a fresh upward break of a repeatedly-turned level -> raw value > 0;
            # a cross upward (yesterday <= level < today) also implies today's close > yesterday's
            rose = (close > prev_close) | prev_close.isna()
            situ = raw.notna() & (raw > 0) & rose
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move per long case", "value": None,
                             "statistic": None, "threshold": "mean > 0 with ordinary t >= 2 over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a fresh close-break "
                           "of a swing-high level (raw break_touches > 0 with a rising close), as the plan's Fidelity requires."),
            "reading": "The situation is read as the recorded raw component being positive (a fresh break) with today's close above yesterday's, on the long side.",
        }

    # ---------- 2. criterion ----------
    case_unusual = []
    case_fc = []
    for coin, wins in bars.items():
        # coin's normal 5-bar drift: non-overlapping grid of all its windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            prepared.append((close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc in prepared:
            n = len(close)
            floor = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    floor = 0.0
                    continue
                if f - floor >= BAND:
                    floor = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                        r = close[t + H] / close[t] - 1.0
                        case_unusual.append(r - drift)
                        case_fc.append(f)
                else:
                    floor = min(floor, f)

    u = np.asarray(case_unusual, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_main = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_main = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_value, sup_t, sup_pass = None, None, None
    n_up, n_lo = 0, 0
    if n_cases > 0:
        med = float(np.median(fcs))
        up = u[fcs > med]
        lo = u[fcs <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up >= 2 and n_lo >= 2:
            sup_value = float(np.mean(up) - np.mean(lo))
            tt = stats.ttest_ind(up, lo, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_value > 0 and sup_t is not None and sup_t >= 1.0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_main is not None and mean_u > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move > 0 with t >= 2 over at least 30 cases, and the upper-minus-lower forecast half difference is positive with Welch t >= 1."
        else:
            status = "inconclusive"
            decided = "Mean unusual move > 0 with t >= 2, but the supporting check (upper minus lower half, Welch t >= 1) fails."
    elif t_main is not None and mean_u < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean unusual move < 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or is undefined), with at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "mean unusual 5-bar move per long case",
            "value": mean_u,
            "statistic": None if t_main is None else {"name": "ordinary t of the mean", "value": t_main},
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "upper minus lower half (by signal-bar forecast) mean unusual move, Welch t >= 1",
            "value": sup_value,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": ("A case is the first bet bar (forecast rise >= 2 from its floor since the last bet, floor reset to 0 when flat) "
                    "in each 5-bar grid cell counted from each window's first row, cases without 5 later bars in the window are dropped, "
                    "the drift is the coin's mean 5-bar return on that grid over all its windows, and the median split puts forecasts "
                    "above the median in the upper half and those at or below it in the lower half."),
    }

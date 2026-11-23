import numpy as np
import pandas as pd


def measure(bars):
    H = 8
    RAW = "debug_info.components.pre_fall.last_history_value"

    active_total = 0
    active_agree = 0
    case_prod = []
    case_ex = []
    case_fc = []

    for coin, wins in bars.items():
        # coin's normal 8-bar drift: non-overlapping grid of each window, pooled over all its windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(list(r[np.isfinite(r)]))
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close_hour = (ts + pd.Timedelta(hours=1)).dt.hour.values
            settle = close_hour == 16
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values

            # 2-bar return ending at this close: raw component value if recorded, else from prices
            ret2 = np.full(len(c), np.nan)
            ret2[2:] = c[2:] / c[:-2] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                fall_val = np.where(np.isfinite(raw), raw, ret2)
            else:
                fall_val = ret2
            fall = np.isfinite(fall_val) & (fall_val < 0)

            act = fc != 0
            active_total += int(act.sum())
            active_agree += int((act & settle & fall & (fc > 0)).sum())

            fwd = np.full(len(c), np.nan)
            if len(c) > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0
            cases = settle & (fc > 0) & np.isfinite(fwd)
            if np.isfinite(drift):
                ex = fwd[cases] - drift
                case_ex.extend(list(ex))
                case_fc.extend(list(fc[cases]))
                case_prod.extend(list(fc[cases] * ex))

    agreement = active_agree / active_total if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.9
    threshold = "mean > 0 with t >= 2 and supporting check passes confirms; mean < 0 with t <= -2 rejects; fewer than 300 cases inconclusive"
    mm_name = "mean of forecast x drift-removed 8-bar return, pooled"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "cases": int(len(case_prod))},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are 16:00 UTC settlement-close bars after a 2-hour fall with a long forecast, so the config does not do what the plan's Fidelity says.",
            "reading": "The settlement bar is the bar whose close (start + 1h) is 16:00 UTC, and the fall is the recorded raw 2-bar scaled return (or the price 2-bar return where not recorded) below zero.",
        }

    prod = np.array(case_prod, dtype=float)
    ex = np.array(case_ex, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n = int(len(prod))

    mean = float(np.mean(prod)) if n else None
    t = None
    if n > 1:
        sd = float(np.std(prod, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n > 0:
        med = float(np.median(fcs))
        hi = ex[fcs > med]
        lo = ex[fcs < med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi and n_lo:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n, "cases above median": n_hi, "cases below median": n_lo}

    if n < 300:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 300."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main-measure mean is > 0 with t >= 2 and the supporting check passes."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main-measure mean is < 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": mean,
            "statistic": {"name": "ordinary t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "drift-removed 8-bar return, above-median forecast minus below-median",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The settlement bar is the bar whose close (start + 1h) is 16:00 UTC, the 8-bar return is taken 8 rows ahead inside the window, the median is pooled over all cases with cases equal to it left out of both halves, and the 300-case minimum is treated as the plan's minimum count (not observable).",
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    SPREAD = "debug_info.components.sma_cross_spread.last_history_value"

    active_total = 0
    active_ok = 0
    in_rets, out_rets = [], []
    n_stretches = 0

    for coin, windows in bars.items():
        for wname, df in windows.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            spread = pd.to_numeric(df[SPREAD], errors="coerce") if SPREAD in df.columns else pd.Series(np.nan, index=df.index)

            # Situation check: active bars should be bars with SMA50 > SMA200 (raw spread > 0), long side
            act = fc.notna() & (fc != 0)
            active_total += int(act.sum())
            ok = act & spread.notna() & (spread > 0) & (fc > 0)
            active_ok += int(ok.sum())

            # Distinct up-cross stretches: contiguous runs of raw spread > 0 within the window
            pos = (spread > 0).fillna(False).astype(int).values
            if len(pos):
                starts = np.sum((pos[1:] == 1) & (pos[:-1] == 0)) + (1 if pos[0] == 1 else 0)
                n_stretches += int(starts)

            # Next-bar close-to-close return, inside the window only
            ret = close.shift(-1) / close - 1.0
            valid = ret.notna() & fc.notna()
            in_mask = valid & (fc > 0)
            out_mask = valid & (fc == 0)
            in_rets.extend(ret[in_mask].tolist())
            out_rets.extend(ret[out_mask].tolist())

    agreement = (active_ok / active_total) if active_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("In-stretch bars are bars with forecast > 0 and out-of-stretch bars those with forecast = 0, "
               "each with its next-bar return inside its own window pooled over all windows present; distinct "
               "up-cross stretches are counted as contiguous runs of the raw SMA50-SMA200 spread above zero in each "
               "window (a run already under way at the window's start counts as one); the supporting check passes "
               "when the up-share difference is positive; the plan's minimum counts, when unmet, give 'not observable'.")

    threshold = "confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "in-stretch minus out-of-stretch mean next-bar return",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"in-stretch bars": len(in_rets), "out-of-stretch bars": len(out_rets),
                       "up-cross stretches": n_stretches},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 50-day SMA "
                           "is above the 200-day SMA, so the config's forecast does not follow the plan's cross-to-cross stretch."),
            "reading": reading,
        }

    a = np.asarray(in_rets, dtype=float)
    b = np.asarray(out_rets, dtype=float)
    n_in, n_out = len(a), len(b)

    diff = float(a.mean() - b.mean()) if n_in > 0 and n_out > 0 else None
    t = None
    if n_in >= 2 and n_out >= 2:
        tt = stats.ttest_ind(a, b, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    up_diff = float(np.mean(a > 0) - np.mean(b > 0)) if n_in > 0 and n_out > 0 else None
    sup = {"name": "share of up next-bars in-stretch minus out-of-stretch",
           "value": up_diff, "passed": (None if up_diff is None else bool(up_diff > 0))}

    counts = {"in-stretch bars": n_in, "out-of-stretch bars": n_out, "up-cross stretches": n_stretches}

    short = []
    if n_in < 100:
        short.append(f"in-stretch bars {n_in} < 100")
    if n_out < 100:
        short.append(f"out-of-stretch bars {n_out} < 100")
    if n_stretches < 3:
        short.append(f"up-cross stretches {n_stretches} < 3")

    if short:
        status = "not observable"
        decided_by = "The plan's minimum counts are not reached: " + "; ".join(short) + "."
    elif t is None or diff is None:
        status = "inconclusive"
        decided_by = "The Welch t could not be computed, so |t| < 2 cannot be ruled out and the result is inconclusive."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided_by = "The in-stretch minus out-of-stretch mean next-bar return is positive with Welch t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided_by = "The in-stretch minus out-of-stretch mean next-bar return is negative with Welch t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The Welch t has |t| < 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "in-stretch minus out-of-stretch mean next-bar return",
                         "value": diff,
                         "statistic": (None if t is None else {"name": "Welch t", "value": t}),
                         "threshold": threshold},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }

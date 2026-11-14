import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    ret_col = "close"
    act_rets, act_fc, all_rets = [], [], []
    window_excess = {}

    for coin, windows in bars.items():
        for w, df in windows.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d[ret_col], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # next-bar return, inside this window only
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            base_mask = nxt.notna()
            act_mask = base_mask & fc.notna() & (fc < 0)

            w_all = nxt[base_mask].values
            w_act = nxt[act_mask].values
            all_rets.extend(w_all.tolist())
            act_rets.extend(w_act.tolist())
            act_fc.extend(fc[act_mask].values.tolist())

            key = f"{coin}:{w}"
            if len(w_act) > 0 and len(w_all) > 0:
                window_excess[key] = float(np.mean(w_act) - np.mean(w_all))
            else:
                window_excess[key] = None

    act_rets = np.asarray(act_rets, dtype=float)
    act_fc = np.asarray(act_fc, dtype=float)
    all_rets = np.asarray(all_rets, dtype=float)
    n = int(len(act_rets))

    excess, t = None, None
    if n > 0 and len(all_rets) > 0:
        base_mean = float(np.mean(all_rets))
        excess = float(np.mean(act_rets) - base_mean)
        if n > 1:
            sd = float(np.std(act_rets, ddof=1))
            if sd > 0:
                t = float(excess / (sd / np.sqrt(n)))

    neg_windows = int(sum(1 for v in window_excess.values() if v is not None and v < 0))

    # Supporting check: slope of next-bar return on forecast across active bars
    slope, passed = None, None
    if n >= 3 and np.ptp(act_fc) > 0:
        lr = stats.linregress(act_fc, act_rets)
        slope = float(lr.slope)
        passed = bool(slope > 0)

    if n < 60:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 60 active bars across the windows."
    elif excess is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the excess return could not be computed."
    elif excess >= 0:
        status = "rejected"
        decided_by = "Reject: the excess return is zero or positive with at least 60 active bars."
    elif t is not None and t <= -2 and neg_windows >= 4:
        status = "confirmed"
        decided_by = "Confirm: the excess return is negative with t <= -2 over at least 60 active bars and negative in at least 4 of the 6 windows."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the excess return is negative but t is between -2 and 0 or it is negative in fewer than 4 windows."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return after active bars minus mean next-bar return over all bars",
            "value": excess,
            "threshold": "negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows to confirm; zero or positive to reject",
        },
        "supporting_check": {
            "name": "slope of next-bar return on forecast across active bars (positive expected)",
            "value": slope,
            "passed": passed,
        },
        "cases": n,
        "decided_by": decided_by,
        "reading": (
            "Active bars are the bars with a negative forecast. Excess return is pooled across all windows. "
            "Its t is (mean of active returns minus the all-bar mean) divided by the standard error of the active returns. "
            "A window counts as negative if its own active-minus-all mean is below zero, and a window with no active bars is not negative. "
            "The slope regresses the next-bar return on the signed forecast, so a positive slope means larger shorts were followed by larger falls."
        ),
        "details": {
            "t_stat": t,
            "negative_windows": neg_windows,
            "window_excess": window_excess,
            "all_bars": int(len(all_rets)),
        },
    }

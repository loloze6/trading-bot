import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    act_all, base_all, act_fc = [], [], []
    window_excess = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            r = close.shift(-1) / close - 1.0  # next-bar return, inside this window only
            # horizon 1 bar: grid positions 0,1,2,... -> every bar with a next bar
            base_mask = r.notna()
            act_mask = base_mask & fc.notna() & (fc < 0)
            b = r[base_mask].to_numpy(dtype=float)
            a = r[act_mask].to_numpy(dtype=float)
            base_all.extend(b.tolist())
            act_all.extend(a.tolist())
            act_fc.extend(fc[act_mask].to_numpy(dtype=float).tolist())
            if len(a) > 0 and len(b) > 0:
                window_excess[f"{coin}:{w}"] = float(a.mean() - b.mean())

    act = np.array(act_all, dtype=float)
    base = np.array(base_all, dtype=float)
    fcs = np.array(act_fc, dtype=float)
    n_act = int(len(act))
    n_base = int(len(base))

    excess = None
    t = None
    if n_act >= 1 and n_base >= 1:
        excess = float(act.mean() - base.mean())
    if n_act >= 2 and n_base >= 2:
        tt = stats.ttest_ind(act, base, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    neg_windows = int(sum(1 for v in window_excess.values() if v < 0))

    slope = None
    passed = None
    if n_act >= 3 and np.ptp(fcs) > 0:
        slope = float(stats.linregress(fcs, act).slope)
        passed = bool(slope > 0)

    if n_act < 60 or excess is None:
        status = "inconclusive"
        decided = "Fewer than 60 active bars across the windows, so the result is inconclusive."
    elif excess >= 0:
        status = "rejected"
        decided = "The excess return is zero or positive with at least 60 active bars, so the idea is rejected."
    elif t is not None and t <= -2 and neg_windows >= 4:
        status = "confirmed"
        decided = "The excess return is negative with t <= -2 over at least 60 active bars and negative in at least 4 of the 6 windows."
    else:
        status = "inconclusive"
        decided = "The excess return is negative but t is between -2 and 0 or it is negative in fewer than 4 windows, so the result is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return after active bars minus mean next-bar return over all bars",
            "value": excess,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "excess negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows",
        },
        "supporting_check": {
            "name": "slope of next-bar return on signed forecast across active bars (should be positive)",
            "value": slope,
            "passed": passed,
        },
        "counts": {
            "active bars": n_act,
            "all bars": n_base,
            "windows with negative excess": neg_windows,
            "windows with active bars": int(len(window_excess)),
        },
        "decided_by": decided,
        "reading": "Active bars are bars with a negative forecast; every bar with a next close in its window is used (horizon 1, so no overlap) and the Welch t compares active against all-bar next returns; a window counts as negative when its active-minus-all mean is below zero, and windows with no active bars do not count; the supporting slope regresses next-bar return on the signed forecast, so a larger short followed by a larger fall gives a positive slope, and it does not change the status.",
    }

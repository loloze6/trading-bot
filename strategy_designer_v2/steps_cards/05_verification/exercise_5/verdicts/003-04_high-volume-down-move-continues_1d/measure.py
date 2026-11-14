import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    act_rets, all_rets, act_fc = [], [], []
    window_excess = {}
    n_windows_present = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            n_windows_present += 1
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # next-bar return within this window only
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            regime = d["regime"].astype(str)

            valid = nxt.notna()
            all_w = nxt[valid].to_numpy(dtype=float)
            is_act = valid & (regime == "trending") & fc.notna()
            act_w = nxt[is_act].to_numpy(dtype=float)
            fc_w = fc[is_act].to_numpy(dtype=float)

            all_rets.extend(all_w.tolist())
            act_rets.extend(act_w.tolist())
            act_fc.extend(fc_w.tolist())

            if len(act_w) > 0 and len(all_w) > 0:
                window_excess[f"{coin}:{w}"] = float(np.mean(act_w) - np.mean(all_w))
            else:
                window_excess[f"{coin}:{w}"] = None

    act = np.array(act_rets, dtype=float)
    allr = np.array(all_rets, dtype=float)
    fcs = np.array(act_fc, dtype=float)
    n_act = int(len(act))
    n_neg_windows = int(sum(1 for v in window_excess.values() if v is not None and v < 0))

    excess = None
    t_val = None
    if n_act >= 1 and len(allr) >= 1:
        excess = float(np.mean(act) - np.mean(allr))
    if n_act >= 2 and len(allr) >= 2:
        t_res = stats.ttest_ind(act, allr, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    slope = None
    passed = None
    if n_act >= 3 and np.ptp(fcs) > 0:
        lr = stats.linregress(fcs, act)
        slope = float(lr.slope)
        passed = bool(slope > 0)

    if n_act < 60 or excess is None:
        status = "inconclusive"
        decided = "Fewer than 60 active bars across the windows, so the result is inconclusive."
    elif excess >= 0:
        status = "rejected"
        decided = "The excess return is zero or positive with at least 60 active bars, so the idea is rejected."
    elif t_val is not None and t_val <= -2 and n_neg_windows >= 4:
        status = "confirmed"
        decided = "The excess return is negative with t <= -2 over at least 60 active bars and negative in at least 4 of the 6 windows, so the idea is confirmed."
    else:
        status = "inconclusive"
        decided = "The excess return is negative but t is above -2 or it is negative in fewer than 4 windows, so the result is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return after active bars minus mean next-bar return over all bars",
            "value": excess,
            "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
            "threshold": "negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows",
        },
        "supporting_check": {
            "name": "slope of next-bar return on forecast across active bars (should be positive)",
            "value": slope,
            "passed": passed,
        },
        "counts": {
            "active bars": n_act,
            "windows with negative excess return": n_neg_windows,
            "windows": n_windows_present,
        },
        "decided_by": decided,
        "reading": "Active bars are rows labelled regime 'trending' with a next bar inside the same window, the baseline is every bar with a next-bar return in the same windows (horizon 1, so every bar is on the grid), the t is Welch's between the two groups, a window without active bars does not count as negative, and the supporting slope regresses next-bar return on the signed forecast so a positive slope means a larger short precedes a larger fall.",
    }

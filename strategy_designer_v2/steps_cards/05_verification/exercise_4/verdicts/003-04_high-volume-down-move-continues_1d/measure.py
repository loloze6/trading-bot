import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    act_rets, act_fc, all_rets = [], [], []
    per_window = {}

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values if "forecast" in df.columns else np.full(len(df), np.nan)
            if "regime" in df.columns:
                regime = df["regime"].astype(str).values
            else:
                regime = np.array([""] * len(df))

            # horizon 1 bar: positions 0,1,2,... ; next-bar return inside the window
            nxt = np.full(len(df), np.nan)
            nxt[:-1] = close[1:] / close[:-1] - 1.0

            w_act, w_all = [], []
            for i in range(len(df) - 1):
                r = nxt[i]
                if not np.isfinite(r):
                    continue
                w_all.append(r)
                all_rets.append(r)
                if regime[i] == "trending":
                    w_act.append(r)
                    act_rets.append(r)
                    act_fc.append(fc[i])

            key = f"{coin}:{window}"
            if len(w_act) > 0 and len(w_all) > 0:
                per_window[key] = float(np.mean(w_act) - np.mean(w_all))
            else:
                per_window[key] = None

    act = np.asarray(act_rets, dtype=float)
    allr = np.asarray(all_rets, dtype=float)
    n_act = int(len(act))
    n_all = int(len(allr))

    excess = None
    t_val = None
    if n_act > 0 and n_all > 0:
        excess = float(np.mean(act) - np.mean(allr))
    if n_act >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(act, allr, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    neg_windows = int(sum(1 for v in per_window.values() if v is not None and v < 0))

    # supporting check: slope of next-bar return on (signed) forecast across active bars
    slope = None
    passed = None
    fc_arr = np.asarray(act_fc, dtype=float)
    mask = np.isfinite(fc_arr) & np.isfinite(act) if n_act > 0 else np.array([], dtype=bool)
    if mask.sum() >= 3 and np.std(fc_arr[mask]) > 0:
        lr = stats.linregress(fc_arr[mask], act[mask])
        slope = float(lr.slope)
        passed = bool(slope > 0)

    if n_act < 60:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 60 active bars across the 6 windows."
    elif excess is not None and excess >= 0:
        status = "rejected"
        decided_by = "Reject: the excess return is zero or positive with at least 60 active bars."
    elif excess is not None and excess < 0 and t_val is not None and t_val <= -2 and neg_windows >= 4:
        status = "confirmed"
        decided_by = "Confirm: the excess return is negative with t <= -2 over at least 60 active bars and negative in at least 4 of the 6 windows."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: a negative excess return with t between -2 and 0, or negative in fewer than 4 windows."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return after active bars minus mean next-bar return over all bars",
            "value": excess,
            "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
            "threshold": "excess negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows",
        },
        "supporting_check": {
            "name": "slope of next-bar return on forecast across active bars (should be positive)",
            "value": slope,
            "passed": passed,
        },
        "counts": {
            "active bars": n_act,
            "all bars": n_all,
            "windows with negative excess": neg_windows,
            "windows": int(len(per_window)),
        },
        "decided_by": decided_by,
        "reading": "Active bars are rows whose regime label is 'trending' (the veto's heavy-volume down-day regime), every bar with a next close in its window counts once as the all-bars baseline, the per-window rule counts windows whose active-minus-all mean is below zero (windows without active bars count as not negative), and 'forecast size' is the signed forecast so a positive slope means larger shorts precede larger falls.",
    }

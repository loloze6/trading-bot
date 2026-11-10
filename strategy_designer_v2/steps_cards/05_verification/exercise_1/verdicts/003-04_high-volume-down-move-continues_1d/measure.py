import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    act_rets, act_fc, all_rets = [], [], []
    window_excess = {}

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # next-bar return inside this window only
            if "regime" in d.columns:
                reg = d["regime"].astype(str)
            else:
                reg = d["debug_info.regime"].astype(str)
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            valid_all = nxt.notna()
            all_r = nxt[valid_all].values
            active = (reg == "trending") & nxt.notna()
            a_r = nxt[active].values
            a_f = fc[active].values

            all_rets.extend(all_r.tolist())
            act_rets.extend(a_r.tolist())
            act_fc.extend(a_f.tolist())

            key = f"{coin}:{w}"
            if len(a_r) > 0 and len(all_r) > 0:
                window_excess[key] = float(np.mean(a_r) - np.mean(all_r))
            else:
                window_excess[key] = None

    act_rets = np.array(act_rets, dtype=float)
    act_fc = np.array(act_fc, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    n_act = int(len(act_rets))

    excess = None
    t_stat = None
    if n_act > 0 and len(all_rets) > 0:
        excess = float(np.mean(act_rets) - np.mean(all_rets))
        if n_act > 1:
            sd = float(np.std(act_rets, ddof=1))
            if sd > 0:
                t_stat = float(excess / (sd / np.sqrt(n_act)))

    neg_windows = int(sum(1 for v in window_excess.values() if v is not None and v < 0))

    # Supporting check: slope of next-bar return on (signed) forecast over active bars
    slope = None
    passed = None
    m = ~np.isnan(act_fc) & ~np.isnan(act_rets)
    if m.sum() >= 3 and np.std(act_fc[m]) > 0:
        res = stats.linregress(act_fc[m], act_rets[m])
        slope = float(res.slope)
        passed = bool(slope > 0)

    if n_act < 60:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 60 active bars across the windows."
    elif excess is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the excess return could not be computed."
    elif excess >= 0:
        status = "rejected"
        decided_by = "Reject: the excess return is zero or positive with at least 60 active bars."
    elif t_stat is not None and t_stat <= -2 and neg_windows >= 4:
        status = "confirmed"
        decided_by = ("Confirm: the excess return is negative with t <= -2 over at least 60 active bars "
                      "and negative in at least 4 of the 6 windows.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the excess return is negative but t is between -2 and 0 "
                      "or it is negative in fewer than 4 windows.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return on active bars minus mean next-bar return on all bars",
            "value": excess,
            "threshold": "negative with t <= -2 over >= 60 active bars and negative in >= 4 of 6 windows",
        },
        "supporting_check": {
            "name": "slope of next-bar return on signed forecast over active bars (should be positive)",
            "value": slope,
            "passed": passed,
        },
        "cases": n_act,
        "decided_by": decided_by,
        "reading": ("Active bars are rows whose regime is 'trending' (the veto's heavy-volume down days), pooled "
                    "across windows against all bars with a next-bar return; t is the excess divided by the active "
                    "bars' standard error (sd/sqrt(n)); a window counts as negative only if it has active bars and "
                    "a negative excess; the slope uses the signed forecast so a positive slope means larger shorts "
                    "precede larger falls; t = " + (f"{t_stat:.3f}" if t_stat is not None else "n/a")
                    + f", negative windows = {neg_windows}."),
    }

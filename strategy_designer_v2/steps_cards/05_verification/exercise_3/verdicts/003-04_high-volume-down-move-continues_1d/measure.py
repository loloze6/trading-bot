import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 1
    act_rets, act_fc, all_rets = [], [], []
    window_excess = {}
    n_windows_total = 0

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            n_windows_total += 1
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            nxt = close.shift(-H) / close - 1.0  # inside this window only
            grid = np.arange(0, len(df), H)
            w_all, w_act = [], []
            for i in grid:
                r = nxt.iloc[i]
                if pd.isna(r):
                    continue
                w_all.append(float(r))
                f = fc.iloc[i]
                if pd.notna(f) and f != 0:
                    w_act.append(float(r))
                    act_rets.append(float(r))
                    act_fc.append(float(f))
            all_rets.extend(w_all)
            key = f"{coin}:{win}"
            if len(w_act) > 0 and len(w_all) > 0:
                window_excess[key] = float(np.mean(w_act) - np.mean(w_all))
            else:
                window_excess[key] = None

    n_active = len(act_rets)
    n_all = len(all_rets)
    neg_windows = sum(1 for v in window_excess.values() if v is not None and v < 0)

    excess, t_val = None, None
    if n_active > 0 and n_all > 0:
        excess = float(np.mean(act_rets) - np.mean(all_rets))
    if n_active >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(act_rets, all_rets, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    slope, passed = None, None
    if n_active >= 3 and np.std(act_fc) > 0:
        lr = stats.linregress(np.array(act_fc), np.array(act_rets))
        slope = float(lr.slope)
        passed = bool(slope > 0)

    if n_active < 60 or excess is None:
        status = "inconclusive"
        decided = "Fewer than 60 active bars across the windows, so the result is inconclusive."
    elif excess >= 0:
        status = "rejected"
        decided = "The excess return is zero or positive with at least 60 active bars, so the idea is rejected."
    elif t_val is not None and t_val <= -2 and neg_windows >= 4:
        status = "confirmed"
        decided = "The excess return is negative with t <= -2 over at least 60 active bars and negative in at least 4 of the 6 windows."
    else:
        status = "inconclusive"
        decided = "The excess return is negative but t is above -2 or it is negative in fewer than 4 windows, so the result is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return on active bars minus mean next-bar return on all bars",
            "value": excess,
            "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
            "threshold": "excess < 0 with t <= -2 over at least 60 active bars, negative in at least 4 of 6 windows",
        },
        "supporting_check": {
            "name": "slope of next-bar return on signed forecast across active bars (should be positive)",
            "value": slope,
            "passed": passed,
        },
        "counts": {
            "active bars": n_active,
            "all bars": n_all,
            "windows with negative excess": neg_windows,
            "windows": n_windows_total,
        },
        "decided_by": decided,
        "reading": "Active bars are rows with a non-zero, non-missing forecast; the baseline is all bars with a next-bar return in the same windows; the Welch t compares active bars against all bars; per-window excess is active minus all within each window (windows without active bars count as not negative); and the slope regresses next-bar return on the signed forecast so that a positive slope means larger shorts precede larger falls.",
    }

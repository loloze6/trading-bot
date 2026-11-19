import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 168
    M30 = 720
    WEEK = "debug_info.components.week.last_history_value"

    # ---------- 1. Situation check: m30 (720-bar return) > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            m30 = np.full(len(d), np.nan)
            if len(d) > M30:
                m30[M30:] = close[M30:] / close[:-M30] - 1.0
            active = np.isfinite(fc) & (fc != 0) & np.isfinite(m30)
            n_active += int(active.sum())
            n_agree += int((active & (m30 > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of excess forward 168-bar return on raw 7-day return, trending grid bars"
    thr = "confirm if slope t >= 2 (and supporting difference > 0); reject if t <= -2"
    reading = ("The 720-bar return is recomputed from closes inside each window (bars without 720 prior bars "
               "in the window are left out of the agreement); trending = regime column 'trending'; a coin's mean "
               "168-bar return is the mean of its non-overlapping grid forward returns over all windows and all bars; "
               "the minimum counts are applied to grid cases with a forward return and a raw week value.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active forecast bars are bars where the 720-bar return is "
                           "positive with a long forecast, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_fwd = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            idx = np.arange(0, n, H)
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            fwd = close[idx + H] / close[idx] - 1.0
            all_fwd.extend(list(fwd))
            week = d[WEEK].astype(float).values if WEEK in d.columns else np.full(n, np.nan)
            reg = d["regime"].astype(str).values
            fc = d["forecast"].astype(float).values
            for k, i in enumerate(idx):
                rows.append((coin, reg[i], week[i], fc[i], fwd[k]))
        all_fwd = np.array(all_fwd, dtype=float)
        all_fwd = all_fwd[np.isfinite(all_fwd)]
        coin_means[coin] = float(all_fwd.mean()) if len(all_fwd) else np.nan

    g = pd.DataFrame(rows, columns=["coin", "regime", "week", "fc", "fwd"])
    g = g[g["regime"] == "trending"].copy()
    g["excess"] = g["fwd"] - g["coin"].map(coin_means)
    g = g.dropna(subset=["week", "fc", "excess"])
    g = g[np.isfinite(g["week"]) & np.isfinite(g["excess"]) & np.isfinite(g["fc"])]

    n_cases = int(len(g))
    pos = g[g["fc"] > 0]["excess"]
    zero = g[g["fc"] == 0]["excess"]
    n_pos, n_zero = int(len(pos)), int(len(zero))
    counts = {"trending grid cases": n_cases,
              "forecast > 0 cases": n_pos,
              "forecast = 0 cases": n_zero}

    slope, t = None, None
    if n_cases >= 3 and g["week"].std() > 0:
        lr = stats.linregress(g["week"].values, g["excess"].values)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    diff = float(pos.mean() - zero.mean()) if (n_pos > 0 and n_zero > 0) else None
    sup_pass = (diff > 0) if diff is not None else None

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": "mean excess forward return, forecast > 0 minus forecast = 0",
           "value": diff, "passed": sup_pass}

    if n_cases < 100 or n_pos < 30 or n_zero < 30 or t is None:
        status = "not observable"
        decided = ("A minimum count is not reached: the plan needs at least 100 trending grid cases and "
                   "at least 30 on each side of the forecast-zero split (or the slope t could not be computed).")
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting difference is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting difference is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

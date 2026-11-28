import numpy as np
import pandas as pd
from scipy import stats


def _get_component(df, comp_id, field):
    col = "debug_info.components.%s.%s" % (comp_id, field)
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" in df.columns:
        vals = df["debug_info.components"].tolist()
        for i, v in enumerate(vals):
            try:
                if isinstance(v, dict) and comp_id in v and isinstance(v[comp_id], dict):
                    x = v[comp_id].get(field)
                    if x is not None:
                        out[i] = float(x)
            except Exception:
                pass
    return out


def measure(bars):
    H = 3
    BAND = 2.0

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    per_window = []  # (coin, window, df prepared)
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            brk = np.full(n, np.nan)  # 1 break, 0 not, nan undeterminable
            for t in range(3, n):
                c0, c1, c2, c3 = close[t], close[t - 1], close[t - 2], close[t - 3]
                if np.any(np.isnan([c0, c1, c2, c3])):
                    continue
                brk[t] = 1.0 if (c0 > c1 and c1 < c2 and c2 < c3) else 0.0
            for t in range(n):
                if fc[t] != 0 and not np.isnan(brk[t]):
                    n_active += 1
                    if brk[t] == 1.0 and fc[t] > 0:
                        n_agree += 1
            per_window.append((coin, win, df, close, fc))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Break bars are recomputed from closes inside each window (an up close after at least two strict down "
               "closes), bars without three prior closes in the window are left out of the agreement, and the profile "
               "vetoes (365-bar volatility percentile) cannot be rebuilt from the recorded bars so only the break and "
               "the long side are checked; a case is the first bet in each 3-bar grid cell (positions 0,3,6,... of its "
               "window), the drift is the coin's mean non-overlapping 3-bar return over all its windows, the mean's t "
               "clusters cases by UTC day (deviations summed per day, G/(G-1) correction), the slope's t is the "
               "ordinary least-squares t, and fewer than 30 cases or 30 days gives 'not observable'.")

    main_name = "mean unusual 3-bar move of the cases (long)"
    main_thr = "mean > 0 with day-clustered t >= 2 to confirm; t <= -2 to reject"
    sup_name = "OLS slope of unusual move on post_pipeline_value of upday"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Only %.1f%% of the bars with a non-zero forecast are long on an up close breaking a run of "
                           "2+ down closes, below the 90%% the plan's situation requires." % (100 * agreement)),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin in set(p[0] for p in per_window):
        rets = []
        for (c, w, df, close, fc) in per_window:
            if c != coin:
                continue
            n = len(close)
            for t in range(0, n - H, H):
                if not (np.isnan(close[t]) or np.isnan(close[t + H])) and close[t] > 0:
                    rets.append(close[t + H] / close[t] - 1.0)
        drift[coin] = float(np.mean(rets)) if len(rets) > 0 else np.nan

    # ---------- cases ----------
    cases = []  # (day, unusual, ppv)
    for (coin, win, df, close, fc) in per_window:
        n = len(close)
        ppv = _get_component(df, "upday", "post_pipeline_value")
        ref = 0.0
        bet = np.zeros(n, dtype=bool)
        for t in range(n):
            f = fc[t]
            if f <= 0:
                ref = 0.0
                continue
            if f - ref >= BAND:
                bet[t] = True
                ref = f
            else:
                ref = min(ref, f)
        used_cells = set()
        for t in range(n):
            if not bet[t]:
                continue
            cell = t // H
            if cell in used_cells:
                continue
            used_cells.add(cell)
            if t + H >= n:
                continue
            if np.isnan(close[t]) or np.isnan(close[t + H]) or close[t] <= 0 or np.isnan(drift[coin]):
                continue
            r = close[t + H] / close[t] - 1.0
            day = df["timestamp"].iloc[t].floor("D")
            cases.append((day, r - drift[coin], ppv[t]))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_val = None
    t_mean = None
    slope = None
    t_slope = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases], dtype=float)
        mean_val = float(np.mean(x))
        if n_cases > 1 and n_days > 1:
            dev = x - mean_val
            dser = pd.Series(dev).groupby([c[0] for c in cases]).sum().to_numpy()
            G = len(dser)
            var = (G / (G - 1.0)) * np.sum(dser ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_mean = float(mean_val / se) if se > 0 else None
        pv = np.array([c[2] for c in cases], dtype=float)
        ok = ~np.isnan(pv) & ~np.isnan(x)
        if ok.sum() >= 3 and np.std(pv[ok]) > 0:
            lr = stats.linregress(pv[ok], x[ok])
            slope = float(lr.slope)
            t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_passed = None if t_slope is None else bool(slope > 0 and t_slope >= 1)
    result = {
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_val,
                         "statistic": None if t_mean is None else {"name": "t of the mean, cases clustered by day",
                                                                   "value": t_mean},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": sup_passed,
                             "t": t_slope},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 30 or n_days < 30:
        result["status"] = "not observable"
        result["decided_by"] = ("The plan's minimum of 30 cases over 30 distinct days is not reached (%d cases, %d days)."
                                % (n_cases, n_days))
        return result

    if t_mean is not None and mean_val > 0 and t_mean >= 2 and sup_passed:
        result["status"] = "confirmed"
        result["decided_by"] = "Confirm: the mean unusual move is above 0 with t >= 2 and the slope is positive with t >= 1."
    elif (t_mean is not None and t_mean <= -2) or (t_slope is not None and t_slope <= -2):
        result["status"] = "rejected"
        result["decided_by"] = "Reject: the mean unusual move has t <= -2 or the slope has t <= -2."
    else:
        result["status"] = "inconclusive"
        if t_mean is not None and t_mean >= 2:
            result["decided_by"] = "Inconclusive: the mean t is >= 2 but the slope is not positive with t >= 1."
        else:
            result["decided_by"] = "Inconclusive: the mean t lies between -2 and 2 and the slope t is above -2."
    return result

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 28
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            situ = raw.notna() & (raw > 0)
            side_ok = fc > 0
            n_active += int(active.sum())
            n_agree += int((active & situ & side_ok).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars after a positive scaled "
                           "7-day rise with a long forecast (or there are no active bars), so the config does not "
                           "trade the plan's situation on its side."),
            "reading": "The situation is a positive raw scaled 7-day rise (last_history_value > 0) and the side is long (forecast > 0).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                coin_cells.append((r, fc[t], ts.iloc[t].floor("D")))
        if not coin_rets:
            continue
        drift = float(np.mean(coin_rets))
        for r, f, d in coin_cells:
            if np.isfinite(f) and f > 0:
                rows.append({"coin": coin, "day": d, "f": float(f), "ex": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases with a positive forecast": n_cases, "distinct days": n_days}

    main_name = "forecast-weighted mean 28-bar excess return (over the coin's normal 28-bar drift)"
    main_thr = "t >= 2 with a positive mean to confirm; t <= -2 to reject"
    sup_name = "upper-half minus lower-half mean excess return at the median forecast"
    reading = ("The 28-bar grid starts at each window's first row with the forward return inside the window; the drift is "
               "the coin's mean grid 28-bar return over all its windows; the day-clustered t of the weighted mean is "
               "m / (sqrt(G/(G-1) * sum over days of (sum of w*(e-m))^2) / sum w); the upper half is forecast above the "
               "median, the lower half at or below it, compared by unweighted means; the plan's minimum of 30 cases on "
               "30 days, when not reached, gives 'not observable'.")

    if n_cases < 30 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases with a positive forecast on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    w = cases["f"].to_numpy()
    e = cases["ex"].to_numpy()
    m = float(np.sum(w * e) / np.sum(w))
    cases["u"] = w * (e - m)
    per_day = cases.groupby("day")["u"].sum().to_numpy()
    G = len(per_day)
    var = (G / (G - 1)) * np.sum(per_day ** 2) / (np.sum(w) ** 2) if G > 1 else np.nan
    se = float(np.sqrt(var)) if np.isfinite(var) else np.nan
    t_main = float(m / se) if (np.isfinite(se) and se > 0) else None

    med = float(np.median(w))
    up = e[w > med]
    lo = e[w <= med]
    if len(up) >= 2 and len(lo) >= 2:
        diff = float(np.mean(up) - np.mean(lo))
        wt = stats.ttest_ind(up, lo, equal_var=False)
        t_w = float(wt.statistic) if np.isfinite(wt.statistic) else None
    elif len(up) >= 1 and len(lo) >= 1:
        diff = float(np.mean(up) - np.mean(lo))
        t_w = None
    else:
        diff, t_w = None, None
    counts["upper half cases"] = int(len(up))
    counts["lower half cases"] = int(len(lo))

    sup_pass = bool(diff is not None and diff > 0)

    if (t_main is not None and t_main <= -2) or (t_w is not None and t_w <= -2):
        status = "rejected"
        decided = ("Reject rule met: the weighted mean excess return has t <= -2, or the upper-minus-lower "
                   "difference has a Welch t <= -2.")
    elif t_main is not None and m > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = ("Confirm rule met: the weighted mean excess return is positive with t >= 2 and the "
                   "upper-minus-lower difference is above 0.")
    else:
        status = "inconclusive"
        if t_main is not None and m > 0 and t_main >= 2 and not sup_pass:
            decided = ("The main measure meets the confirm rule but the upper-minus-lower difference is not above 0, "
                       "so the result is inconclusive.")
        else:
            decided = "Neither rule met: the main t is between -2 and 2 (or undefined) and no reject condition holds."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": ({"name": "t of the weighted mean, cases of one day taken together", "value": t_main}
                          if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name + (f" (Welch t = {t_w:.3f})" if t_w is not None else " (Welch t undefined)"),
            "value": diff,
            "passed": sup_pass if diff is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

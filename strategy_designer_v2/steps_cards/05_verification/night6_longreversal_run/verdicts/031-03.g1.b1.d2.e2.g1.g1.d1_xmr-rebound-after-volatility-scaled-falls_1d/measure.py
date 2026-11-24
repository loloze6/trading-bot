import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- collect per-window data ----------
    all_next_rets = []
    rows = []  # (forecast, next_ret)
    n_active = 0
    n_agree = 0
    n_pos_forecast_total = 0

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            next_ret = close.shift(-1) / close - 1.0  # inside this window only
            prev_ret = close / close.shift(1) - 1.0

            # coin's mean daily return over all windows (every 1-bar return)
            all_next_rets.append(next_ret.dropna().values)

            # ---------- situation check ----------
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float)
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: the day's return is a fall (raw value = return / mean vol, so its sign is the return's sign);
            # where the raw value is missing, fall back to the price return
            fall = raw.where(raw.notna(), prev_ret) < 0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fall.fillna(False) & (fc > 0)).sum())

            pos = fc > 0
            n_pos_forecast_total += int(pos.sum())
            sel = pos & next_ret.notna()
            for f, r in zip(fc[sel].values, next_ret[sel].values):
                rows.append((float(f), float(r)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted mean next-day excess return over XMR's mean daily return (bars with forecast > 0)"
    threshold = "confirm: > 0 with t >= 2 (and top-third minus bottom-third > 0); reject: < 0 with t <= -2"
    sup_name = "mean next-day excess return, top third by forecast minus bottom third"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": n_pos_forecast_total, "active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are one-day falls (raw scaled return < 0) with a long "
                           "forecast, so the config does not trade the plan's situation on its side."
                           if n_active > 0 else "No active bars: the config never takes the plan's position."),
            "reading": "The situation is a bar whose raw component value (day's return over mean 30-day vol) is "
                       "negative, the expected side long.",
        }

    allr = np.concatenate(all_next_rets) if all_next_rets else np.array([])
    mu = float(np.mean(allr)) if allr.size else np.nan

    n = len(rows)
    counts = {"bars with forecast > 0": n, "bars with forecast > 0 (incl. without next-day return)": n_pos_forecast_total}
    reading = ("Bars with forecast > 0 counted are those with a next-day return inside their window; the coin's mean "
               "daily return is the mean of all 1-bar returns over all windows; the t of the weighted mean uses the "
               "weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); thirds are the floor(n/3) lowest "
               "and highest forecasts (stable sort); fewer than 100 such bars is reported as not observable.")

    if n < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 100 bars with forecast > 0 is not reached.",
            "reading": reading,
        }

    f = np.array([r[0] for r in rows], dtype=float)
    x = np.array([r[1] for r in rows], dtype=float) - mu

    sw = float(np.sum(f))
    wmean = float(np.sum(f * x) / sw)
    se = float(np.sqrt(n / (n - 1.0) * np.sum((f ** 2) * (x - wmean) ** 2)) / sw)
    t = float(wmean / se) if se > 0 else (0.0 if wmean == 0 else float(np.sign(wmean) * np.inf))

    order = np.argsort(f, kind="mergesort")
    k = n // 3
    bottom = x[order[:k]]
    top = x[order[n - k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else None
    sup_passed = bool(diff is not None and diff > 0)

    if wmean > 0 and t >= 2 and sup_passed:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is > 0 with t >= 2 and the top-third minus bottom-third difference is > 0."
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is < 0 with t <= -2."
    elif wmean > 0 and t >= 2 and not sup_passed:
        status = "inconclusive"
        decided = "The main measure meets the confirm rule but the top-third minus bottom-third difference is not above 0."
    else:
        status = "inconclusive"
        decided = "The t of the forecast-weighted mean excess return lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": wmean,
                         "statistic": {"name": "t of the forecast-weighted mean", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

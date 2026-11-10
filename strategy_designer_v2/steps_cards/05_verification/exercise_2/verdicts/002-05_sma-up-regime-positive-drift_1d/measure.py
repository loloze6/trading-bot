import numpy as np
import pandas as pd


def measure(bars):
    in_rets = []
    all_rets = []
    n_stretches = 0

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # next-bar return inside this window only
            nxt = close.shift(-1) / close - 1.0

            # all-bar sample (buy-and-hold over same bars)
            valid_all = nxt.notna()
            all_rets.append(nxt[valid_all].values)

            # in-stretch sample: forecast > 0 and a next-bar return exists
            valid_in = valid_all & fc.notna() & (fc > 0)
            in_rets.append(nxt[valid_in].values)

            # distinct stretches: contiguous runs of forecast > 0 within the window
            pos = (fc > 0) & fc.notna()
            pos_arr = pos.values.astype(bool)
            if len(pos_arr) > 0:
                starts = pos_arr & ~np.concatenate([[False], pos_arr[:-1]])
                n_stretches += int(starts.sum())

    in_r = np.concatenate(in_rets) if in_rets else np.array([])
    all_r = np.concatenate(all_rets) if all_rets else np.array([])
    n_in = int(len(in_r))

    reading = ("t-statistic is the one-sample t of in-stretch next-bar returns against the pooled all-bar mean "
               "(mean_in - mean_all) / (sd_in / sqrt(n_in)); in-stretch means forecast > 0; a distinct up-cross "
               "stretch is a contiguous run of forecast > 0 within one window, including a run already under way "
               "at a window's first bar; insufficient counts are checked first, then reject, then confirm.")

    mean_in = float(np.mean(in_r)) if n_in > 0 else None
    mean_all = float(np.mean(all_r)) if len(all_r) > 0 else None
    diff = (mean_in - mean_all) if (mean_in is not None and mean_all is not None) else None

    t_stat = None
    if n_in > 1 and diff is not None:
        sd = float(np.std(in_r, ddof=1))
        if sd > 0:
            t_stat = float(diff / (sd / np.sqrt(n_in)))

    up_in = float(np.mean(in_r > 0)) if n_in > 0 else None
    up_all = float(np.mean(all_r > 0)) if len(all_r) > 0 else None
    sup_passed = None
    sup_value = None
    if up_in is not None and up_all is not None:
        sup_value = float(up_in - up_all)
        sup_passed = bool(up_in > up_all)

    if n_in < 100 or n_stretches < 3:
        status = "inconclusive"
        decided_by = (f"Inconclusive: {n_in} in-stretch bars (need 100) and {n_stretches} distinct up-cross "
                      f"stretches (need 3) do not meet the minimum counts.")
    elif diff is None or t_stat is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the t-statistic could not be computed."
    elif diff <= 0:
        status = "rejected"
        decided_by = "Rejected: the in-stretch mean daily return is at or below the all-bar mean (no persistence)."
    elif t_stat <= -2.0:
        status = "rejected"
        decided_by = "Rejected: the t-statistic on the difference is -2.0 or lower (moves reverse after up-crosses)."
    elif t_stat >= 2.0 and sup_passed:
        status = "confirmed"
        decided_by = ("Confirmed: the in-stretch mean exceeds the all-bar mean with t >= 2.0 and the in-stretch "
                      "up-day share exceeds the all-bar share.")
    elif t_stat >= 2.0:
        status = "inconclusive"
        decided_by = ("Inconclusive: t >= 2.0 but the in-stretch up-day share does not exceed the all-bar share, "
                      "so the confirm rule is not fully met.")
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the t-statistic lies between -2.0 and 2.0."

    return {
        "status": status,
        "main_measure": {
            "name": "in-stretch minus all-bar mean next-bar return (one-sided t-stat)",
            "value": t_stat,
            "threshold": "t >= 2.0 with positive difference confirms; difference <= 0 or t <= -2.0 rejects",
        },
        "supporting_check": {
            "name": "in-stretch up-day share minus all-bar up-day share",
            "value": sup_value,
            "passed": sup_passed,
        },
        "cases": n_in,
        "decided_by": decided_by,
        "reading": reading,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.power_rev.last_history_value"

    # ---------- 1. situation check ----------
    # Fidelity: long only, when the negated (standardised) product is positive.
    # standardise only scales by a positive mean size, so its sign is the raw sign:
    # the situation on its side is raw product < 0 with forecast > 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & np.isfinite(raw) & (raw < 0) & (fc > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the slope of excess 5-day return on the forecast (forecast > 0, non-overlapping grid)"
    main_thr = "confirm: slope t >= 2 (with Welch t >= 2); reject: slope t <= -2 or Welch t <= -2"
    sup_name = "mean excess 5-day return after prior 5-day return <= 0 minus after > 0, Welch t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the raw "
                           "excess-power product is negative (the reading implying a fall), as the Fidelity requires."),
            "reading": "The situation is a negative raw product with a positive forecast, since standardise keeps the raw sign and the forecast is its negation clipped at 0.",
        }

    # ---------- 2. criterion ----------
    fc_all, ex_all, prior_all = [], [], []
    for coin, wins in bars.items():
        # coin's mean 5-day return over all its windows (non-overlapping grid, all grid bars)
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    if t - H >= 0 and np.isfinite(close[t - H]) and close[t - H] > 0:
                        pr = c0 / close[t - H] - 1.0
                    else:
                        pr = np.nan
                    coin_cases.append((fc[t], r, pr))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for f, r, pr in coin_cases:
            fc_all.append(f)
            ex_all.append(r - drift)
            prior_all.append(pr)

    fc_all = np.asarray(fc_all, dtype=float)
    ex_all = np.asarray(ex_all, dtype=float)
    prior_all = np.asarray(prior_all, dtype=float)
    n_cases = int(len(fc_all))

    slope = None
    slope_t = None
    if n_cases >= 3 and np.ptp(fc_all) > 0:
        lr = stats.linregress(fc_all, ex_all)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    has_prior = np.isfinite(prior_all)
    g_down = ex_all[has_prior & (prior_all <= 0)]
    g_up = ex_all[has_prior & (prior_all > 0)]
    n_down, n_up = int(len(g_down)), int(len(g_up))
    diff = None
    welch_t = None
    if n_down >= 2 and n_up >= 2:
        diff = float(np.mean(g_down) - np.mean(g_up))
        tt = stats.ttest_ind(g_down, g_up, equal_var=False)
        welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    counts = {
        "grid cases with a positive forecast": n_cases,
        "cases with prior 5-day return <= 0": n_down,
        "cases with prior 5-day return > 0": n_up,
    }

    sup_passed = None if welch_t is None else bool(welch_t >= 2)

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 grid cases with a positive forecast ({n_cases})."
    elif n_down < 30 or n_up < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases in a prior-return group (<= 0: {n_down}, > 0: {n_up})."
    elif slope_t is None or welch_t is None:
        status = "inconclusive"
        decided = "The slope t or the Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope_t <= -2 or welch_t <= -2:
        status = "rejected"
        decided = (f"Reject rule met: slope t {slope_t:.2f} <= -2 or Welch t {welch_t:.2f} <= -2.")
    elif slope_t >= 2 and welch_t >= 2:
        status = "confirmed"
        decided = f"Confirm rule met: slope t {slope_t:.2f} >= 2 and Welch t {welch_t:.2f} >= 2."
    else:
        status = "inconclusive"
        decided = (f"Neither rule met (slope t {slope_t:.2f}, Welch t {welch_t:.2f}): any other result is inconclusive.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": welch_t, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 5-day return is taken over all grid bars of all its windows; the regression uses every "
                    "positive-forecast grid case with a 5-day forward return in its window, while the prior-return groups "
                    "use only those with a prior 5-day return inside the window; the plan's minimum counts give "
                    "'not observable'."),
    }

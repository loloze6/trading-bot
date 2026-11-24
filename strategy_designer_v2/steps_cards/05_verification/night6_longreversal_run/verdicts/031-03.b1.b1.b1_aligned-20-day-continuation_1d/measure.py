import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    LHV = "debug_info.components.mom20.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_det = 0
    n_ok = 0
    n_fallback = 0
    n_fallback_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns or "close" not in df.columns:
                continue
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            lhv = df[LHV].astype(float).values if LHV in df.columns else np.full(len(df), np.nan)
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # 20-day return: from prices inside the window, else the recorded raw value
                if t >= 20 and close[t - 20] > 0:
                    r20 = close[t] / close[t - 20] - 1
                else:
                    r20 = lhv[t]
                r60 = close[t] / close[t - 60] - 1 if (t >= 60 and close[t - 60] > 0) else np.nan
                if np.isfinite(r20) and np.isfinite(r60):
                    n_det += 1
                    in_sit = (r20 > 0 and r60 > 0) or (r20 < 0 and r60 < 0)
                    side_ok = np.sign(f) == np.sign(r20)
                    if in_sit and side_ok:
                        n_ok += 1
                else:
                    # 60-day return not computable inside the window: use the detector's regime
                    n_fallback += 1
                    if np.isfinite(r20) and reg[t] == "trending" and np.sign(f) == np.sign(r20) and r20 != 0:
                        n_fallback_ok += 1

    if n_det > 0:
        agreement = n_ok / n_det
    elif n_fallback > 0:
        agreement = n_fallback_ok / n_fallback
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.90

    reading_base = ("Situation check uses bars where both the 20-bar and 60-bar returns can be computed inside the window "
                    "(the regime column only if none can); the coin's mean 10-bar return is the mean of all its "
                    "non-overlapping grid returns over all windows; the day-clustered t sums deviations per UTC date; "
                    "the supporting check splits cases strictly above/below the median |forecast| and passes when "
                    "the high-minus-low mean difference is above 0.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checked": int(n_det)},
            "decided_by": ("Fewer than 90% of active bars have the 20-day and 60-day returns on the same side with the "
                           "forecast's sign equal to the 20-day return's sign, as the Fidelity's situation and side require."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1
                grid_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and f != 0:
                    coin_cases.append((ts.iloc[t].strftime("%Y-%m-%d"), f, r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for day, f, r in coin_cases:
            rows.append({"coin": coin, "day": day, "f": f, "dr": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "dr"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    threshold = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": "mean of forecast/10 x drift-removed 10-bar forward return",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The minimum of 100 grid cases over 50 distinct days is not reached (no cases).",
            "reading": reading_base,
        }

    x = cases["f"].values / 10.0 * cases["dr"].values
    mean = float(np.mean(x))
    dev = pd.Series(x - mean).groupby(cases["day"].values).sum().values
    D = len(dev)
    if D > 1:
        se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / n_cases
        t_main = float(mean / se) if se > 0 else float("nan")
    else:
        t_main = float("nan")

    # supporting check
    absf = np.abs(cases["f"].values)
    dirret = np.sign(cases["f"].values) * cases["dr"].values
    med = np.median(absf)
    hi = dirret[absf > med]
    lo = dirret[absf < med]
    if len(hi) >= 2 and len(lo) >= 2:
        diff = float(np.mean(hi) - np.mean(lo))
        welch_t = float(stats.ttest_ind(hi, lo, equal_var=False).statistic)
        sup_passed = bool(diff > 0)
    else:
        diff = None
        welch_t = None
        sup_passed = None
    supporting = {"name": "drift-removed directional return, |forecast| above minus below median (Welch difference)",
                  "value": diff, "passed": sup_passed}

    main = {"name": "mean of forecast/10 x drift-removed 10-bar forward return",
            "value": mean,
            "statistic": {"name": "day-clustered t of the mean",
                          "value": None if not np.isfinite(t_main) else t_main},
            "threshold": threshold}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 grid cases over 50 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif not np.isfinite(t_main):
        status = "inconclusive"
        decided = "The t of the main measure cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t_main >= 2:
        if sup_passed is True:
            status = "confirmed"
            decided = "The main measure is positive with t >= 2 and the supporting check passes (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The main t is >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean < 0 and t_main <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }

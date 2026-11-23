import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.power_reversal.last_history_value"
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    # Fidelity: the reversal bet against the signal, long only. After 'standardise' (which only scales)
    # and 'negate', the forecast is positive exactly when the raw value (excess power x nearness z) is
    # negative, i.e. when the reversal points up. Situation = raw < 0, expected side = long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw < 0) & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "one-sample t of mean excess 5-day return on positive-forecast grid bars"
    threshold = "confirm t >= 2 (with check passing); reject t <= -2; otherwise inconclusive"
    check_name = "mean excess return, larger half minus smaller half of positive forecasts"
    reading = ("Situation taken as raw component value < 0 with forecast > 0 (standardise only scales, "
               "so negate+clip leaves the forecast positive exactly when the raw value is negative); "
               "the coin's mean 5-day return is taken on the same non-overlapping grid over all its windows; "
               "the halves are split by sorted forecast with the middle case left out when the count is odd; "
               "the plan's fewer-than-100-cases rule is treated as a minimum count, giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "positive-forecast grid cases": 0},
            "decided_by": ("Fewer than 90% of active bars are long bars with a negative raw reversal value "
                           "(the plan's upward reversal situation); the forecast does not follow the Fidelity."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []  # (coin, ret, forecast)
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for t in range(0, n - H, H):
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                allr.append(r)
                if np.isfinite(f[t]) and f[t] > 0:
                    rows.append((coin, r, f[t]))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    ex = np.array([r - coin_rets[c] for c, r, _ in rows], dtype=float)
    fc = np.array([x for _, _, x in rows], dtype=float)
    ok = np.isfinite(ex)
    ex, fc = ex[ok], fc[ok]
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    check_val = None
    check_pass = None
    if n_cases >= 2:
        order = np.argsort(fc, kind="mergesort")
        k = n_cases // 2
        small = ex[order[:k]]
        large = ex[order[n_cases - k:]]
        check_val = float(np.mean(large) - np.mean(small))
        check_pass = bool(check_val > 0)

    counts = {"positive-forecast grid cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} positive-forecast grid cases, fewer than the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so no confirm or reject rule is met."
    elif t_val >= 2 and check_pass:
        status = "confirmed"
        decided = "t >= 2 on the mean excess 5-day return and larger-half minus smaller-half is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "t <= -2 on the mean excess 5-day return of positive-forecast grid bars."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (larger-half minus smaller-half not above 0)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "one-sample t", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": check_name, "value": check_val, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

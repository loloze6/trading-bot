import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.excess_power_high.last_history_value"
    H = 5
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    # Plan's situation: the raw value (excess 365-day power x nearness z-score) is not zero.
    # Expected side: the counter-bet, so the forecast sign is minus the raw sign.
    # standardise only scales, and negate flips, so the expected forecast sign is -sign(raw).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                ok = active & raw.notna() & (raw != 0) & (np.sign(f) == -np.sign(raw))
                n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of forecast/10 x (5-bar forward return minus coin's mean 5-bar return), before costs"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 non-zero-forecast cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases with a non-zero forecast": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast have a non-zero raw excess-power "
                           "value with the forecast's sign opposite to it (the plan's counter-bet)"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The situation is a non-zero raw component value and the expected side is the opposite of its sign.",
        }

    # ---------- 2. Criterion ----------
    products = []
    nonzero = 0
    for coin, wins in bars.items():
        rows = []  # (forecast, fwd return)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = c[i], c[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((f[i], c1 / c0 - 1.0))
        if not rows:
            continue
        arr = np.array(rows, dtype=float)
        rets = arr[:, 1]
        coin_mean = float(np.mean(rets))  # coin's mean 5-bar return over all its windows (grid samples)
        fc = arr[:, 0]
        valid = np.isfinite(fc)
        prod = fc[valid] / 10.0 * (rets[valid] - coin_mean)
        products.extend(prod.tolist())
        nonzero += int(np.sum(fc[valid] != 0))

    products = np.array(products, dtype=float)
    n_cases = int(len(products))
    mean = float(np.mean(products)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(products, ddof=1))
        if sd > 0:
            t = float(mean / (sd / np.sqrt(n_cases)))

    if nonzero < MIN_CASES:
        status = "not observable"
        decided = f"Only {nonzero} grid cases have a non-zero forecast, below the plan's minimum of 300."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean is above 0 with t >= 2 on at least 300 non-zero-forecast cases (confirm rule)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean is below 0 with t <= -2 on at least 300 non-zero-forecast cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t is strictly between -2 and 2 (or the mean and t disagree in sign), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {
            "cases with a non-zero forecast": int(nonzero),
            "grid cases": n_cases,
        },
        "decided_by": decided,
        "reading": ("The mean and t are taken over all grid cases at positions 0, 5, 10, ... of each window with a "
                    "full 5-bar forward return (zero-forecast cases contribute 0), the coin's mean 5-bar return is "
                    "the mean of its grid returns over all its windows, and the 300-case minimum counts the "
                    "non-zero-forecast cases."),
    }

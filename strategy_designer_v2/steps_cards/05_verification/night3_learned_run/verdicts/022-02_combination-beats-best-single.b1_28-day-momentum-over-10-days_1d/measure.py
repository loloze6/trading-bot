import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    MIN_CASES = 300
    RAW = "debug_info.components.mom28.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = the coin's 28-day return (higher or lower); outcome = next-10-day return
    # in the same direction as the 28-day return -> long when the 28-day return is positive,
    # short when it is negative.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the raw value is not recorded, recompute it from prices (inside the window only).
            recomputed = close / close.shift(28) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(fc) == np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "t of the mean of forecast/10 x excess 10-bar return (net of the coin's mean 10-bar return)"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 non-overlapping cases"
    reading = ("Every grid bar (positions 0, 10, 20, ... of each window with close[t+10] inside the window and a "
               "forecast recorded) is a case, including those with forecast 0, and the coin's mean 10-bar return is "
               "the mean over the same non-overlapping grid returns of all its windows; the situation's side is the "
               "sign of the recorded raw 28-day return (recomputed from closes where missing).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases": 0},
            "decided_by": ("Fewer than 90% of the active bars have a forecast whose sign matches the sign of the "
                           "28-day return the plan's situation expects (long after a rise, short after a fall)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    per_coin = {}
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((fc[t], c1 / c0 - 1.0))
        per_coin[coin] = rows

    products = []
    for coin, rows in per_coin.items():
        rets = np.array([r for _, r in rows], dtype=float)
        if len(rets) == 0:
            continue
        mean_ret = float(np.mean(rets))
        for f, r in rows:
            if not np.isfinite(f):
                continue
            products.append(f / 10.0 * (r - mean_ret))

    products = np.array(products, dtype=float)
    n_cases = int(len(products))
    mean_val = float(np.mean(products)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(products, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 300."
    elif t_val is not None and mean_val > 0 and t_val >= 2:
        status = "confirmed"
        decided_by = "The mean forecast-weighted excess 10-bar return is positive with t >= 2 over at least 300 non-overlapping cases."
    elif t_val is not None and mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The mean forecast-weighted excess 10-bar return is negative with t <= -2 over at least 300 non-overlapping cases."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 over at least 300 non-overlapping cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {"non-overlapping cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }

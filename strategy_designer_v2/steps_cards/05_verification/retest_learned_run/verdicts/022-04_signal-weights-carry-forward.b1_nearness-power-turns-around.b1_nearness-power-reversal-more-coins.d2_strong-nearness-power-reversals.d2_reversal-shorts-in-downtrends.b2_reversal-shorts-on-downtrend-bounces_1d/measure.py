import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.excess_power_z.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan's situation: 20-day return < 0, 5-day return > 0, and joint reading > 0.
    # The standardise step keeps the sign, so the raw component's sign is the reading's sign.
    # Expected side: the coin falls, so the forecast must be short (< 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce").astype(float)
            r20 = close / close.shift(20) - 1.0
            r5 = close / close.shift(5) - 1.0
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            # Use the returns computed from prices where the window holds enough history.
            # Before that, use the detector's recorded decision.
            gate_calc = (r20 < 0) & (r5 > 0)
            have_hist = r20.notna() & r5.notna()
            gate = np.where(have_hist, gate_calc, regime == "mean_reversion")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").astype(float)
            else:
                raw = pd.Series(np.nan, index=d.index)
            situation = gate & (raw > 0).fillna(False).values
            active = (fc != 0) & fc.notna()
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of mean of (forecast/10) x (5-bar return minus coin's mean 5-bar return), short grid bars"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 grid cases"

    if not passed:
        if agreement is None:
            decided = "No bar has a nonzero forecast, so the shorts the plan's situation expects cannot be found."
        else:
            decided = ("Fewer than 90% of the bars with a nonzero forecast are short bars where the 20-day return "
                       "is negative, the 5-day return is positive and the joint reading is positive.")
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases": None},
            "decided_by": decided,
            "reading": "Before 20 bars of a window exist, the recorded regime stands in for the two return conditions; the reading's sign is taken from the raw component value.",
        }

    # ---------- 2. Criterion ----------
    products = []
    for coin, wins in bars.items():
        # The coin's mean 5-bar return over all its windows, taken on the non-overlapping grid.
        coin_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").astype(float).values
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    cases.append((fc[t], r))
        if not coin_rets:
            continue
        mu = float(np.mean(coin_rets))
        for f, r in cases:
            products.append((f / 10.0) * (r - mu))

    products = np.asarray(products, dtype=float)
    n = int(products.size)
    mean = float(products.mean()) if n > 0 else None
    if n >= 2:
        sd = float(products.std(ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        tval = None

    if n < 30:
        status = "not observable"
        decided = f"Only {n} grid cases have a negative forecast, which is fewer than the plan's minimum of 30."
    elif tval is not None and mean > 0 and tval >= 2:
        status = "confirmed"
        decided = "The mean product is positive with t >= 2 over at least 30 grid cases."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean product is negative with t <= -2 over at least 30 grid cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 grid cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {"grid cases": n},
        "decided_by": decided,
        "reading": ("The grid is each window's bars 0, 5, 10, ... that have a close 5 bars later. The coin's mean "
                    "5-bar return is taken on that same grid over all its windows. The plan's 'fewer than 30 grid "
                    "cases' is read as the minimum count, which gives 'not observable'. Before 20 bars of a window "
                    "exist, the recorded regime stands in for the return gate in the situation check."),
    }

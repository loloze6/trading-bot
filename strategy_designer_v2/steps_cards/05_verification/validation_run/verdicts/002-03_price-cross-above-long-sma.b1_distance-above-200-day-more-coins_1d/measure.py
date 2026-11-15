import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_CASES = 100
    RAW = "debug_info.components.dist200.last_history_value"

    # ---------- 1. Situation check: close above its 200-day SMA (raw distance > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW not in df.columns:
                continue  # a missing column is not a value of zero: these rows are left out
            raw = pd.to_numeric(df[RAW], errors="coerce")
            m = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(m.sum())
            n_agree += int((m & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars (forecast != 0) are bars where the close is above its "
                           "200-day SMA (raw dist200 > 0) with a long forecast, so the config does not do what the "
                           "plan's Fidelity says." if n_active > 0 else
                           "No active bars with a recorded dist200 value, so the situation could not be matched."),
            "reading": "Agreement is computed on active bars with a non-missing raw dist200 value; the situation is raw distance > 0 and the side is forecast > 0.",
        }

    # ---------- 2. Non-overlapping 20-bar grid per window ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append({"coin": coin, "window": w, "fc": fc[p], "ret": c1 / c0 - 1.0})
    g = pd.DataFrame(rows, columns=["coin", "window", "fc", "ret"])

    # coin's mean 20-bar return over all windows (all grid samples of the coin)
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["excess"] = []

    pos = g[(g["fc"] > 0) & g["fc"].notna() & g["excess"].notna()].copy()
    n_cases = int(len(pos))

    # OLS slope t
    slope = None
    t_val = None
    if n_cases >= 3 and np.nanstd(pos["fc"].to_numpy()) > 0:
        lr = stats.linregress(pos["fc"].to_numpy(dtype=float), pos["excess"].to_numpy(dtype=float))
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_val = float(lr.slope / lr.stderr)

    # supporting check: top third minus bottom third by forecast
    diff = None
    k = n_cases // 3
    if k >= 1:
        s = pos.sort_values("fc", kind="mergesort")
        bottom = s.iloc[:k]["excess"].mean()
        top = s.iloc[-k:]["excess"].mean()
        diff = float(top - bottom)
    sup_passed = None if diff is None else bool(diff > 0)

    main = {
        "name": "OLS slope of 20-bar excess return on forecast (positive-forecast grid bars)",
        "value": slope,
        "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
        "threshold": "slope t >= +2 with >= 100 cases to confirm (with top-minus-bottom third > 0); t <= -2 with >= 100 cases to reject",
    }
    support = {"name": "top-third minus bottom-third mean excess return", "value": diff, "passed": sup_passed}
    counts = {"positive-forecast grid cases": n_cases}
    reading = ("The coin's mean 20-bar return is taken over all its grid bars (positions 0, 20, 40, ... of each "
               "window) in all windows; thirds are the floor(n/3) lowest and highest forecasts after a stable sort; "
               "fewer than 100 cases is reported as not observable per the minimum-count rule.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} positive-forecast grid cases ({n_cases}), so the minimum count is not reached."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Slope t is at least +2 with at least 100 cases and the top-minus-bottom-third difference is above 0."
        else:
            status = "inconclusive"
            decided = "Slope t is at least +2 but the top-minus-bottom-third difference is 0 or less, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "Slope t is at most -2 with at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

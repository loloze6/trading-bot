import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 300
    comp_col = "debug_info.components.vol_scaled_rise.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (Fidelity, kept): a one-day rise scaled by the 20-day std of daily returns.
    # Expected side: long, because the outcome is a further rise.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # one-day return inside the window only
            r1 = close / close.shift(1) - 1.0
            if comp_col in df.columns:
                raw = pd.to_numeric(df[comp_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # an up day: from the prices; on the window's first row, from the recorded raw component
            up = r1 > 0
            first_missing = r1.isna()
            up = up.where(~first_missing, raw > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & up.fillna(False).astype(bool) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are up days "
                           "(a scaled one-day rise) with a long forecast, so the config does not "
                           "implement the plan's situation on its expected side."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, forecast, fwd5)
    coin_all = {}
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                ret = c1 / c0 - 1.0
                allret.append(ret)
                rows.append((coin, fc[t], ret))
        coin_all[coin] = float(np.mean(allret)) if allret else np.nan

    sel_f, sel_x = [], []
    for coin, f, ret in rows:
        if np.isfinite(f) and f > 0 and np.isfinite(coin_all.get(coin, np.nan)):
            sel_f.append(float(f))
            sel_x.append(ret - coin_all[coin])
    sel_f = np.array(sel_f)
    sel_x = np.array(sel_x)
    n_cases = int(len(sel_f))

    reading = ("Coin mean 5-bar return is taken over all grid bars of all its windows; the top and "
               "bottom fifths are the n//5 largest and n//5 smallest positive forecasts by stable sort "
               "of the pooled grid cases; the plan's 300-case minimum maps to 'not observable'; the "
               "situation's up day is read from the close-to-close return (raw component sign on a "
               "window's first row).")

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(sel_f) > 0:
        lr = stats.linregress(sel_f, sel_x)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    diff = None
    sup_pass = None
    k = n_cases // 5
    n_top = n_bot = 0
    if k >= 1:
        order = np.argsort(sel_f, kind="mergesort")
        bot = sel_x[order[:k]]
        top = sel_x[order[-k:]]
        n_top, n_bot = len(top), len(bot)
        diff = float(np.mean(top) - np.mean(bot))
        sup_pass = bool(diff > 0)

    main = {
        "name": "slope of 5-bar excess return on positive forecast, pooled",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if slope t >= 2 with supporting check passing; reject if slope t <= -2",
    }
    supporting = {
        "name": "top fifth minus bottom fifth mean 5-bar excess return > 0",
        "value": diff,
        "passed": sup_pass,
    }
    counts = {
        "independent positive-forecast cases": n_cases,
        "top fifth cases": int(n_top),
        "bottom fifth cases": int(n_bot),
    }

    if n_cases < MIN_CASES or t_slope is None:
        status = "not observable"
        decided = (f"Only {n_cases} independent positive-forecast cases on the 5-bar grid, below "
                   f"the plan's minimum of {MIN_CASES}.")
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and the top-minus-bottom fifth excess return difference is > 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the supporting check (top minus bottom fifth > 0) fails."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

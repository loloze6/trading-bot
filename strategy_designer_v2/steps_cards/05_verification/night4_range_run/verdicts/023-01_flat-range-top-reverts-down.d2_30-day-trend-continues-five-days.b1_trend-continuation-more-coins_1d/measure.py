import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PERIOD = 30
    NMR_THR = 0.5
    FC = "forecast"
    RET_COL = "debug_info.components.ret30.last_history_value"

    # ---------------- 1. Situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)

            # Recompute NetMoveToRangeRatio(30, high_low) from prices, inside the window.
            # Two literal variants of the range span (30 or 31 bars) are both accepted.
            net = (close - close.shift(PERIOD)).abs()
            rng30 = high.rolling(PERIOD).max() - low.rolling(PERIOD).min()
            rng31 = high.rolling(PERIOD + 1).max() - low.rolling(PERIOD + 1).min()
            nmr30 = net / rng30.replace(0, np.nan)
            nmr31 = net / rng31.replace(0, np.nan)
            computable = nmr30.notna() | nmr31.notna()
            in_sit_price = (nmr30 >= NMR_THR) | (nmr31 >= NMR_THR)
            # Bars too early in the window to recompute: use the detector's recorded decision.
            regime_tr = d["regime"].astype(str) == "trending"
            in_sit = np.where(computable, in_sit_price, regime_tr)

            # Expected side: sign of the 30-day return (raw component value, else from prices).
            if RET_COL in d.columns:
                r30 = pd.to_numeric(d[RET_COL], errors="coerce")
            else:
                r30 = pd.Series(np.nan, index=d.index)
            r30_px = close / close.shift(PERIOD) - 1.0
            r30 = r30.where(r30.notna(), r30_px)
            exp_side = np.sign(r30.values)

            active = fc.values != 0
            agree = active & in_sit.astype(bool) & (np.sign(fc.values) == exp_side) & (exp_side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation recomputed as |close[t]-close[t-30]| over the high-low range of the last 30 or 31 bars "
               "(either accepted), using the recorded regime where a window's early bars cannot be recomputed, with "
               "the expected side the sign of the 30-day return; the coin's drift is the mean 5-bar return over all "
               "grid bars of all its windows; the slope t is the ordinary OLS t with an intercept; and the plan's "
               "'fewer than 100 grid cases' rule is applied as a minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are bars where the 30-day net move "
                           "covers at least half of the 30-day high-low range with the forecast on the side of the "
                           "30-day return, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------------- 2. Criterion ----------------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t], reg[t]))

    g = pd.DataFrame(rows, columns=["coin", "fwd", "fc", "regime"])
    if len(g):
        drift = g.groupby("coin")["fwd"].mean()
        g["unusual"] = g["fwd"] - g["coin"].map(drift)
        cases = g[(g["regime"] == "trending") & g["fc"].notna() & (g["fc"] != 0) & g["unusual"].notna()]
    else:
        cases = g
    n_cases = int(len(cases))

    slope = None
    tval = None
    sup_mean = None
    if n_cases >= 3:
        x = cases["fc"].values / 10.0
        y = cases["unusual"].values
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cases > 0:
        sup_mean = float(np.mean(cases["unusual"].values * np.sign(cases["fc"].values)))
    sup_pass = None if sup_mean is None else bool(sup_mean > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases in the trending regime with a nonzero forecast, fewer than the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean directional unusual move is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean directional unusual move is at or below 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger 30-day returns are followed by larger moves against them."
    else:
        status = "inconclusive"
        decided = "The slope's t is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of drift-adjusted 5-bar forward return on forecast/10",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": "confirm at t >= 2 (with supporting mean > 0), reject at t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual 5-bar move in the forecast's direction",
            "value": sup_mean,
            "passed": sup_pass,
        },
        "counts": {"grid cases in the regime": n_cases},
        "decided_by": decided,
        "reading": reading,
    }

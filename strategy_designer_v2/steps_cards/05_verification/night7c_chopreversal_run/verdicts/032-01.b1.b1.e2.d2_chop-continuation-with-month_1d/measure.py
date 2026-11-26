import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    ER_P, ER_MAX = 30, 0.3
    P7, P30 = 7, 30
    MIN_CASES = 50

    fc_col = "forecast"
    reg_col = "regime"

    # ---------- 1. situation check ----------
    n_active_checked = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            f = d[fc_col].astype(float)
            net30 = (c - c.shift(ER_P)).abs()
            path30 = c.diff().abs().rolling(ER_P, min_periods=ER_P).sum()
            er = net30 / path30.replace(0, np.nan)
            r7 = c / c.shift(P7) - 1.0
            r30 = c / c.shift(P30) - 1.0
            computable = er.notna() & r7.notna() & r30.notna()
            active = f.notna() & (f != 0)
            sel = active & computable
            if not sel.any():
                continue
            s7 = np.sign(r7[sel])
            s30 = np.sign(r30[sel])
            in_sit = (er[sel] <= ER_MAX) & (s7 == s30) & (s7 != 0)
            on_side = np.sign(f[sel]) == s7
            n_active_checked += int(sel.sum())
            n_agree += int((in_sit & on_side).sum())

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The situation is recomputed inside each window from closes (ER = |close[t]-close[t-30]| / sum of the "
               "last 30 absolute daily changes, 7- and 30-bar returns as close[t]/close[t-h]-1) and checked only on active "
               "bars where all three can be computed from the window's own bars; regime bars are those whose recorded "
               "regime is 'mean_reversion', the drift is the coin's mean 7-bar return over the non-overlapping grid of all "
               "its windows, the slope is a pooled OLS over coins and windows, and the plan's 'fewer than 50 grid cases' "
               "is applied as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active_checked},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 30-bar ER is at most 0.3 with the 7- and "
                           "30-day returns of the same sign and the forecast on the side of the 7-day move."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # drift per coin: mean of non-overlapping 7-bar returns over all windows
    grid_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                ret = c[i + H] / c[i] - 1.0
                grid_rows.append({
                    "coin": coin,
                    "ret": ret,
                    "regime": d.loc[i, reg_col] if reg_col in d.columns else None,
                    "forecast": d.loc[i, fc_col],
                    "day": pd.Timestamp(d.loc[i, "timestamp"]).normalize(),
                })
    g = pd.DataFrame(grid_rows)
    if len(g) == 0:
        cases = pd.DataFrame(columns=["y", "forecast"])
    else:
        g = g[np.isfinite(g["ret"].astype(float))]
        drift = g.groupby("coin")["ret"].mean()
        g["y"] = g["ret"] - g["coin"].map(drift)
        cases = g[(g["regime"] == "mean_reversion")].copy()
        cases["forecast"] = pd.to_numeric(cases["forecast"], errors="coerce")
        cases = cases[cases["forecast"].notna() & cases["y"].notna()]

    n_cases = int(len(cases))
    counts = {"grid cases in the regime across coins and windows": n_cases}

    slope = None
    t_slope = None
    sup = None
    if n_cases >= 3 and cases["forecast"].astype(float).nunique() > 1:
        x = cases["forecast"].astype(float).values
        y = cases["y"].astype(float).values
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cases > 0:
        sup = float(np.mean(np.sign(cases["forecast"].astype(float).values) * cases["y"].astype(float).values))

    main = {
        "name": "t of the slope of next 7-day return minus drift on forecast, regime grid bars",
        "value": t_slope,
        "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
        "threshold": "confirm if t >= 2 with positive supporting mean; reject if t <= -2",
    }
    sup_passed = None if sup is None else bool(sup > 0)
    supporting = {
        "name": "mean of sign(forecast) x (next 7-day return minus drift)",
        "value": sup,
        "passed": sup_passed,
    }
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": True}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": main,
            "supporting_check": supporting,
            "counts": counts,
            "decided_by": f"Only {n_cases} grid cases in the regime, fewer than the plan's minimum of 50.",
            "reading": reading,
        }

    if t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope t is 2 or more and the supporting mean is positive (confirm rule)."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less (reject rule)."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the supporting mean is not positive (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

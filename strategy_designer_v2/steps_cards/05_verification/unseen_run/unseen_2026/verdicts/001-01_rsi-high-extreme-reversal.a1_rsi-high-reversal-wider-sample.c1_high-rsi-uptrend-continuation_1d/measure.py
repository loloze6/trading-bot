import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    COMP = "debug_info.components.rsi_mom.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret60 = close / close.shift(60) - 1.0
            regime_tr = d["regime"].astype(str) == "trending"
            # 60-bar return > 0 from prices where computable inside the window, else the detector's decision
            regime_ok = np.where(ret60.notna(), ret60 > 0, regime_tr)
            if COMP in d.columns:
                raw = pd.to_numeric(d[COMP], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # RSI above 50 <=> raw component (50 - RSI, or its standardised value) below 0
            rsi_high = (raw < 0).fillna(False).values
            active = (fc.fillna(0) != 0).values
            sit = regime_ok.astype(bool) & rsi_high
            agree = active & sit & (fc.fillna(0) > 0).values
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 10-bar forward return on forecast (trending, non-overlapping grid, pooled)"
    threshold = "slope t >= 2 confirms (with top-third mean excess > 0), t <= -2 rejects; at least 100 independent cases"
    reading = ("Situation = 60-bar return > 0 (recomputed from closes inside the window, falling back to the recorded "
               "regime where 60 prior bars are not in the window) and RSI above 50 (rsi_mom raw value below 0), long side; "
               "the coin's mean 10-bar return is taken on the same non-overlapping grid of all bars of all its windows; "
               "the top third is the n//3 grid cases with the highest forecasts (stable sort); fewer than 100 cases "
               "is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with a positive 60-bar "
                           "return and RSI above 50, so the config does not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[t] == "trending" and np.isfinite(fc[t]):
                    coin_rows.append((float(fc[t]), r))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for f, r in coin_rows:
            rows.append((f, r - mu))

    n_cases = len(rows)
    counts = {"independent trending-grid cases": n_cases}

    slope = None
    tval = None
    top_mean = None
    if n_cases >= 3:
        x = np.array([r[0] for r in rows], dtype=float)
        y = np.array([r[1] for r in rows], dtype=float)
        if np.ptp(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
        k = n_cases // 3
        if k > 0:
            order = np.argsort(-x, kind="mergesort")
            top_mean = float(np.mean(y[order[:k]]))

    sup_passed = None if top_mean is None else bool(top_mean > 0)
    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold}
    sup = {"name": "mean excess 10-bar return of top third of forecasts", "value": top_mean, "passed": sup_passed}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} independent trending-grid cases, fewer than the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (forecast constant on the sample), so it is not 2 or more nor -2 or less."
    elif tval >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more with at least 100 independent cases and the top-third mean excess return is positive."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 100 independent cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top third's mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

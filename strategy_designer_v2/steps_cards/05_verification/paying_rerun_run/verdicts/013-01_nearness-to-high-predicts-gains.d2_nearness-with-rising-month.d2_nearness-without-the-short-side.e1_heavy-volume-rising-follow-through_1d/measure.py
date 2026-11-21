import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RET_PERIOD = 30
    MIN_CASES = 100
    VR = "debug_info.components.volratio.last_history_value"

    # ---------- 1. Situation check: 30-bar return > 0, long side ----------
    n_active = 0
    n_agree = 0
    n_active_fallback = 0
    n_agree_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret30 = close / close.shift(RET_PERIOD) - 1.0
            reg = d["regime"].astype(str).str.strip().str.lower() if "regime" in d.columns else pd.Series([""] * len(d))
            active = fc != 0
            computable = ret30.notna()
            # bars where the 30-bar return can be computed from the prices
            m = active & computable
            n_active += int(m.sum())
            n_agree += int((m & (ret30 > 0) & (fc > 0)).sum())
            # bars where it cannot (first 30 bars of a window): recorded regime as fallback
            mf = active & ~computable
            n_active_fallback += int(mf.sum())
            n_agree_fallback += int((mf & (reg == "trending") & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
    elif n_active_fallback > 0:
        agreement = n_agree_fallback / n_active_fallback
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.90

    reading = ("The situation is a 30-bar close-to-close return above 0 recomputed inside each window "
               "(active bars in a window's first 30 bars, where it cannot be computed, are left out unless no other "
               "active bar exists, then the recorded regime is used), the expected side is long; the main sample is "
               "bars with recorded regime 'trending' on each window's 0,3,6,... grid, and the coin's mean 3-bar return "
               "is taken over the same grid on all bars of all its windows.")

    main_name = "OLS slope of demeaned 3-bar forward return on volratio, trending grid bars"
    threshold = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; at least 100 grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"trending-regime grid cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive 30-bar "
                           "return, so the config does not trade the plan's situation on its side."
                           if agreement is not None else
                           "The record has no active bar, so the config never trades the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin mean 3-bar return over all its windows (grid samples, all bars)
        all_rets = []
        samples = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            reg = d["regime"].astype(str).str.strip().str.lower().to_numpy()
            vr = (pd.to_numeric(d[VR], errors="coerce").to_numpy(dtype=float)
                  if VR in d.columns else np.full(n, np.nan))
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                if reg[t] == "trending":
                    samples.append((r, vr[t]))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for r, v in samples:
            if np.isfinite(v):
                xs.append(v)
                ys.append(r - mu)

    n_cases = len(xs)
    counts = {"trending-regime grid cases": int(n_cases)}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} trending-regime grid cases, below the plan's minimum of 100.",
            "reading": reading,
        }

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if np.allclose(x, x[0]):
        slope, tstat = None, None
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    if slope is not None and tstat is not None and slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tstat:.2f} >= 2 from {n_cases} grid cases (confirm rule)."
    elif slope is not None and tstat is not None and slope < 0 and tstat <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tstat:.2f} <= -2 from {n_cases} grid cases (reject rule)."
    else:
        status = "inconclusive"
        decided = (f"The slope's t = {tstat:.2f} lies between -2 and +2 (inconclusive rule)."
                   if tstat is not None else "The slope's t could not be computed (inconclusive rule).")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS t of slope", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

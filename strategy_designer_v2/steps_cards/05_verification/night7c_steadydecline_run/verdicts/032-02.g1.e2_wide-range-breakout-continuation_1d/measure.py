import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PE_N = 28
    RNG_N = 28
    MIN_CASES = 30
    pp_col = "debug_info.components.near_high.post_pipeline_value"

    # ---------- 1. situation check ----------
    active_n = 0
    agree_n = 0
    undetermined_active = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            pe = close / close.shift(PE_N) - 1.0
            rng = high - low
            mean_rng = rng.rolling(RNG_N, min_periods=RNG_N).mean()
            ratio = rng / mean_rng.replace(0, np.nan)
            computable = pe.notna() & ratio.notna()
            situation = (pe > 0) & (ratio >= 1.0)
            active = fc != 0
            undetermined_active += int((active & ~computable).sum())
            act_c = active & computable
            active_n += int(act_c.sum())
            agree_n += int((act_c & situation & (fc > 0)).sum())

    agreement = float(agree_n / active_n) if active_n > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading_base = (
        "Situation recomputed from prices inside each window (28-bar close change > 0 and today's high-low range "
        "over the mean high-low range of the last 28 bars including today >= 1, long side); active bars of a "
        "window's first 28 bars, where this cannot be computed, are left out of the agreement "
        f"({undetermined_active} such bars); cases are grid bars (positions 0,5,10,... of each window) with "
        "forecast > 0 and a 5-bar forward return inside the window, the coin's mean taken over all its grid "
        "returns of all windows, and the slope uses post_pipeline_value of near_high."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": active_n},
            "decided_by": ("Fewer than 90% of the active bars are uptrend (28-day return > 0), wide-range "
                           "(range >= its 28-bar mean) bars with a long forecast, as the plan's situation requires."
                           if agreement is not None else
                           "No active bar on which the plan's situation could be checked."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            pp = (pd.to_numeric(d[pp_col], errors="coerce").values
                  if pp_col in d.columns else np.full(len(d), np.nan))
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((r, pp[i]))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for r, p in coin_cases:
            case_rows.append((coin, r - mu, p))

    ex = np.array([c[1] for c in case_rows], dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_mean = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        t_mean = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    t_slope = None
    n_slope = 0
    if n_cases > 0:
        pv = np.array([c[2] for c in case_rows], dtype=float)
        m = np.isfinite(pv) & np.isfinite(ex)
        n_slope = int(m.sum())
        if n_slope >= 3 and np.ptp(pv[m]) > 0:
            lr = stats.linregress(pv[m], ex[m])
            slope = float(lr.slope)
            t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    slope_pass = None if slope is None else bool(slope > 0 and t_slope is not None and t_slope >= 1)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 30."
    elif mean_ex is not None and t_mean is not None and mean_ex > 0 and t_mean >= 2:
        if slope_pass:
            status = "confirmed"
            decided = ("Mean excess 5-day return > 0 with t >= 2 over at least 30 grid cases, and the slope "
                       "on the forecast is positive with t >= 1.")
        else:
            status = "inconclusive"
            decided = "Positive mean excess return with t >= 2, but the supporting slope is not positive with t >= 1."
    elif mean_ex is not None and t_mean is not None and mean_ex < 0 and t_mean <= -2:
        status = "rejected"
        decided = "Mean excess 5-day return < 0 with t <= -2 over at least 30 grid cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess 5-day return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess 5-day return on grid bars with forecast > 0",
            "value": mean_ex,
            "statistic": ({"name": "ordinary t of the mean", "value": t_mean} if t_mean is not None else None),
            "threshold": "confirm: > 0 with t >= 2; reject: < 0 with t <= -2; at least 30 grid cases",
        },
        "supporting_check": {
            "name": "slope of excess return on post_pipeline_value (t >= 1, positive)",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {
            "grid cases with forecast > 0": n_cases,
            "cases in slope regression": n_slope,
            "active bars checked": active_n,
        },
        "decided_by": decided,
        "reading": reading_base + (f" Slope t = {t_slope}." if t_slope is not None else ""),
    }

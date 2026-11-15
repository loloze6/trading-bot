import numpy as np
import pandas as pd
from scipy import stats


def _component_value(df, comp_id, field="last_history_value"):
    """Return a Series with the component's recorded value, or None if not recorded."""
    col = f"debug_info.components.{comp_id}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def _get(x):
            try:
                if isinstance(x, dict):
                    c = x.get(comp_id)
                    if isinstance(c, dict):
                        v = c.get(field)
                        return float(v) if v is not None else np.nan
            except Exception:
                pass
            return np.nan
        s = df["debug_info.components"].apply(_get)
        if s.notna().any():
            return pd.to_numeric(s, errors="coerce")
    return None


def measure(bars):
    H = 20
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            # close above its 200-day SMA and SMA rising: the detector's rule, read on the regime column
            situ = regime == "trending"
            slope = _component_value(df, "ma_slope")
            if slope is not None:
                # the recorded raw 20-bar slope of the 200 SMA must also be > 0 (rising average)
                situ = situ & (slope > 0)
            agree = active & situ & (fc > 0)  # expected side: long (outcome is a rise)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 20-bar forward return of active cases (forecast > 0) over coin holding mean"
    main_thr = "confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of excess 20-bar return on forecast, active cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with non-zero forecast are long bars in the 'trending' regime "
                           "(close above a rising 200-day SMA), so the config does not do what the Fidelity says."
                           if n_active > 0 else
                           "No bar has a non-zero forecast, so the config's activity cannot match the plan's situation."),
            "reading": "Situation taken as regime == 'trending' (detector rule close>SMA200 and SMA200 20-bar slope>0) "
                       "combined with the recorded ma_slope raw value > 0 where recorded; side long.",
        }

    # ---------- 2. criterion ----------
    excess_all = []
    fc_all = []
    for coin in sorted(bars.keys()):
        rows = []  # (fwd_return, forecast)
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((c1 / c0 - 1.0, fc[t]))
        if not rows:
            continue
        r = np.array([x[0] for x in rows], dtype=float)
        f = np.array([x[1] for x in rows], dtype=float)
        hold = float(np.mean(r))  # coin's mean 20-bar return over all its windows
        mask = np.isfinite(f) & (f > 0)
        excess_all.extend((r[mask] - hold).tolist())
        fc_all.extend(f[mask].tolist())

    ex = np.array(excess_all, dtype=float)
    fa = np.array(fc_all, dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    slope_coef = None
    if n_cases > 2 and np.std(fa) > 0:
        slope_coef = float(stats.linregress(fa, ex).slope)
    slope_pass = None if slope_coef is None else bool(slope_coef > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} active non-overlapping cases across all coins and windows, below the plan's minimum of 30."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "Mean excess is above 0 with t >= 2 and the slope coefficient of excess on forecast is above 0."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess return of the active cases is below 0 with t <= -2."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the slope coefficient is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope_coef, "passed": slope_pass},
        "counts": {"active non-overlapping cases": n_cases},
        "decided_by": decided,
        "reading": ("Holding is each coin's mean 20-bar return over the same non-overlapping grid samples of all its windows; "
                    "a grid bar counts only if t+20 lies in the same window; the plan's 'fewer than 30 active cases' "
                    "minimum is treated as not observable; the situation is checked on regime == 'trending' plus the "
                    "recorded ma_slope raw value > 0."),
    }

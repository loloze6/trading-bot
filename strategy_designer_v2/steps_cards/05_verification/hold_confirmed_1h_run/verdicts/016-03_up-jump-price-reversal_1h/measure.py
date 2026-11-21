import numpy as np
import pandas as pd
from scipy import stats


def _ols(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = int(len(x))
    if n < 3 or np.nanstd(x) == 0:
        return None, None, n
    res = stats.linregress(x, y)
    slope = float(res.slope)
    se = float(res.stderr) if res.stderr is not None else np.nan
    if not np.isfinite(se) or se == 0:
        t = float(np.sign(slope) * np.inf) if slope != 0 else 0.0
    else:
        t = slope / se
    return slope, float(t), n


def measure(bars):
    H = 72
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            n = len(df)
            rise = np.full(n, np.nan)
            if n > H:
                rise[H:] = close[H:] / close[:-H] - 1.0
            # where the past 72 bars are not in the record, use the detector's decision
            situation = np.where(np.isfinite(rise), rise > 0, regime == "trending")
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess next-72-bar return on forecast (trending grid bars)"
    main_thr = "confirm: slope > 0 with t >= 2 (and supporting slope > 0); reject: slope < 0 with t <= -2; at least 100 grid cases"
    reading = ("Situation computed as close[t]/close[t-72]-1 > 0 inside each window (falling back to regime == 'trending' "
               "on the first 72 bars of a window where the past is not recorded) with short side forecast < 0; grid is "
               "positions 0,72,144,... of each window, a coin's mean grid return pools all its grid bars with a forward "
               "return across windows, the giveback needs close[t-72] inside the window, and the plan's 'below 100 cases "
               "inconclusive' is reported as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active (non-zero forecast) bars are bars with a positive 72-bar "
                           "return and a short forecast, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                fwd = close[p + H] / close[p] - 1.0
                past = close[p] / close[p - H] - 1.0 if p - H >= 0 else np.nan
                rows.append({"coin": coin, "fwd": fwd, "past": past,
                             "fc": fc[p], "trending": regime[p] == "trending"})
    g = pd.DataFrame(rows, columns=["coin", "fwd", "past", "fc", "trending"])
    g = g[np.isfinite(g["fwd"].astype(float))] if len(g) else g
    if len(g):
        coin_mean = g.groupby("coin")["fwd"].mean()
        g["excess"] = g["fwd"] - g["coin"].map(coin_mean)
        t_rows = g[g["trending"] & np.isfinite(g["fc"].astype(float))].copy()
    else:
        t_rows = pd.DataFrame(columns=["excess", "fc", "past", "fwd"])

    slope, tval, n_cases = _ols(t_rows["fc"], t_rows["excess"]) if len(t_rows) else (None, None, 0)

    if len(t_rows):
        past = t_rows["past"].astype(float).to_numpy()
        with np.errstate(divide="ignore", invalid="ignore"):
            give = np.where(np.isfinite(past) & (past != 0), -t_rows["fwd"].astype(float).to_numpy() / past, np.nan)
        s_slope, s_t, s_n = _ols(np.abs(t_rows["fc"].astype(float).to_numpy()), give)
    else:
        s_slope, s_t, s_n = None, None, 0
    s_pass = None if s_slope is None else bool(s_slope > 0)

    counts = {"grid cases": int(n_cases), "giveback cases": int(s_n)}
    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "OLS t of slope", "value": tval},
            "threshold": main_thr}
    support = {"name": "OLS slope of giveback fraction on |forecast|", "value": s_slope, "passed": s_pass}

    if n_cases < 100 or slope is None:
        status = "not observable"
        decided = f"Only {n_cases} trending grid cases, below the plan's minimum of 100."
    elif tval >= 2 and slope > 0:
        if s_pass:
            status = "confirmed"
            decided = "Main slope positive with t >= 2 and the supporting giveback slope positive (confirm rule)."
        else:
            status = "inconclusive"
            decided = "Main t >= 2 but the supporting giveback slope is not positive (inconclusive rule)."
    elif tval <= -2 and slope < 0:
        status = "rejected"
        decided = "Main slope negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "Main t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    TEN, KIJ, SEN, DISP, LB = 9, 26, 52, 26, 26
    SLOPE_COL = "debug_info.components.cloud_slope.last_history_value"

    def cloud(df):
        h = df["high"].astype(float)
        l = df["low"].astype(float)
        tenkan = (h.rolling(TEN, min_periods=TEN).max() + l.rolling(TEN, min_periods=TEN).min()) / 2.0
        kijun = (h.rolling(KIJ, min_periods=KIJ).max() + l.rolling(KIJ, min_periods=KIJ).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(DISP)
        span_b = ((h.rolling(SEN, min_periods=SEN).max() + l.rolling(SEN, min_periods=SEN).min()) / 2.0).shift(DISP)
        top = pd.concat([span_a, span_b], axis=1).max(axis=1, skipna=False)
        mid = (span_a + span_b) / 2.0
        return top, mid

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active_total += int(active.sum())
            if not active.any():
                continue
            close = df["close"].astype(float)
            top, mid = cloud(df)
            pos = close / top - 1.0
            if SLOPE_COL in df.columns:
                slope = pd.to_numeric(df[SLOPE_COL], errors="coerce")
            else:
                slope = pd.Series(np.nan, index=df.index)
            slope_re = mid / mid.shift(LB) - 1.0
            slope = slope.where(slope.notna(), slope_re)
            determinable = active & pos.notna() & slope.notna()
            situ = (pos > 0) & (slope > 0)
            agree = determinable & situ & (f > 0)
            n_active += int(determinable.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation checked on active bars where the cloud top (recomputed from the window's prices, "
               "9/26/52 spans displaced 26) and the 26-day slope (recorded cloud_slope raw value, else recomputed "
               "from the cloud midpoint) are both computable; cases are grid bars 0,26,52,... of each window with "
               "forecast > 0 and a 26-bar forward return inside the window; the coin's mean is the mean of its "
               "non-overlapping 26-bar grid returns over all its windows; the t-statistic is the ordinary t of the "
               "mean of the per-case forecast x excess-return products.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active_total, "active bars checkable": n_active},
            "decided_by": ("Fewer than 90% of the checkable active bars are long bars with the close above a rising "
                           "Ichimoku cloud, as the plan's situation requires"
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation (close above a rising cloud)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    coin_cases.append((f[i], r))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for fv, r in coin_cases:
            case_rows.append((fv, r - mu))

    n_cases = len(case_rows)
    counts = {"independent cases": n_cases}
    threshold = "t >= 2 (confirm, with positive mean) or t <= -2 (reject, with negative mean), at least 50 independent cases"
    mm_name = "forecast-weighted mean 26-bar excess return over the coin's mean"

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "Spearman rank correlation forecast vs excess return > 0",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 50 independent grid cases (none), the plan's minimum count.",
            "reading": reading,
        }

    fa = np.array([c[0] for c in case_rows], dtype=float)
    ea = np.array([c[1] for c in case_rows], dtype=float)
    wmean = float(np.sum(fa * ea) / np.sum(fa))
    prod = fa * ea
    if n_cases > 1 and np.std(prod, ddof=1) > 0:
        t = float(np.mean(prod) / (np.std(prod, ddof=1) / np.sqrt(n_cases)))
    else:
        t = None
    if n_cases > 2 and np.std(fa) > 0 and np.std(ea) > 0:
        rho = float(stats.spearmanr(fa, ea).correlation)
    else:
        rho = None
    sup_passed = None if rho is None or not np.isfinite(rho) else bool(rho > 0)

    if n_cases < 50:
        status = "not observable"
        decided = f"Fewer than 50 independent grid cases ({n_cases}), the plan's minimum count."
    elif t is not None and wmean > 0 and t >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "Forecast-weighted mean excess return positive with t >= 2 over at least 50 cases and rank correlation > 0."
    elif t is not None and wmean < 0 and t <= -2:
        status = "rejected"
        decided = "Forecast-weighted mean excess return negative with t <= -2 over at least 50 cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the rank correlation is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or not computable), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": mm_name, "value": wmean,
                         "statistic": ({"name": "t of the mean of forecast-weighted excess returns", "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman rank correlation forecast vs excess return > 0",
                             "value": rho, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

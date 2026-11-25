import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    DIST = "debug_info.components.ma_dist.last_history_value"
    CHOPPY_REGIME = "unknown"  # the regime that carries the strategy; the vetoes send |60-bar trend| > 10 to "chop" (flat)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if DIST in df.columns:
                dist = pd.to_numeric(df[DIST], errors="coerce")
            else:
                dist = pd.Series(np.nan, index=df.index)
            # recompute the distance from the prices where it is not recorded
            sma = close.rolling(20, min_periods=20).mean()
            dist_px = (close / sma - 1.0) * 100.0
            dist = dist.where(dist.notna(), dist_px)
            regime = df["regime"].astype(str)
            active = fc != 0
            n_active += int(active.sum())
            in_sit = (regime == CHOPPY_REGIME) & dist.notna() & (dist != 0)
            right_side = np.sign(fc) == np.sign(dist)
            n_agree += int((active & in_sit & right_side).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are choppy-profile bars where the forecast's sign "
                           "follows the sign of the close's distance from its 20-day SMA (long above, short below)."),
            "reading": "The choppy profile is read from the recorded regime (the strategy's 'unknown' regime, flat in 'chop'); the distance from last_history_value, recomputed from closes where missing.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    coin_cases.append((ts.iloc[i].floor("D"), f, r))
        if not coin_grid_rets:
            continue
        drift = float(np.mean(coin_grid_rets))
        for d, f, r in coin_cases:
            rows.append({"coin": coin, "date": d, "f": f, "ex": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "date", "f", "ex"])
    n_cases = int(len(cases))
    n_dates = int(cases["date"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct dates": n_dates}
    reading = ("Cases are grid bars (positions 0,10,20,... of each window) with forecast != 0 and a full 10-bar "
               "forward return in the window, drift is the coin's mean 10-bar return on that grid over all its windows, "
               "the t uses per-date summed deviations from the mean (clustered SE with J/(J-1) correction), and the "
               "median split puts |forecast| > median above and <= median below.")
    mm_name = "mean of forecast/10 x (10-bar return - coin drift)"
    mm_thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"

    if n_cases < 200 or n_dates < 60:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 200 cases and 60 distinct dates is not reached.",
            "reading": reading,
        }

    x = (cases["f"] / 10.0) * cases["ex"]
    mean = float(x.mean())
    dev = (x - mean).groupby(cases["date"]).sum()
    J = len(dev)
    se = np.sqrt(J / (J - 1) * float((dev ** 2).sum())) / n_cases if J > 1 else np.nan
    t_main = float(mean / se) if se and np.isfinite(se) and se > 0 else float("nan")

    absf = cases["f"].abs()
    med = float(absf.median())
    signed = np.sign(cases["f"]) * cases["ex"]
    hi = signed[absf > med].values
    lo = signed[absf <= med].values
    if len(hi) >= 2 and len(lo) >= 2:
        t_sup = float(stats.ttest_ind(hi, lo, equal_var=False).statistic)
        sup_pass = bool(np.isfinite(t_sup) and t_sup > 0)
        diff = float(np.mean(hi) - np.mean(lo))
    else:
        t_sup, sup_pass, diff = None, False, None

    if np.isfinite(t_main) and mean > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure's mean is positive with t >= 2 and the supporting check passes (Welch t > 0)."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the supporting check fails, which the plan calls inconclusive."
    elif np.isfinite(t_main) and mean < 0 and t_main <= -2:
        status = "rejected"
        decided = "The main measure's mean is negative with t <= -2: far-from-average coins reverted rather than continued."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": mean,
            "statistic": {"name": "t of the mean, cases summed per date",
                          "value": t_main if np.isfinite(t_main) else None},
            "threshold": mm_thr,
        },
        "supporting_check": {
            "name": "Welch t of signed excess return, |forecast| above minus below median",
            "value": t_sup,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

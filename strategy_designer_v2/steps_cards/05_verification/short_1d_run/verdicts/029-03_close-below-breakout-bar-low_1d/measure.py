import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.fail_depth.last_history_value"

    def recompute_raw(df):
        # Fallback only when the raw column is missing: FailedBreakoutDepth (period 20, source high,
        # reference breakout_low, fail_window 3), computed from the window's prices.
        high = df["high"].to_numpy(float)
        low = df["low"].to_numpy(float)
        close = df["close"].to_numpy(float)
        n = len(df)
        prior_max = pd.Series(high).shift(1).rolling(20, min_periods=20).max().to_numpy()
        brk = close > prior_max
        out = np.zeros(n)
        for t in range(n):
            for k in range(t, max(-1, t - 3), -1):
                if brk[k]:
                    if close[t] < low[k] and low[k] > 0:
                        out[t] = (low[k] - close[t]) / low[k] * 100.0
                    break
        return out

    # ---- situation check ----
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(float)
                miss = np.isnan(raw)
                if miss.any():
                    rc = recompute_raw(df)
                    raw = np.where(miss, rc, raw)
            else:
                raw = recompute_raw(df)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 5-bar return after forecast < 0 (non-overlapping grid)"
    thr = "confirm: mean < 0 with t <= -2 over >= 30 cases and rank correlation < 0; reject: mean > 0 with t >= +2 over >= 30 cases"
    reading = ("Situation bars are bars with the recorded raw fail_depth value above 0 (recomputed from prices only where missing); "
               "grid bars whose 5-bar forward return would leave the window are dropped both from the cases and from the coin's mean, "
               "and an undefined rank correlation counts as a failed check.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on a close below the breakout day's low "
                           "(raw failed-breakout depth > 0), so the config does not do what the Fidelity says."
                           if n_active > 0 else "The forecast is never non-zero, so the config never takes the plan's short."),
            "reading": reading,
        }

    # ---- main measure ----
    exc_all = []
    absf_all = []
    for coin, wins in bars.items():
        rets_coin = []
        case_rets = []
        case_f = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                rets_coin.append(r)
                if np.isfinite(fc[p]) and fc[p] < 0:
                    case_rets.append(r)
                    case_f.append(abs(fc[p]))
        if len(rets_coin) == 0:
            continue
        mu = float(np.mean(rets_coin))
        exc_all.extend([r - mu for r in case_rets])
        absf_all.extend(case_f)

    exc = np.array(exc_all, float)
    absf = np.array(absf_all, float)
    n_cases = int(len(exc))

    mean_exc = float(exc.mean()) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = exc.std(ddof=1)
        if sd > 0:
            t = float(mean_exc / (sd / np.sqrt(n_cases)))
    rho = None
    if n_cases > 2 and np.std(absf) > 0 and np.std(exc) > 0:
        rr = stats.spearmanr(absf, exc).correlation
        rho = float(rr) if np.isfinite(rr) else None
    sup_pass = bool(rho is not None and rho < 0) if n_cases > 0 else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, all coins and windows pooled, fewer than the plan's minimum of 30."
    elif t is not None and t <= -2 and mean_exc < 0 and sup_pass:
        status = "confirmed"
        decided = "The mean excess 5-bar return is negative with t <= -2 over at least 30 cases and the rank correlation is below 0."
    elif t is not None and t <= -2:
        status = "inconclusive"
        decided = "t <= -2 but the rank correlation between |forecast| and the excess return is not below 0, which the plan calls inconclusive."
    elif t is not None and t >= 2 and mean_exc > 0:
        status = "rejected"
        decided = "The mean excess 5-bar return is positive with t >= +2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and +2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_exc,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| with excess 5-bar return, below 0",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "active bars": n_active},
        "decided_by": decided,
        "reading": reading,
    }

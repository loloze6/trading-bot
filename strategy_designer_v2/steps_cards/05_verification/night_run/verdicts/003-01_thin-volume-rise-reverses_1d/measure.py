import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RISE = "debug_info.components.rise.last_history_value"
    THIN = "debug_info.components.thin.last_history_value"

    # ---------- 1. Situation check: up day AND volume below prior-30-day mean, side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")

            # raw rise: sign is the sign of the 1-bar return (vol scaling is positive)
            rec_rise = pd.to_numeric(df[RISE], errors="coerce") if RISE in df.columns else pd.Series(np.nan, index=df.index)
            ret1 = close / close.shift(1) - 1.0  # inside this window only
            rv = ret1.rolling(20, min_periods=20).std()
            calc_rise = ret1 / rv
            rise = rec_rise.where(rec_rise.notna(), calc_rise)

            # raw volume measure: recorded as log ratio (log < 0 <=> ratio < 1)
            rec_thin = pd.to_numeric(df[THIN], errors="coerce") if THIN in df.columns else pd.Series(np.nan, index=df.index)
            prior_mean = vol.shift(1).rolling(30, min_periods=30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                calc_thin = np.log(vol / prior_mean)
            thin = rec_thin.where(rec_thin.notna(), calc_thin)

            active = fc.notna() & (fc != 0)
            situ = (rise > 0) & (thin < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean of -forecast/10 x (coin 5-bar return minus coin mean 5-bar return), active grid bars"
    main_thr = "t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; < 100 active grid cases not observable"
    sup_name = "mean excess 5-bar return of the 20% most negative-forecast active grid bars below 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are short bars on an up day with volume below its prior 30-day mean, as the plan's situation requires.",
            "reading": "Situation taken as rise raw value > 0 and log volume ratio < 0 (ratio < 1) with forecast < 0, using recorded raw values and recomputing from prices where missing.",
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, forecast, ret5)
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append((coin, float(fc[i]), float(r)))
        coin_grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    q, ex, fcs = [], [], []
    for coin, f, r in rows:
        mu = coin_grid_rets.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        e = r - mu
        ex.append(e)
        fcs.append(f)
        q.append(-f / 10.0 * e)
    q = np.array(q)
    ex = np.array(ex)
    fcs = np.array(fcs)
    n_cases = int(len(q))

    mean_q = float(np.mean(q)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(q, ddof=1))
        if sd > 0:
            t = float(mean_q / (sd / np.sqrt(n_cases)))

    sup_val, sup_pass, n_top = None, None, 0
    if n_cases > 0:
        n_top = max(1, int(np.ceil(0.2 * n_cases)))
        order = np.argsort(fcs, kind="mergesort")
        sup_val = float(np.mean(ex[order[:n_top]]))
        sup_pass = bool(sup_val < 0)

    counts = {"active grid cases": n_cases, "top 20% cases": int(n_top)}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} active grid cases in total, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero dispersion)."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the supporting check passes."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the supporting check fails."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The main measure's t is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_q,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "The coin's mean 5-bar return is the mean over all its non-overlapping grid bars (positions 0,5,10,... with a full 5-bar return inside the window) in all windows, the top 20% is the ceiling of 0.2 x the active grid cases ranked by most negative forecast, and the plan's 'fewer than 100 active grid cases' is applied as the minimum count giving 'not observable'.",
    }

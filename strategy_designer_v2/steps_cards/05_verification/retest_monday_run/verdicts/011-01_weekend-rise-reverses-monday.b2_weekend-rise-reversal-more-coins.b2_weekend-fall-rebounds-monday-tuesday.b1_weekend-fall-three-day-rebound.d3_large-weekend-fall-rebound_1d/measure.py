import numpy as np
import pandas as pd
from scipy import stats


def _ts(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        unit = "ms" if v.abs().max() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 3
    RAW = "debug_info.components.wkend_fall.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            ts = _ts(df["timestamp"])
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            # raw component, recomputed from prices where not recorded
            ret1 = close.pct_change()
            vol = ret1.rolling(20).std()
            recomputed = ret1 / vol
            if RAW in df.columns:
                raw = df[RAW].astype(float).where(df[RAW].notna(), recomputed)
            else:
                raw = recomputed
            sunday = (ts.dt.dayofweek == 6).values  # bar whose coming bar is a Monday
            fall = (raw < 0).values
            active = (fc != 0).values & fc.notna().values
            agree = active & sunday & fall & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are Sunday bars after a "
                           "weekend fall (negative vol-scaled return) with a long forecast, as the Fidelity's "
                           "situation and side require."),
            "reading": "The situation is a Sunday bar (next bar a Monday) with a negative raw vol-scaled return, side long.",
        }

    # ---------- criterion ----------
    xs, fs = [], []
    for coin in sorted(bars):
        # coin's mean 3-bar return over all its windows, non-overlapping grid
        grid_rets = []
        per_window = {}
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            per_window[w] = df
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in per_window.items():
            ts = _ts(df["timestamp"])
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            sunday = (ts.dt.dayofweek == 6).values
            n = len(close)
            for i in range(n - H):
                if sunday[i] and np.isfinite(fc[i]) and fc[i] >= 2:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        xs.append(r - drift)
                        fs.append(fc[i])
    x = np.array(xs, dtype=float)
    f = np.array(fs, dtype=float)
    n_cases = int(len(x))

    reading = ("Cases are Sunday bars (UTC weekday 6) with forecast >= 2 whose 3-bar return lies inside the window; "
               "the coin's mean 3-bar return is taken on the non-overlapping grid of all its windows; the t of the "
               "forecast-weighted mean is that mean over its weighted standard error "
               "sqrt(sum(w^2 (x - m)^2)) / sum(w) (sandwich form); the top quartile is the ceil(n/4) cases with the "
               "largest forecast (stable sort), compared with the rest by Welch t.")

    wmean = None
    t_main = None
    sup_val = None
    sup_pass = None
    if n_cases >= 2 and f.sum() > 0:
        wmean = float(np.sum(x * f) / np.sum(f))
        se = float(np.sqrt(np.sum(f ** 2 * (x - wmean) ** 2)) / np.sum(f))
        t_main = float(wmean / se) if se > 0 else 0.0
        order = np.argsort(-f, kind="mergesort")
        k = int(np.ceil(n_cases / 4))
        top = x[order[:k]]
        rest = x[order[k:]]
        if len(top) >= 2 and len(rest) >= 2:
            tt = stats.ttest_ind(top, rest, equal_var=False).statistic
            sup_val = float(tt) if np.isfinite(tt) else None
            sup_pass = bool(sup_val is not None and sup_val > 0)

    main = {
        "name": "forecast-weighted mean excess 3-bar return after a weekend fall",
        "value": wmean,
        "statistic": {"name": "t of the weighted mean", "value": t_main} if t_main is not None else None,
        "threshold": "above 0 with t >= 2 confirms (with the top-quartile check); t <= -2 rejects",
    }
    sup = {"name": "top-quartile minus other cases mean excess return, Welch t > 0",
           "value": sup_val, "passed": sup_pass}
    counts = {"cases": n_cases}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, fewer than the plan's minimum of 100."
    elif t_main is None:
        status = "not observable"
        decided = "The main measure could not be computed on the cases."
    elif wmean > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the top-quartile check passes."
    elif t_main <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return has t <= -2: the largest weekend falls keep falling against the drift."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main measure reaches t >= 2 but the top-quartile check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the forecast-weighted mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

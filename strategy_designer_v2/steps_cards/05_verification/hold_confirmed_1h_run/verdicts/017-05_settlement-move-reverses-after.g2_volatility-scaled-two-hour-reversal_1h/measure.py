import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    RAW = "debug_info.components.fade2h.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the coin's 2-bar move, and the outcome is that the move reverses.
    # So the expected side is opposite to the raw 2-bar return, and the situation holds when that move is non-zero.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float)
            recomputed = close / close.shift(2) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(fc) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of next 2-bar excess return on forecast"
    thr = "slope t >= 2 to confirm (t <= -2 to reject) on at least 5000 independent cases"
    sup_name = "top minus bottom |forecast| quintile mean of sign(forecast) x excess 2-bar return, Welch t >= 2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of non-zero forecasts are opposite in sign to the non-zero 2-bar move "
                          "that the plan's Fidelity says the forecast fades.",
            "reading": "The situation is a non-zero 2-bar return, taken from last_history_value (or recomputed from close "
                       "where it is missing), and the expected side is opposite to its sign.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            idx = np.arange(0, n, H)
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            r = close[idx + H] / close[idx] - 1.0
            f = fc[idx]
            coin_rows.append(pd.DataFrame({"r": r, "f": f}))
        if not coin_rows:
            continue
        cdf = pd.concat(coin_rows, ignore_index=True)
        cdf = cdf[np.isfinite(cdf["r"])]
        # The coin's mean 2-bar return over all its windows, taken on the same grid.
        mu = cdf["r"].mean()
        cdf["ex"] = cdf["r"] - mu
        cdf["coin"] = coin
        rows.append(cdf)

    if rows:
        pool = pd.concat(rows, ignore_index=True)
        pool = pool[np.isfinite(pool["ex"]) & np.isfinite(pool["f"])]
    else:
        pool = pd.DataFrame({"ex": [], "f": []})
    n_pool = int(len(pool))

    slope = None
    t_slope = None
    if n_pool >= 3 and pool["f"].nunique() > 1:
        x = pool["f"].to_numpy(float)
        y = pool["ex"].to_numpy(float)
        X = np.column_stack([np.ones_like(x), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        dof = n_pool - 2
        s2 = float(resid @ resid) / dof
        cov = s2 * np.linalg.inv(X.T @ X)
        slope = float(beta[1])
        se = float(np.sqrt(cov[1, 1]))
        t_slope = float(slope / se) if se > 0 else None

    # Supporting check: quintiles of |forecast| on the pooled grid.
    n_top = n_bot = 0
    diff = None
    t_w = None
    sup_pass = None
    if n_pool > 0:
        a = pool["f"].abs()
        q20, q80 = a.quantile(0.2), a.quantile(0.8)
        top = pool[a >= q80]
        bot = pool[a <= q20]
        n_top, n_bot = int(len(top)), int(len(bot))
        vt = (np.sign(top["f"]) * top["ex"]).to_numpy(float)
        vb = (np.sign(bot["f"]) * bot["ex"]).to_numpy(float)
        if n_top >= 2 and n_bot >= 2:
            diff = float(vt.mean() - vb.mean())
            tw = stats.ttest_ind(vt, vb, equal_var=False).statistic
            t_w = float(tw) if np.isfinite(tw) else None
            sup_pass = bool(t_w is not None and diff > 0 and t_w >= 2)

    counts = {"pooled cases": n_pool, "top quintile cases": n_top, "bottom quintile cases": n_bot}

    if n_pool < 5000 or n_top < 1000 or n_bot < 1000:
        status = "not observable"
        decided = ("A minimum count is not reached: the plan needs at least 5000 pooled cases "
                   "and 1000 cases in each quintile.")
    elif t_slope is not None and slope > 0 and t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = ("The slope is positive with t >= 2 on at least 5000 independent cases, "
                   "and the supporting check passes.")
    elif t_slope is not None and slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 5000 independent cases."
    elif t_slope is not None and t_slope >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": t_w, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Each coin's mean 2-bar return is taken over its non-overlapping grid in all windows; "
                    "the regression is OLS with an intercept on all grid bars, zero forecasts included; "
                    "the quintiles are pooled over coins (|f| >= 80th percentile and |f| <= 20th percentile, "
                    "ties included); the check passes when top minus bottom is positive with Welch t >= 2."),
    }

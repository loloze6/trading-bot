import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the choppy profile

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            # range position recomputed from prices (bar t included), used only where raw is missing
            hh = high.rolling(20, min_periods=20).max()
            ll = low.rolling(20, min_periods=20).min()
            half = (hh - ll) / 2.0
            pos_px = (close - (hh + ll) / 2.0) / half.replace(0, np.nan)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), pos_px)
            else:
                raw = pos_px
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            in_sit = (regime == PROFILE_REGIME) & raw.notna() & (raw != 0)
            same_side = np.sign(fc) == np.sign(raw)
            n_agree += int((active & in_sit & same_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of excess 5-bar forward return on forecast"
    threshold = "slope t >= 2 (with top-minus-bottom third > 0) confirms; t <= -2 rejects"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are choppy-profile bars whose forecast sign "
                           "matches the side of the close in its 20-day range (long above middle, short below)."),
            "reading": "The choppy profile is read as regime 'unknown' (the only regime with a strategy); the expected side is the sign of the raw range position.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        coin_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_all.append(r)
                coin_rows.append((coin, ts.iloc[i].floor("D"), fc[i], r))
        if not coin_all:
            continue
        mu = float(np.mean(coin_all))
        for coin_, day, f, r in coin_rows:
            if np.isfinite(f) and f != 0:
                rows.append((coin_, day, float(f), r - mu))

    n_cases = len(rows)
    days = [r[1] for r in rows]
    n_days = int(len(set(days)))
    counts = {"grid cases inside the profile": int(n_cases), "distinct days": n_days}

    reading = ("The choppy profile is read as regime 'unknown' (the only regime with a strategy); the coin's mean 5-bar return "
               "is taken over all its grid cells in all windows; OLS with intercept, cluster-robust (by UTC day) SEs with the "
               "usual G/(G-1)(N-1)/(N-K) correction; thirds are cut at the pooled 1/3 and 2/3 forecast quantiles; "
               "the plan's 'fewer than 100 cases or 60 days' is reported as not observable.")

    slope = None
    tstat = None
    diff = None
    if n_cases >= 3:
        f = np.array([r[2] for r in rows])
        y = np.array([r[3] for r in rows])
        X = np.column_stack([np.ones(n_cases), f])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        resid = y - X @ beta
        slope = float(beta[1])
        dser = pd.Series(days)
        codes, uniq = pd.factorize(dser)
        G = len(uniq)
        meat = np.zeros((2, 2))
        for g in range(G):
            idx = codes == g
            s = X[idx].T @ resid[idx]
            meat += np.outer(s, s)
        K = 2
        if G > 1 and n_cases > K:
            corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - K))
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            tstat = float(slope / se) if np.isfinite(se) and se > 0 else None
        q1, q2 = np.quantile(f, [1 / 3, 2 / 3])
        top = y[f >= q2]
        bot = y[f <= q1]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())

    sup_pass = None if diff is None else bool(diff > 0)
    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if tstat is None else {"name": "slope t, SE clustered by day", "value": tstat},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 5-bar return, top third minus bottom third of forecasts",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 100 or n_days < 60:
        result["status"] = "not observable"
        result["decided_by"] = ("Minimum count not reached: fewer than 100 grid cases inside the profile or cases on "
                                "fewer than 60 distinct days.")
        return result
    if tstat is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
        return result
    if tstat >= 2 and sup_pass:
        result["status"] = "confirmed"
        result["decided_by"] = "Slope t >= 2 and the top-minus-bottom third difference is above zero (confirm rule)."
    elif tstat <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "Slope t <= -2: higher range positions are followed by smaller rises (reject rule)."
    elif tstat >= 2:
        result["status"] = "inconclusive"
        result["decided_by"] = "Slope t >= 2 but the top-minus-bottom third difference is at or below zero (inconclusive rule)."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "Slope t is between -2 and 2 (inconclusive rule)."
    return result

import numpy as np
import pandas as pd


def measure(bars):
    H = 20          # horizon in bars
    LOOK = 60       # prior closes for the breakout
    BAND = 2.0      # default bet band (min_allocation_change)
    MIN_CASES = 30
    MIN_DAYS = 30

    def _prep(df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        return df

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = _prep(df)
            prepared[coin][w] = d
            close = d["close"]
            prior_max = close.shift(1).rolling(LOOK, min_periods=LOOK).max()
            computable = prior_max.notna() & close.notna()
            situ_price = close > prior_max
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            situ_regime = regime == "trending"
            situ = np.where(computable, situ_price, situ_regime)
            d["_situ"] = situ.astype(bool)
            active = d["forecast"] != 0
            agree = active & d["_situ"] & (d["forecast"] > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The breakout is recomputed from the window's own closes where 60 prior closes exist in the window "
               "and read from the recorded regime ('trending') on earlier bars; a case is the first bet (a rise of the "
               "long forecast of at least the default 2-point band from its low since the last bet) in each 20-bar grid "
               "cell of a window, on a break bar, with a full 20-bar return inside the window; the normal drift is the "
               "coin's mean 20-bar return on the grid of all its windows; the slope t uses OLS with standard errors "
               "clustered by UTC day; the plan's 'fewer than 30 cases or days' rule is reported as 'not observable'.")

    main_name = "OLS slope of 20-day unusual move on the case's forecast"
    main_thr = "slope > 0 with t >= 2 confirms (with mean unusual move > 0); slope < 0 with t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose close is above the "
                           "highest of the prior 60 closes" if n_active > 0 else
                           "The forecast is never non-zero, so no bar shows the plan's long breakout situation"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in prepared.items():
        # normal drift: mean of grid 20-bar returns over all windows of the coin
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].values
            for p in range(0, len(d), H):
                if p + H < len(d) and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in wins.items():
            f = d["forecast"].values
            c = d["close"].values
            situ = d["_situ"].values
            n = len(d)
            side = 0
            trough = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                s = int(np.sign(fi))
                if s == 0:
                    side = 0
                    trough = 0.0
                    continue
                if s != side:
                    side = s
                    trough = 0.0
                lvl = abs(fi)
                if lvl - trough >= BAND - 1e-12:
                    bet[i] = True
                    trough = lvl
                else:
                    trough = min(trough, lvl)
            for start in range(0, n, H):
                end = min(start + H, n)
                for i in range(start, end):
                    if bet[i] and f[i] > 0 and situ[i]:
                        if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                            r = c[i + H] / c[i] - 1.0
                            xs.append(float(f[i]))
                            ys.append(float(r - drift))
                            days.append(d["timestamp"].iloc[i].strftime("%Y-%m-%d"))
                        break  # one case per grid cell

    n_cases = len(xs)
    n_days = len(set(days))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    mean_unusual = float(np.mean(y)) if n_cases > 0 else None

    slope, tval = None, None
    if n_cases >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        dser = pd.Series(np.arange(n_cases)).groupby(pd.Series(days)).apply(list)
        meat = np.zeros((2, 2))
        for idx in dser:
            idx = np.array(idx)
            sg = X[idx].T @ resid[idx]
            meat += np.outer(sg, sg)
        G = len(dser)
        k = 2
        if G > 1 and n_cases > k:
            corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k))
        else:
            corr = 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
        slope = float(beta[1])
        tval = float(slope / se) if se > 0 else None

    sup_passed = None if mean_unusual is None else bool(mean_unusual > 0)
    supporting = {"name": "mean unusual 20-day move over all cases > 0",
                  "value": mean_unusual, "passed": sup_passed}
    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "slope t, clustered by day", "value": tval},
            "threshold": main_thr}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (no spread in the forecast), so it is not >= 2 nor <= -2: inconclusive."
    elif slope > 0 and tval >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move is above 0: confirm."
        else:
            status = "inconclusive"
            decided = "The slope t >= 2 but the mean unusual move is at or below 0: inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: reject."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

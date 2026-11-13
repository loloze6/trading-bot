import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    N_DON = 20
    BOUND = 0.01  # +-1 percentage point of 10-day return, as a decimal

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    rows = []          # (coin, forecast, fwd return, cluster id)
    coin_fwd_all = {}  # coin -> list of all 10-bar forward returns
    cluster_counter = 0

    for coin, wins in bars.items():
        coin_fwd_all.setdefault(coin, [])
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # Situation: the close is the highest of the last 20 closes,
            # computed from the prices.
            rollmax = close.rolling(N_DON, min_periods=N_DON).max()
            situ = close >= rollmax - 1e-12
            enough = rollmax.notna()
            # Where the window does not hold 20 closes yet, fall back on the
            # detector's own decision.
            if "regime" in df.columns:
                reg_tr = df["regime"].astype(str).str.lower() == "trending"
            else:
                reg_tr = pd.Series(False, index=df.index)
            situ = situ.where(enough, reg_tr).fillna(False).astype(bool)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

            # Forward 10-bar return, inside this window only.
            fwd = close.shift(-H) / close - 1.0
            coin_fwd_all[coin].extend(fwd.dropna().tolist())

            # Clusters: breakout bars (forecast > 0) within 10 bars of each
            # other form one cluster.
            pos_idx = np.where((fc > 0).fillna(False).values)[0]
            prev = None
            cid = None
            for i in pos_idx:
                if prev is None or i - prev > H:
                    cluster_counter += 1
                    cid = cluster_counter
                prev = i
                r = fwd.iloc[i]
                f = fc.iloc[i]
                if pd.notna(r) and pd.notna(f):
                    rows.append((coin, float(f), float(r), cid))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = ("Top-minus-bottom half of positive forecast: mean excess "
                 "10-bar forward return (pp), pooled over coins")
    threshold_txt = ("Reject if t >= 2 or t <= -2; confirm if |t| < 2 and both "
                     "one-sided tests against +-1 pp reach t >= 2")
    tost_name = "TOST against +-1 pp: min of the two one-sided t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active),
                       "active bars on a new 20-day closing high, long": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are "
                           "long bars where the close is the highest of the last 20 "
                           "closes, so the config does not trade the plan's situation."),
            "reading": ("The situation is recomputed from closes as close >= max of "
                        "the last 20 closes (including today), falling back on "
                        "regime == 'trending' where the window has fewer than 20 "
                        "closes."),
        }

    # ---------- 2. Criterion ----------
    reading = ("Halves split at the pooled median of positive forecasts "
               "(top: forecast > median, bottom: forecast <= median). The coin's "
               "mean 10-bar return is taken over every bar of all its windows. "
               "Clusters are runs of positive-forecast bars less than or equal to 10 "
               "bars apart in the same window. The t is cluster-robust (CR1) on the "
               "top-indicator coefficient, and the per-half counts are the distinct "
               "clusters with a bar in that half.")

    if len(rows) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": {"name": tost_name, "value": None, "passed": None},
            "counts": {"independent breakout clusters": 0,
                       "clusters in top half": 0, "clusters in bottom half": 0},
            "decided_by": ("Fewer than 100 independent breakout clusters (none with "
                           "a 10-bar forward return)."),
            "reading": reading,
        }

    d = pd.DataFrame(rows, columns=["coin", "f", "r", "cl"])
    coin_mean = {c: (np.mean(v) if len(v) else np.nan) for c, v in coin_fwd_all.items()}
    d["x"] = d["r"] - d["coin"].map(coin_mean)
    d = d.dropna(subset=["x"])
    med = float(d["f"].median())
    d["top"] = (d["f"] > med).astype(float)

    n_clusters = int(d["cl"].nunique())
    n_cl_top = int(d.loc[d["top"] == 1, "cl"].nunique())
    n_cl_bot = int(d.loc[d["top"] == 0, "cl"].nunique())
    counts = {"independent breakout clusters": n_clusters,
              "clusters in top half": n_cl_top,
              "clusters in bottom half": n_cl_bot}

    diff = None
    se = None
    t = None
    if n_cl_top > 0 and n_cl_bot > 0:
        diff = float(d.loc[d["top"] == 1, "x"].mean() - d.loc[d["top"] == 0, "x"].mean())
        X = np.column_stack([np.ones(len(d)), d["top"].values])
        y = d["x"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("cl").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_clusters
        N = len(d)
        K = 2
        if G > 1 and N > K:
            adj = (G / (G - 1.0)) * ((N - 1.0) / (N - K))
            V = adj * XtX_inv @ meat @ XtX_inv
            var_b = V[1, 1]
            if var_b > 0:
                se = float(np.sqrt(var_b))
                t = float(beta[1] / se)

    tost_min = None
    tost_pass = None
    if diff is not None and se is not None and se > 0:
        t_low = (diff + BOUND) / se
        t_up = (BOUND - diff) / se
        tost_min = float(min(t_low, t_up))
        tost_pass = bool(t_low >= 2 and t_up >= 2)

    if n_clusters < 100 or n_cl_top < 40 or n_cl_bot < 40:
        missing = []
        if n_clusters < 100:
            missing.append(f"{n_clusters} independent breakout clusters (< 100)")
        if n_cl_top < 40:
            missing.append(f"{n_cl_top} clusters in the top half (< 40)")
        if n_cl_bot < 40:
            missing.append(f"{n_cl_bot} clusters in the bottom half (< 40)")
        status = "not observable"
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif t is None:
        status = "inconclusive"
        decided = ("The cluster-robust t could not be computed, so neither the "
                   "confirm nor the reject rule is met.")
    elif t >= 2:
        status = "rejected"
        decided = ("Reject: the top-minus-bottom difference has t >= 2, so outsized "
                   "breakout days are followed by larger rises.")
    elif t <= -2:
        status = "rejected"
        decided = ("Reject: the top-minus-bottom difference has t <= -2, so breakout "
                   "size subtracts.")
    elif tost_pass:
        status = "confirmed"
        decided = ("Confirm: |t| < 2 and both one-sided tests against +-1 pp reach "
                   "t >= 2.")
    else:
        status = "inconclusive"
        decided = ("Inconclusive: |t| < 2 but the two one-sided tests against +-1 pp "
                   "do not both reach t >= 2.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": (float(diff * 100.0) if diff is not None else None),
            "statistic": ({"name": "cluster-robust t (breakout clusters)", "value": float(t)}
                          if t is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": tost_name, "value": tost_min, "passed": tost_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

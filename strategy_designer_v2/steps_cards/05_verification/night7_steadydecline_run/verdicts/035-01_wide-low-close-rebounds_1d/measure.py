import numpy as np
import pandas as pd


def measure(bars):
    comp = "wide_low_close"
    raw_col = f"debug_info.components.{comp}.last_history_value"
    post_col = f"debug_info.components.{comp}.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the graded product (high - close) / mean prior 14-day range,
    # which is positive whenever the close is below the high. Expected side: long (a rise).
    n_active = 0
    n_agree = 0
    cases = []  # (coin, window, timestamp, forecast_value, next_return)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # Raw component value: recorded, else recomputed from prices inside the window.
            rng = high - low
            prior_mean = rng.shift(1).rolling(14, min_periods=14).mean()
            recomputed = (high - close) / prior_mean.replace(0, np.nan)
            if raw_col in d.columns:
                raw = pd.to_numeric(d[raw_col], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # cases for the criterion
            nxt = close.shift(-1) / close - 1.0
            post = pd.to_numeric(d[post_col], errors="coerce") if post_col in d.columns \
                else pd.Series(np.nan, index=d.index)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            for i in range(len(d)):
                cases.append((coin, w, ts.iloc[i], post.iloc[i], nxt.iloc[i]))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled slope of next-day excess return on post_pipeline_value"
    thr = "t (day-clustered) >= 2 confirms (with top-fifth mean > 0); t <= -2 rejects"
    sup_name = "mean next-day excess return of the per-coin top fifth of forecast values"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where "
                           "the close sits below the high (positive graded product), as the Fidelity's "
                           "situation and long side require."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    c = pd.DataFrame(cases, columns=["coin", "window", "ts", "f", "r"])
    # coin's mean daily return over all windows (all next-bar returns within windows)
    coin_mean = c.dropna(subset=["r"]).groupby("coin")["r"].mean()
    c["ex"] = c["r"] - c["coin"].map(coin_mean)
    c["day"] = c["ts"].dt.floor("D")

    n_days_forecast = int(c.loc[c["f"].notna(), "day"].nunique())

    u = c.dropna(subset=["f", "ex", "day"]).copy()
    n_cases = int(len(u))

    slope = None
    t_stat = None
    if n_cases >= 3 and u["f"].var() > 0:
        X = np.column_stack([np.ones(n_cases), u["f"].values.astype(float)])
        y = u["ex"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        codes, _ = pd.factorize(u["day"])
        G = int(codes.max()) + 1
        scores = np.zeros((G, 2))
        np.add.at(scores, codes, X * resid[:, None])
        meat = scores.T @ scores
        corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - 2)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_stat = float(slope / se) if se and np.isfinite(se) else None

    # supporting check: per-coin top fifth of forecast values
    top_parts = []
    for coin, g in u.groupby("coin"):
        q = g["f"].quantile(0.8)
        top_parts.append(g[g["f"] >= q])
    top = pd.concat(top_parts) if top_parts else u.iloc[0:0]
    top_mean = float(top["ex"].mean()) if len(top) > 0 else None
    sup_pass = (top_mean is not None and top_mean > 0)

    counts = {
        "distinct days with a recorded forecast": n_days_forecast,
        "cases": n_cases,
        "days with cases": int(u["day"].nunique()),
        "top-fifth cases": int(len(top)),
    }

    if n_days_forecast < 500:
        status = "not observable"
        decided = f"Only {n_days_forecast} distinct days with a recorded forecast, below the plan's minimum of 500."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-fifth mean next-day excess return is positive."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-fifth mean next-day excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t, day-clustered SE", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": top_mean, "passed": bool(sup_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The slope is an OLS with intercept of next-bar excess return on post_pipeline_value over all "
                    "coin-bars, its t from a sandwich SE clustered by UTC calendar day (small-sample factor "
                    "G/(G-1)*(N-1)/(N-2)); 'top fifth' is the bars at or above each coin's 80th percentile of "
                    "post_pipeline_value; the 500-day minimum counts distinct UTC days with a non-missing "
                    "post_pipeline_value and, as a minimum count, gives 'not observable'; the situation is a "
                    "positive raw component value (close below the high) on a long forecast."),
    }

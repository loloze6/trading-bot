import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.vol_ratio.last_history_value"

    # ---------- collect per-bar rows ----------
    rows = []
    for coin, wins in bars.items():
        per_coin = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            vol = d["volume"].astype(float)
            # next-bar return inside the window only
            d["_ret1"] = close.shift(-1) / close - 1.0
            # raw component: recorded value, recomputed from prices where missing
            prior_mean = vol.shift(1).rolling(20, min_periods=20).mean()
            recomputed = vol / prior_mean - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            d["_raw"] = raw
            d["_coin"] = coin
            d["_win"] = w
            d["_day"] = d["timestamp"].dt.floor("D")
            per_coin.append(d[["_coin", "_win", "_day", "forecast", "_raw", "_ret1"]])
        if not per_coin:
            continue
        cdf = pd.concat(per_coin, ignore_index=True)
        # coin's mean daily return over all its windows together
        coin_mean = cdf["_ret1"].mean()
        cdf["_exc"] = cdf["_ret1"] - coin_mean
        rows.append(cdf)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "clustered-by-day t >= 2 confirms, <= -2 rejects"},
            "supporting_check": None,
            "counts": {"distinct days with recorded forecasts": 0},
            "decided_by": "No bars in the record; the minimum of 500 distinct days is not reached.",
            "reading": "none",
        }

    allb = pd.concat(rows, ignore_index=True)
    allb["forecast"] = pd.to_numeric(allb["forecast"], errors="coerce")

    # ---------- situation check ----------
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    if len(active) > 0:
        expected = np.sign(active["_raw"].values)  # heavier -> long, lighter -> short
        got = np.sign(active["forecast"].values)
        ok = (expected != 0) & np.isfinite(active["_raw"].values) & (expected == got)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = agreement >= 0.90

    threshold_txt = "slope t (clustered by day) >= 2 with supporting check passing confirms; t <= -2 rejects; otherwise inconclusive"
    main_name = "slope of next-day excess return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(len(active))},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign equal to the sign of the "
                           "centred volume ratio (long on heavier-than-20-day-mean volume, short on lighter)."),
            "reading": "The plan's situation and side are read as: forecast sign must equal the sign of volume/prior-20-day-mean - 1.",
        }

    # ---------- minimum count ----------
    n_days_forecast = int(allb.loc[allb["forecast"].notna(), "_day"].nunique())

    # ---------- main measure: pooled OLS slope, clustered by day ----------
    s = allb[allb["forecast"].notna() & allb["_exc"].notna()].copy()
    slope = None
    tstat = None
    n_obs = int(len(s))
    n_clusters = int(s["_day"].nunique()) if n_obs else 0
    if n_obs >= 3 and n_clusters >= 2 and s["forecast"].std() > 0:
        x = s["forecast"].values.astype(float)
        y = s["_exc"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        resid = y - X @ beta
        codes = pd.factorize(s["_day"])[0]
        G = codes.max() + 1
        scores = X * resid[:, None]
        S = np.zeros((G, 2))
        np.add.at(S, codes, scores)
        meat = S.T @ S
        k = 2
        corr = (G / (G - 1.0)) * ((n_obs - 1.0) / (n_obs - k))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1]))
        slope = float(beta[1])
        tstat = float(slope / se) if se > 0 else None

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    if n_obs > 0:
        q20 = s["forecast"].quantile(0.2)
        q80 = s["forecast"].quantile(0.8)
        top = s.loc[s["forecast"] >= q80, "_exc"]
        bot = s.loc[s["forecast"] <= q20, "_exc"]
        if len(top) > 0 and len(bot) > 0:
            sup_val = float(top.mean() - bot.mean())
            sup_pass = bool(sup_val > 0)

    counts = {
        "distinct days with recorded forecasts": n_days_forecast,
        "bars in slope": n_obs,
        "day clusters": n_clusters,
    }

    reading = ("Every bar with a forecast and a same-window next close enters (zero forecasts included); "
               "the slope's t uses an intercept and CR1 cluster-robust errors by UTC day; top/bottom fifths are "
               "forecast >= pooled 80th / <= pooled 20th percentile; 'days with recorded forecasts' are distinct "
               "UTC days with a non-missing forecast on any coin.")

    if n_days_forecast < 500:
        status = "not observable"
        decided = f"Only {n_days_forecast} distinct days with recorded forecasts, below the plan's minimum of 500."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom-fifth excess return is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t, clustered by day", "value": tstat}
                          if tstat is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "top-fifth minus bottom-fifth mean next-day excess return",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    D = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday; D["yr"] = D["day"].dt.year
    D["sat"] = (D["wd"] == 5)
    def welch(x, m):
        a = x[m]; b = x[~m]
        t = stats.ttest_ind(a, b, equal_var=False)
        return a.mean() - b.mean(), t.statistic, len(a)
    r = []
    for coin, d in D.groupby("coin"):
        dif, t, n = welch(d["coin_return"].values, d["sat"].values)
        dif2, t2, _ = welch(d["coin_return"].values, d["wd"].isin([4, 5]).values)
        r.append(dict(coin=coin, sat_minus_rest=dif, t=t, n_sat=n, frisat_minus_rest=dif2, t2=t2))
    out["sat_by_coin"] = pd.DataFrame(r).set_index("coin").round(4)
    r = []
    for yr, d in D.groupby("yr"):
        dif, t, n = welch(d["coin_return"].values, d["sat"].values)
        r.append(dict(yr=yr, sat_minus_rest=dif, t=t, n_sat=n))
    out["sat_by_year"] = pd.DataFrame(r).set_index("yr").round(4)
    # cross-sectional: daily mean across coins, weekday t (independent days)
    X = D.groupby("day")["coin_return"].mean().to_frame("m")
    X["wd"] = X.index.weekday
    s = X.groupby("wd")["m"].agg(["count", "mean", "std"])
    s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
    out["xs_mean_weekday"] = s.round(5)
    # regime for days: regime at last bar of day
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values; n = len(c)
            fwd10 = np.r_[c[10:] / c[:-10] - 1, [np.nan] * 10] if n > 10 else np.full(n, np.nan)
            p30 = pd.Series(c).pct_change(30).values
            sma200dist = np.nan
            for i in range(0, n, 10):
                rows.append(dict(coin=coin, w=w, fwd10=fwd10[i], p30=p30[i], reg=df["regime"].iloc[i],
                                 s=df.get("debug_info.components.run.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    g = g.dropna(subset=["ex", "p30"])
    # 30-day return standardised per coin by pooled std (rough), deciles by regime
    for reg in ["trending", "unknown"]:
        x = g[g.reg == reg].copy()
        x["dq"] = pd.qcut(x["p30"], 10, labels=False)
        r = x.groupby("dq").agg(n=("ex", "count"), mean=("ex", "mean"), std=("ex", "std"), p30=("p30", "median"))
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["n"]))
        out[f"p30_decile_{reg}"] = r.round(4)
        # slope of ex on p30 in upper half
        up = x[x["p30"] > x["p30"].median()]
        sl = stats.linregress(up["p30"], up["ex"])
        out[f"upperhalf_slope_{reg}"] = f"slope={sl.slope:.4f} t={sl.slope/sl.stderr:.2f} n={len(up)}"
        sl = stats.linregress(x["p30"], x["ex"])
        out[f"all_slope_{reg}"] = f"slope={sl.slope:.4f} t={sl.slope/sl.stderr:.2f} n={len(x)}"
    return out

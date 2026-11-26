import pandas as pd, numpy as np

def tclust(x, day):
    df = pd.DataFrame({"x": x.values, "d": day.values}).dropna()
    if len(df) < 3: return (len(df), np.nan, np.nan, np.nan)
    m = df["x"].mean()
    s = (df["x"] - m).groupby(df["d"]).sum()
    G = len(s)
    se = np.sqrt((s**2).sum() * G / (G - 1)) / len(df)
    return (len(df), G, m, m / se)

def tab(g, key, col="ex", day="day"):
    rows = {}
    for k, gg in g.groupby(key):
        n, G, m, t = tclust(gg[col], gg[day])
        rows[k] = dict(n=n, days=G, mean=m, t_clust=t)
    return pd.DataFrame(rows).T

def explore(data):
    out = {}
    d = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day", "coin_return", "book_return"]].copy(); x["coin"] = coin; x["win"] = w
            d.append(x)
    d = pd.concat(d).dropna()
    d["day"] = pd.to_datetime(d["day"])
    d["wd"] = d["day"].dt.dayofweek
    d["yr"] = d["day"].dt.year
    d["ex"] = d["coin_return"] - d.groupby("coin")["coin_return"].transform("mean")
    out["daily ex by weekday, day-clustered"] = tab(d, "wd")
    d["half"] = np.where(d["yr"] <= 2021, "2018-2021", "2022-2025")
    d["wd_half"] = d["wd"].astype(str) + "_" + d["half"]
    out["daily ex by weekday x half, day-clustered"] = tab(d, "wd_half")
    sat = d[d.wd == 5]
    out["saturday ex by coin"] = tab(sat, "coin")
    out["saturday ex by year"] = tab(sat, "yr")
    # previous day return graded -> next day, by sign of prev
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(20, n - 20, 20):
                rows.append(dict(coin=coin, day=ts.iloc[i].normalize(), ret=c[i+20]/c[i]-1,
                                 regime=df["regime"].iloc[i],
                                 score=df["debug_info.regime_scores.mean_reversion"].iloc[i],
                                 rally=df["debug_info.components.rally.last_history_value"].iloc[i],
                                 past20=c[i]/c[i-20]-1,
                                 dd20=c[i]/c[max(0,i-20):i+1].max()-1))
    g = pd.DataFrame(rows)
    g["ex"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    s = g.dropna(subset=["score"]).copy()
    s["sq"] = pd.qcut(s["score"].rank(method="first"), 5, labels=False)
    out["h20 ex by score quintile, clustered"] = tab(s, "sq")
    r = g[g.regime == "mean_reversion"].dropna(subset=["rally"]).copy()
    r["rq"] = pd.qcut(r["rally"].rank(method="first"), 3, labels=False)
    out["h20 in-regime by rally tercile, clustered"] = tab(r, "rq")
    r["rq5"] = pd.qcut(r["rally"].rank(method="first"), 5, labels=False)
    out["h20 in-regime by rally quintile, clustered"] = tab(r, "rq5")
    out["in-regime rally vs ex spearman"] = float(r[["rally", "ex"]].corr(method="spearman").iloc[0, 1])
    u = g[g.regime != "mean_reversion"].copy()
    u["pq"] = pd.qcut(u["past20"].rank(method="first"), 3, labels=False)
    out["h20 out-of-regime by past20 tercile, clustered"] = tab(u, "pq")
    r["pq"] = pd.qcut(r["past20"].rank(method="first"), 3, labels=False)
    out["h20 in-regime by past20 tercile, clustered"] = tab(r, "pq")
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin drift on the 7-bar grid over all windows
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r30 = c / c.shift(30) - 1
            r7p = c / c.shift(7) - 1
            r1 = c / c.shift(1) - 1
            vol30 = r1.rolling(30).std()
            rng = (b["high"] - b["low"]) / b["close"]
            closepos = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            for i in range(0, n, 7):
                rows.append(dict(coin=coin, w=w, i=i, ts=b["timestamp"].iloc[i],
                                 regime=b["regime"].iloc[i], fc=b["forecast"].iloc[i],
                                 r30=r30.iloc[i], r7p=r7p.iloc[i], r1=r1.iloc[i],
                                 vol30=vol30.iloc[i], rng=rng.iloc[i], cp=closepos.iloc[i],
                                 fwd7=fwd7.iloc[i]))
    g = pd.DataFrame(rows)
    g["ts"] = pd.to_datetime(g["ts"])
    drift = g.groupby("coin")["fwd7"].mean()
    g["ex7"] = g["fwd7"] - g["coin"].map(drift)
    g["day"] = g["ts"].dt.floor("D")
    g["year"] = g["ts"].dt.year
    g["chop"] = g["regime"] == "unknown"
    vmed = g.groupby("coin")["vol30"].median()
    g["agit"] = g["vol30"] > g["coin"].map(vmed)
    out = {}
    def summ(df, key):
        d = df.dropna(subset=["ex7", key])
        res = d.groupby(key)["ex7"].agg(["mean", "count", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res
    for name, sub in [("chop", g[g.chop]), ("notchop", g[~g.chop])]:
        d = sub.dropna(subset=["r30", "ex7"]).copy()
        d["q"] = pd.qcut(d["r30"], 5, labels=False, duplicates="drop")
        out[f"r30 quintile -> ex7, {name}"] = summ(d, "q")
        d2 = sub.dropna(subset=["r7p", "ex7"]).copy()
        d2["q"] = pd.qcut(d2["r7p"], 5, labels=False, duplicates="drop")
        out[f"r7past quintile -> ex7, {name}"] = summ(d2, "q")
    # chop, r30 sign x agitation
    d = g[g.chop].dropna(subset=["r30", "ex7"]).copy()
    d["side"] = np.where(d.r30 < 0, "fall", "rise")
    d["cell"] = d["side"] + "_" + np.where(d.agit, "agit", "calm")
    out["chop r30 side x agitation -> ex7"] = summ(d, "cell")
    # slope r30 -> ex7 by cell
    sl = {}
    for k, s in d.groupby("cell"):
        if len(s) > 20:
            r = stats.linregress(s["r30"], s["ex7"]); sl[k] = (r.slope, r.slope / r.stderr, len(s))
    out["chop slope ex7 on r30 by cell (slope,t,n)"] = pd.DataFrame(sl, index=["slope", "t", "n"]).T
    d["yr"] = d["year"]
    out["chop fall cases by year"] = summ(d[d.side == "fall"], "yr")
    # last-day move and range, all bars
    d3 = g.dropna(subset=["r1", "ex7"]).copy()
    d3["q"] = pd.qcut(d3["r1"] / d3["vol30"], 5, labels=False, duplicates="drop")
    out["scaled last day quintile -> ex7 all"] = summ(d3, "q")
    d3["cpq"] = pd.qcut(d3["cp"], 5, labels=False, duplicates="drop")
    out["close position quintile -> ex7 all"] = summ(d3, "cpq")
    # book daily
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    D = pd.concat(days)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["wd"] = bk["day"].dt.dayofweek; bk["yr"] = bk["day"].dt.year
    out["book by window"] = bk.groupby("w")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["coin return by weekday"] = bk.groupby("wd")["coin_return"].agg(["mean", "count", "std"]).assign(
        t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    return out

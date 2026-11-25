def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    daily = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            ret7 = c / c.shift(7) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            vol = r1.rolling(30).std()
            volpct = vol.rolling(100, min_periods=40).apply(lambda x: (x[:-1] < x[-1]).mean() if len(x) > 1 else np.nan, raw=True)
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            z7 = ret7 / (vol * np.sqrt(7))
            z1 = r1 / vol
            ret30 = c / c.shift(30) - 1
            fc = df["forecast"].reset_index(drop=True)
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(c)), "ret7": ret7, "er": er,
                              "vol": vol, "volpct": volpct, "fwd7": fwd7, "z7": z7, "z30": ret30/(vol*np.sqrt(30)),
                              "fc": fc, "wd": ts.dt.weekday, "z1": z1, "fwd1": fwd1, "r1": r1})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 7 == 0].dropna(subset=["fwd7"]).copy()
    drift = G.groupby("coin")["fwd7"].mean()
    G["u7"] = G["fwd7"] - G["coin"].map(drift)
    G = G.dropna(subset=["z7", "er"])
    def summ(g):
        x = g["u7"]; n = len(x)
        return pd.Series({"n": n, "mean_u7": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan,
                          "mean_z7": g["z7"].mean()})
    out = {}
    G["z7q"] = pd.qcut(G["z7"], 5, labels=False)
    out["u7 by z7 quintile (all)"] = G.groupby("z7q").apply(summ)
    G["chop"] = np.where(G["er"] < 0.3, "chop", "trend")
    out["u7 by z7 quintile x chop"] = G.groupby(["chop", "z7q"]).apply(summ)
    Gv = G.dropna(subset=["volpct"]).copy()
    Gv["agit"] = np.where(Gv["volpct"] >= 0.5, "agit", "calm")
    out["u7 by chop x agit x sign"] = Gv.groupby(["chop", "agit", Gv["z7"] > 0]).apply(summ)
    # slope of u7 on z7 by regime
    sl = []
    for k, g in Gv.groupby(["chop", "agit"]):
        r = stats.linregress(g["z7"], g["u7"]); sl.append({"reg": str(k), "n": len(g), "slope": r.slope, "t": r.slope/r.stderr})
    out["slope u7~z7 by regime"] = pd.DataFrame(sl)
    G["z30q"] = pd.qcut(G["z30"], 5, labels=False)
    out["u7 by z30 quintile"] = G.groupby("z30q").apply(summ)
    G["volq"] = pd.qcut(G["vol"].rank(pct=True), 3, labels=False)
    out["u7 by vol tercile (raw vol)"] = G.groupby("volq").apply(summ)
    out["u7 by er quintile"] = G.groupby(pd.qcut(G["er"], 5, labels=False)).apply(summ)
    # daily: weekday, large moves
    A2 = A.dropna(subset=["fwd1"]).copy()
    A2["u1"] = A2["fwd1"] - A2["coin"].map(A2.groupby("coin")["fwd1"].mean())
    wd = A2.groupby("wd")["u1"].agg(["count", "mean", "std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["next-day u by weekday of signal"] = wd
    A3 = A2.dropna(subset=["z1"]).copy()
    A3["z1b"] = pd.cut(A3["z1"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    g = A3.groupby("z1b")["u1"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next-day u by today's z"] = g
    # largest 1-day move -> next 7 days on grid
    G["z1b"] = pd.cut(G["z1"], [-99, -2, -1, 1, 2, 99])
    out["u7 by today's z1"] = G.groupby("z1b").apply(summ)
    # book days
    bk = []
    for coin, wins in days.items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk).dropna(subset=["book_return"])
    bd = B.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    out["book by window"] = bd.groupby("w").agg(n=("book_return", "size"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    q = bd["book_return"].quantile([0.02, 0.98])
    out["coin ret on book extreme days"] = pd.DataFrame({
        "worst2%": bd[bd.book_return <= q.iloc[0]][["book_return", "coin_return"]].mean(),
        "best2%": bd[bd.book_return >= q.iloc[1]][["book_return", "coin_return"]].mean()})
    return out

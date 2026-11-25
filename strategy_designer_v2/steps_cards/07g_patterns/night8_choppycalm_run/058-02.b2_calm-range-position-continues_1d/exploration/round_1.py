def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = 2 * (c - lo) / (hi - lo) - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            ret1 = r1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "pos": pos, "fwd": fwd, "fwd1": fwd1,
                               "inprof": (b["regime"] == "unknown").astype(int), "volratio": vol20 / vol60,
                               "vol20": vol20, "ret20": ret20, "ret60": ret60, "ret1": ret1, "ret1z": ret1 / vol20,
                               "wd": ts.dt.weekday, "year": ts.dt.year, "fc": b["forecast"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.i % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.i % H == 0)].dropna(subset=["ex", "pos"])
    out = {}
    def tbl(df, key, col="ex"):
        g = df.groupby(key)[col]
        r = pd.DataFrame({"n": g.size(), "mean%": g.mean() * 100, "t": g.mean() / (g.std() / np.sqrt(g.size()))})
        return r.round(3)
    G["posq"] = pd.cut(G["pos"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out["pos bins in profile"] = tbl(G[G.inprof == 1], "posq")
    out["pos bins out of profile"] = tbl(G[G.inprof == 0], "posq")
    G2 = G.dropna(subset=["ret60"]).copy()
    G2["trend"] = pd.cut(G2["ret60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G2["vq"] = pd.qcut(G2["volratio"], 2, labels=["calmer", "agit"])
    def slope(df):
        if len(df) < 30: return pd.Series({"n": len(df), "slope%": np.nan, "t": np.nan})
        s = stats.linregress(df["pos"], df["ex"])
        return pd.Series({"n": len(df), "slope%": s.slope * 100, "t": s.slope / s.stderr})
    out["slope pos by trend x volratio"] = G2.groupby(["trend", "vq"]).apply(slope).round(3)
    G["r20q"] = pd.qcut(G["ret20"], 5)
    out["20d return quintiles fwd5 ex"] = tbl(G.dropna(subset=["r20q"]), "r20q")
    G["r1zq"] = pd.qcut(G["ret1z"], 5)
    out["1d z-move quintiles fwd5 ex"] = tbl(G.dropna(subset=["r1zq"]), "r1zq")
    G["vq5"] = pd.qcut(G["volratio"], 5)
    out["volratio quintiles fwd5 ex"] = tbl(G.dropna(subset=["vq5"]), "vq5")
    A1 = A.dropna(subset=["fwd1"])
    A1["fwd1ex"] = A1["fwd1"] - A1["coin"].map(A1.groupby("coin")["fwd1"].mean())
    out["weekday next-day ex"] = tbl(A1, "wd", "fwd1ex")
    out["year fwd5 ex by pos sign in profile"] = G[G.inprof == 1].assign(s=np.sign(G["pos"])).groupby(["year", "s"])["ex"].agg(["size", "mean"]).round(4)
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["year"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book by window"] = bk.groupby(level="w").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean")).round(5)
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book extreme days"] = pd.Series({"low_n": (bk.book_return < q.iloc[0]).sum(), "low_sum": bk.book_return[bk.book_return < q.iloc[0]].sum(),
                                          "high_n": (bk.book_return > q.iloc[1]).sum(), "high_sum": bk.book_return[bk.book_return > q.iloc[1]].sum(),
                                          "total_sum": bk.book_return.sum()}).round(4)
    out["share in profile"] = float(A.inprof.mean())
    return out

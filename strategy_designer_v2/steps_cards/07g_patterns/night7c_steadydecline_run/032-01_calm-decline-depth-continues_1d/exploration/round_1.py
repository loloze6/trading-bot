def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    rows = []
    rows1 = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            rng = (d["high"] - d["low"]).astype(float) / c
            vol = d["volume"].astype(float)
            f = pd.DataFrame({"ts": pd.to_datetime(d["timestamp"])})
            f["coin"] = coin; f["w"] = w
            f["r28"] = c / c.shift(28) - 1
            f["r7"] = c / c.shift(7) - 1
            f["r1"] = c / c.shift(1) - 1
            f["rr"] = rng.rolling(7).mean() / rng.rolling(28).mean()
            f["vr"] = vol.rolling(7).mean() / vol.rolling(28).mean()
            f["vsp"] = vol / vol.rolling(28).mean()
            f["calm"] = (d["regime"] == "trending").astype(int)
            f["fc"] = d["forecast"].astype(float)
            f["fwd5"] = c.shift(-H) / c - 1
            f["fwd1"] = c.shift(-1) / c - 1
            f["pos"] = d["postRebalance_current_allocation"].astype(float)
            g = f.iloc[::H].copy()
            rows.append(g)
            rows1.append(f)
    G = pd.concat(rows); A = pd.concat(rows1)
    G = G.dropna(subset=["fwd5"])
    G["ex"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    A = A.dropna(subset=["fwd1"])
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    A["day"] = A["ts"].dt.floor("D"); G["day"] = G["ts"].dt.floor("D")

    def tday(df, col):
        s = df.groupby("day")[col].sum()
        n = df.groupby("day")[col].size()
        m = s.sum() / n.sum()
        dev = (df[col] - m).groupby(df["day"]).sum()
        se = np.sqrt((dev**2).sum()) / n.sum()
        return m, m / se if se > 0 else np.nan, len(s)

    def bucket(df, var, col, q=5):
        d = df.dropna(subset=[var, col]).copy()
        d["b"] = d.groupby("coin")[var].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        out = []
        for b, x in d.groupby("b"):
            m, t, n = tday(x, col)
            out.append({"bucket": b, "mean_var": x[var].mean(), "mean_ex": m, "t": t, "days": n, "cases": len(x)})
        return pd.DataFrame(out)

    res = {}
    res["r28 quint -> ex5 (all)"] = bucket(G, "r28", "ex")
    res["r28 quint -> ex5 calm"] = bucket(G[G.calm == 1], "r28", "ex", 3)
    res["r28 quint -> ex5 notcalm"] = bucket(G[G.calm == 0], "r28", "ex")
    res["r7 quint -> ex5"] = bucket(G, "r7", "ex")
    res["rangeratio quint -> ex5"] = bucket(G, "rr", "ex")
    res["volratio quint -> ex5"] = bucket(G, "vr", "ex")
    res["volspike quint -> ex5"] = bucket(G, "vsp", "ex")
    res["r1 quint -> ex1 (all bars)"] = bucket(A, "r1", "ex1")
    A["wd"] = A["ts"].dt.dayofweek
    wd = A.groupby("wd")["fwd1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    res["next-day return by weekday of signal bar"] = wd
    # r28 x rr interaction
    d = G.dropna(subset=["r28", "rr"]).copy()
    d["neg28"] = (d.r28 < 0).astype(int)
    d["hirr"] = (d.rr > d.groupby("coin")["rr"].transform("median")).astype(int)
    out = []
    for k, x in d.groupby(["neg28", "hirr"]):
        m, t, n = tday(x, "ex")
        out.append({"neg28": k[0], "hirange": k[1], "mean_ex": m, "t": t, "days": n})
    res["fall x range expansion"] = pd.DataFrame(out)
    # book: by window
    days = data["days"]
    bw = []
    for coin, ws in days.items():
        for w, df in ws.items():
            bw.append({"coin": coin, "w": w, "book": df["book_return"].sum(), "coin_ret": df["coin_return"].sum()})
    bw = pd.DataFrame(bw)
    res["book by window"] = bw.groupby("w")[["book", "coin_ret"]].mean()
    res["share calm"] = float(A["calm"].mean())
    return res

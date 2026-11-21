def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = 5
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            s = pd.Series(c)
            lr = np.log(s).diff()
            r1 = s.pct_change()
            r5 = s.pct_change(5)
            r30 = s.pct_change(30)
            r10 = s.pct_change(10)
            vol20 = lr.rolling(20).std()
            vol60 = lr.rolling(60, min_periods=30).std()
            hi30 = s.rolling(30).max()
            lo30 = s.rolling(30).min()
            pos30 = (s - lo30) / (hi30 - lo30)
            f = b["forecast"].astype(float)
            alloc = b["postRebalance_current_allocation"].astype(float)
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, f=f.iloc[t], al=alloc.iloc[t],
                    r1=r1.iloc[t], r5=r5.iloc[t], r10=r10.iloc[t], r30=r30.iloc[t],
                    vr=vol20.iloc[t] / vol60.iloc[t] if vol60.iloc[t] else np.nan,
                    vol=vol20.iloc[t], pos=pos30.iloc[t], wd=wd.iloc[t],
                    fwd=c[t + H] / c[t] - 1,
                    fwd10=(c[t + 10] / c[t] - 1) if t + 10 < n else np.nan,
                    fwd20=(c[t + 20] / c[t] - 1) if t + 20 < n else np.nan))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["ex10"] = df["fwd10"] - df.groupby("coin")["fwd10"].transform("mean")
    df["ex20"] = df["fwd20"] - df.groupby("coin")["fwd20"].transform("mean")
    out = {}
    def bucket(col, q=5, target="ex"):
        d = df.dropna(subset=[col, target]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        g = d.groupby("q")[target].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.round(5)
    def slope(col, target="ex", sub=None):
        d = (df if sub is None else sub).dropna(subset=[col, target])
        z = d.groupby("coin")[col].transform(lambda x: (x - x.mean()) / x.std())
        r = stats.linregress(z, d[target])
        return (round(r.slope, 5), round(r.slope / r.stderr, 2), len(d))
    out["forecast quintile -> ex5"] = bucket("f")
    out["r30 quintile -> ex20"] = bucket("r30", target="ex20")
    sl = {}
    for col in ["f", "r30", "r10", "r5", "r1", "vr", "vol", "pos"]:
        for tg in ["ex", "ex10", "ex20"]:
            sl[f"{col}->{tg}"] = slope(col, tg)
    out["slopes (slope,t,n)"] = pd.DataFrame(sl, index=["slope", "t", "n"]).T
    out["r5 quintile -> ex5"] = bucket("r5")
    out["pos30 quintile -> ex5"] = bucket("pos")
    out["volratio quintile -> ex5"] = bucket("vr")
    # momentum slope by vol regime
    d = df.dropna(subset=["vol", "r30", "ex"]).copy()
    d["hv"] = d.groupby("coin")["vol"].transform(lambda x: x > x.median())
    out["r30 slope high vol"] = str(slope("r30", "ex", d[d.hv]))
    out["r30 slope low vol"] = str(slope("r30", "ex", d[~d.hv]))
    d["up"] = d["r30"] > 0
    out["ex5 by sign of r30, by vol"] = d.groupby(["hv", "up"])["ex"].agg(["mean", "count"]).round(5)
    # per coin
    pc = {}
    for coin, g in df.groupby("coin"):
        pc[coin] = slope("r30", "ex", g)
    out["r30 slope per coin"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T
    # long vs short side gain
    df["pg"] = df["al"] * df["fwd"]
    out["book gain by side (grid)"] = df.assign(side=np.sign(df["al"])).groupby("side")["pg"].agg(["mean", "count"]).round(5)
    # book daily returns: drawdowns, by year
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"])
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    B["year"] = B.index.get_level_values("day").year
    yr = B.groupby("year").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    yr["book_sh"] = B.groupby("year")["book_return"].apply(lambda x: x.mean() / x.std() * np.sqrt(365))
    out["book by year"] = yr.round(5)
    wn = B.groupby(level="w").agg(book=("book_return", "mean"), hold=("coin_return", "mean"))
    wn["cum_book"] = B.groupby(level="w")["book_return"].apply(lambda x: (1 + x).prod() - 1)
    out["book by window"] = wn.round(4)
    return out

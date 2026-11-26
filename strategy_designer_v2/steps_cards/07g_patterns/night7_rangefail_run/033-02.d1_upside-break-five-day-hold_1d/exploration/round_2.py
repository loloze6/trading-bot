def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 5
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            hh = hi.shift(1).rolling(20).max(); ll = lo.shift(1).rolling(20).min()
            rp = (c - ll) / (hh - ll)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)), "day": ts.dt.floor("D"),
                              "year": ts.dt.year, "rp": rp, "dhi": c / hh - 1,
                              "r20p": c / c.shift(20) - 1, "r60p": c / c.shift(60) - 1,
                              "vol20": vol20, "fwd": c.shift(-H) / c - 1,
                              "fwd1": c.shift(-1) / c - 1,
                              "alloc": df["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["volr"] = A.groupby("coin")["vol20"].rank(pct=True)
    A["calm"] = np.where(A["volr"] <= 0.5, "calm", "agit")
    G = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["u"] = G["fwd"] - G["coin"].map(drift)

    def tstat(g, col="u"):
        s = g.groupby("day")[col].sum(); n = len(s)
        t = s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return len(g), n, 100 * g[col].mean(), t

    def tab(df, keys, col="u"):
        out = []
        for k, g in df.dropna(subset=[col]).groupby(keys, observed=True):
            n, nd, m, t = tstat(g, col)
            out.append({"k": str(k), "n": n, "days": nd, "mean_u%": m, "t_day": t})
        return pd.DataFrame(out)

    res = {}
    G["rp_bin"] = pd.cut(G["rp"], [-np.inf, 0.2, 0.4, 0.6, 0.8, 1, np.inf])
    res["rangepos_by_calm"] = tab(G.dropna(subset=["rp_bin"]), ["calm", "rp_bin"])
    # slope of u on rp by calm
    out = []
    for k, g in G.dropna(subset=["rp"]).groupby("calm"):
        x = g["rp"].clip(-0.5, 1.5); y = g["u"]
        b = np.polyfit(x, y, 1)[0]
        r = np.corrcoef(x, y)[0, 1]; n = len(g)
        out.append({"calm": k, "n": n, "slope%": 100 * b, "corr": r, "t": r * np.sqrt((n - 2) / (1 - r * r))})
    res["rp_slope_by_calm"] = pd.DataFrame(out)
    G["r20q"] = pd.qcut(G["r20p"], 5, labels=False)
    res["r20q_by_year"] = G.dropna(subset=["r20q"]).groupby(["r20q", "year"])["u"].mean().unstack() * 100
    G["tr"] = pd.cut(G["r60p"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    res["rangepos_by_trend60"] = tab(G.dropna(subset=["rp_bin", "tr"]), ["tr", "rp_bin"])
    # breaks: by calm and trend
    B = G[G["dhi"] > 0]
    res["break_by_calm"] = tab(B, ["calm"])
    res["break_by_trend60"] = tab(B.dropna(subset=["tr"]), ["tr"])
    res["break_by_year"] = tab(B, ["year"])
    # book: daily returns, largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["w"] = w; D.append(x)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    bk["q"] = pd.qcut(bk["br"].rank(method="first"), 10, labels=False)
    res["book_deciles"] = bk.groupby("q").agg(n=("br", "size"), book=("br", lambda x: 100 * x.mean()),
                                             coin=("cr", lambda x: 100 * x.mean()))
    # positions by age: return of held bars by days since entry
    A["held"] = A["alloc"].abs() > 1e-6
    A["g1"] = A["alloc"] * A["fwd1"]
    ages = []
    for (coin, w), g in A.groupby(["coin", "w"]):
        h = g["held"].values; a = np.zeros(len(h)); cnt = 0
        for i in range(len(h)):
            cnt = cnt + 1 if h[i] else 0; a[i] = cnt
        ages.append(pd.Series(a, index=g.index))
    A["age"] = pd.concat(ages)
    A["ageb"] = pd.cut(A["age"], [0, 5, 10, 20, 1000])
    H1 = A[A["held"]].dropna(subset=["fwd1"])
    H1 = H1.assign(u1=H1["fwd1"] - H1["coin"].map(A.groupby("coin")["fwd1"].mean()))
    res["held_by_age"] = H1.groupby("ageb", observed=True).agg(n=("g1", "size"),
        gain_bp=("g1", lambda x: 1e4 * x.mean()), u1_bp=("u1", lambda x: 1e4 * x.mean()),
        t=("u1", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    return res

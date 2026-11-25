def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi20 = c.rolling(20, min_periods=20).max(); lo20 = c.rolling(20, min_periods=20).min()
            pos = (c - lo20) / (hi20 - lo20)
            r1 = c.pct_change()
            r5b = c / c.shift(5) - 1
            r20b = c / c.shift(20) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"])
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "win": w, "i": idx, "pos": pos, "r1": r1, "r5b": r5b,
                               "r20b": r20b, "vol20": vol20, "rng": rng, "clv": clv, "fwd": fwd, "fwd1": fwd1,
                               "fc": b["debug_info.components.range_pos.post_pipeline_value"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "volz": vol20 / vol20.rolling(60, min_periods=30).mean()})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin on grid
    G = A[(A["i"] % H == 0) & A["fwd"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    sd = G.groupby("coin")["fwd"].std()
    G["exs"] = G["ex"] / G["coin"].map(sd)
    out = {}
    def tab(g, key):
        t = g.groupby(key, observed=True)["ex"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    Gp = G.dropna(subset=["pos"]).copy()
    Gp["posq"] = pd.cut(Gp["pos"], [-0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.999, 1.0])
    out["ex5 by range position"] = tab(Gp, "posq")
    out["ex5 by year"] = tab(Gp, "yr")
    # slope of ex on pos by year and coin
    def slope(g):
        g = g.dropna(subset=["pos", "ex"])
        if len(g) < 30: return pd.Series({"n": len(g)})
        s = stats.linregress(g["pos"], g["ex"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope ex~pos by year"] = Gp.groupby("yr").apply(slope).round(4)
    out["slope ex~pos by coin"] = Gp.groupby("coin").apply(slope).round(4)
    out["slope ex~pos by window"] = Gp.groupby("win").apply(slope).round(4)
    # 20d trend, vol regime
    Gt = Gp.dropna(subset=["r20b"]).copy()
    Gt["tr"] = pd.cut(Gt["r20b"], [-9, -0.15, -0.05, 0.05, 0.15, 9])
    out["slope ex~pos by 20d trend"] = Gt.groupby("tr", observed=True).apply(slope).round(4)
    out["ex5 by 20d trend"] = tab(Gt, "tr")
    Gv = Gp.dropna(subset=["volz"]).copy()
    Gv["vq"] = pd.qcut(Gv["volz"], 3, labels=["calm", "mid", "agit"])
    out["slope ex~pos by vol level"] = Gv.groupby("vq", observed=True).apply(slope).round(4)
    # after large 1d moves (standardised)
    G2 = G.dropna(subset=["r1", "vol20"]).copy()
    G2["z1"] = G2["r1"] / G2["vol20"]
    G2["zq"] = pd.cut(G2["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["ex5 after 1d move z"] = tab(G2, "zq")
    G2["r5q"] = pd.qcut(G2["r5b"], 5)
    out["ex5 by past 5d return quintile"] = tab(G2.dropna(subset=["r5b"]), "r5q")
    G2["clq"] = pd.cut(G2["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.0])
    out["ex5 by close location in day bar"] = tab(G2.dropna(subset=["clv"]), "clq")
    G2["rgq"] = pd.qcut(G2["rng"] / G2["vol20"], 4)
    out["ex5 by day range / vol quartile"] = tab(G2.dropna(subset=["rng"]), "rgq")
    # weekday next-day return (all bars)
    A1 = A.dropna(subset=["fwd1"]).copy()
    A1["ex"] = A1["fwd1"] - A1["coin"].map(A1.groupby("coin")["fwd1"].mean())
    out["next 1d ex by weekday of signal bar"] = tab(A1, "wd")
    # book: position gain by pos bucket
    A1["gain"] = A1["alloc"] * A1["fwd1"]
    Ap = A1.dropna(subset=["pos"]).copy()
    Ap["posq"] = pd.cut(Ap["pos"], [-0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.999, 1.0])
    out["book gain per bar by pos bucket"] = Ap.groupby("posq", observed=True)["gain"].agg(["count", "mean", "sum"]).round(5)
    # book daily largest gains/losses: what preceded
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bd = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bd["book_return"].quantile([0.05, 0.95])
    out["book worst5% vs best5% days: mean coin ret"] = pd.DataFrame({
        "worst": bd[bd["book_return"] <= q.iloc[0]].mean(), "best": bd[bd["book_return"] >= q.iloc[1]].mean(),
        "n": [ (bd["book_return"] <= q.iloc[0]).sum()]*2}).round(4)
    out["book corr with coin mean daily"] = float(bd.corr().iloc[0, 1])
    return out

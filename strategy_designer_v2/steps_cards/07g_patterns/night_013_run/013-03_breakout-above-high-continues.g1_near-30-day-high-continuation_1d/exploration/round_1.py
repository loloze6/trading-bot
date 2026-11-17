def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ph = h.shift(1).rolling(30, min_periods=30).max()
            dist = (c - ph) / ph * 100
            r10p = c / c.shift(10) - 1
            r30p = c / c.shift(30) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            vrel = v / v.rolling(30, min_periods=20).mean()
            fwd10 = c.shift(-10) / c - 1
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "dist": dist, "r1": r1, "r10p": r10p,
                               "r30p": r30p, "vol20": vol20, "vrel": vrel, "fwd10": fwd10, "fwd5": fwd5, "fwd1": fwd1,
                               "fc": b["forecast"].astype(float), "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["ex10"] = D["fwd10"] - D.groupby("coin")["fwd10"].transform("mean")
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    S = D[(D["pos"] % 10 == 0)].dropna(subset=["ex10"])
    out = {}
    def qtab(col, q=5, data_=S, y="ex10"):
        d = data_.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        g = d.groupby("q")[y].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["xmean"] = d.groupby("q")[col].mean()
        return g.round(4)
    out["dist_quint_ex10"] = qtab("dist")
    out["r10p_quint_ex10"] = qtab("r10p")
    out["r30p_quint_ex10"] = qtab("r30p")
    out["vol20_quint_ex10"] = qtab("vol20")
    out["vrel_quint_ex10"] = qtab("vrel")
    # dist effect per coin
    pc = []
    for coin, d in S.dropna(subset=["dist"]).groupby("coin"):
        sl = stats.linregress(d["dist"], d["ex10"])
        pc.append({"coin": coin, "slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(d)})
    out["dist_slope_by_coin"] = pd.DataFrame(pc).round(4)
    # dist interacted with volume: near high (top dist quintile) split by vrel
    d = S.dropna(subset=["dist", "vrel"]).copy()
    d["near"] = d["dist"] > d.groupby("coin")["dist"].transform(lambda x: x.quantile(0.6))
    d["hv"] = d["vrel"] > d.groupby("coin")["vrel"].transform("median")
    out["near_x_highvol_ex10"] = d.groupby(["near", "hv"])["ex10"].agg(["mean", "count"]).round(4)
    # daily 1-day: big moves -> next day
    E = D.dropna(subset=["r1", "ex1", "vol20"]).copy()
    E["z"] = E["r1"] / E["vol20"]
    E["zb"] = pd.cut(E["z"], [-99, -2, -1, 0, 1, 2, 99])
    g = E.groupby("zb")["ex1"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["next_day_after_zmove"] = g.round(5)
    g = E.groupby("wd")["ex1"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_ex1"] = g.round(5)
    # book attribution
    dd = []
    for coin in days:
        for w, x in days[coin].items():
            dd.append(x.assign(coin=coin, w=w))
    Y = pd.concat(dd, ignore_index=True)
    bk = Y.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bw = bk.groupby(level=0).agg(["mean"]); 
    wtab = Y.groupby("w")[["book_return", "coin_return"]].mean()
    out["by_window_book_vs_coin_x1e4"] = (wtab * 1e4).round(2)
    # alloc stats
    out["alloc_desc"] = D["alloc"].describe().round(3)
    out["corr_alloc_dist"] = float(D[["alloc", "dist"]].dropna().corr().iloc[0, 1])
    # bars: book gain by dist quintile on daily level
    D["gain"] = D["alloc"] * D["fwd1"]
    Dq = D.dropna(subset=["dist", "gain"]).copy()
    Dq["q"] = Dq.groupby("coin")["dist"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["daily_gain_by_dist_q"] = Dq.groupby("q").agg(gain=("gain", "mean"), alloc=("alloc", "mean"), fwd1=("ex1", "mean"), n=("gain", "count")).round(5)
    return out

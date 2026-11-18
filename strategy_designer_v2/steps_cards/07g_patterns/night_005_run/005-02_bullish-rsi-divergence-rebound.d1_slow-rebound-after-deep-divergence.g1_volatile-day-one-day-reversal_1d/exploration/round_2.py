def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            z = r / sd
            vr = sd / sd.rolling(60, min_periods=20).mean()
            nxt = c.shift(-1)/c - 1
            nxt3 = c.shift(-3)/c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z, "vr": vr,
                               "nxt": nxt, "nxt3": nxt3,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["vrq"] = pd.qcut(d["vr"], 4, labels=["q1", "q2", "q3", "q4"])
    def slope(g, x, y):
        g = g[[x, y]].dropna()
        if len(g) < 30: return (np.nan, np.nan, len(g))
        res = stats.linregress(g[x], g[y]); return (res.slope, res.slope/res.stderr, len(g))
    t = []
    for (coin, q), g in d.groupby(["coin", "vrq"], observed=True):
        t.append([coin, q, *slope(g, "z", "ex")])
    out["per coin slope by vr quartile"] = pd.DataFrame(t, columns=["coin", "q", "slope", "t", "n"])
    t = []
    for q, g in d.groupby("vrq", observed=True):
        for side in ["up", "down"]:
            gg = g[(g.z > 0) if side == "up" else (g.z < 0)]
            t.append([q, side, *slope(gg, "z", "ex"), gg.ex.mean()])
    out["side x vr quartile"] = pd.DataFrame(t, columns=["q", "side", "slope", "t", "n", "mean_ex"])
    # down day severity x vr: next ex mean when z<-1 by vrq
    out["z<-1 next ex by vrq"] = d[d.z < -1].groupby("vrq", observed=True)["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["z>1 next ex by vrq"] = d[d.z > 1].groupby("vrq", observed=True)["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # low vol 3d continuation per coin
    g3 = d[d.pos % 3 == 0].copy()
    g3["ex3"] = g3["nxt3"] - g3.groupby("coin")["nxt3"].transform("mean")
    t = []
    for coin, g in g3[g3.vr < 1].groupby("coin"):
        t.append([coin, *slope(g, "z", "ex3")])
    for q, g in g3.groupby("vrq", observed=True):
        t.append([q, *slope(g, "z", "ex3")])
    out["3d slope z by coin (lowvol) and vrq"] = pd.DataFrame(t, columns=["grp", "slope", "t", "n"])
    # book decomposition
    mu = d.groupby("coin")["nxt"].transform("mean")
    d["mkt"] = d.alloc*mu; d["pnl"] = d.alloc*d.nxt
    out["book decomposition per bar"] = pd.Series({"pnl": d.pnl.mean(), "market_part": d.mkt.mean(), "timing": (d.pnl - d.mkt).mean()})
    # book days: largest losses / gains, coin return before and after
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.reset_index(drop=True).copy()
            x["prev_coin"] = x.coin_return.shift(1); x["next_coin"] = x.coin_return.shift(-1)
            x["coin"] = coin; dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return"])
    lo = D.book_return.quantile(0.02); hi = D.book_return.quantile(0.98)
    out["around book extremes"] = pd.DataFrame({
        "worst2%": D[D.book_return <= lo][["book_return", "coin_return", "prev_coin", "next_coin"]].mean(),
        "best2%": D[D.book_return >= hi][["book_return", "coin_return", "prev_coin", "next_coin"]].mean()})
    out["worst2% share coin up"] = float((D[D.book_return <= lo].coin_return > 0).mean())
    return out

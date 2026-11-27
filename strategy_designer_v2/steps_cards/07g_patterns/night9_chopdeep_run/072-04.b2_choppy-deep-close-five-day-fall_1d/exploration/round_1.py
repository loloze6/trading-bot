def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            f1 = c.shift(-1) / c - 1
            f5 = c.shift(-5) / c - 1
            f2 = c.shift(-2) / c - 1
            sd20 = r1.rolling(20).std()
            hi20 = c.rolling(20).max()
            depth = (c / hi20 - 1) / sd20
            lo20 = c.rolling(20).min()
            rngpos = (c - lo20) / (hi20 - lo20)
            ret5p = c / c.shift(5) - 1
            ret20p = c / c.shift(20) - 1
            vol_rel = sd20 / r1.rolling(60).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n), "regime": b["regime"].values,
                              "fc": b["forecast"].values, "alloc": b["postRebalance_current_allocation"].values,
                              "r1": r1, "f1": f1, "f2": f2, "f5": f5, "depth": depth, "rngpos": rngpos,
                              "ret5p": ret5p / sd20, "ret20p": ret20p, "vol_rel": vol_rel,
                              "wd": ts.dt.weekday.values, "year": ts.dt.year.values,
                              "day": ts.dt.floor("D").values})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin
    g5 = D[D.pos % 5 == 0].dropna(subset=["f5"])
    drift5 = g5.groupby("coin")["f5"].mean()
    drift1 = D.dropna(subset=["f1"]).groupby("coin")["f1"].mean()
    D["x5"] = D["f5"] - D.coin.map(drift5)
    D["x1"] = D["f1"] - D.coin.map(drift1)
    D["choppy"] = D.regime == "unknown"
    out["regime share"] = D.regime.value_counts(normalize=True)
    def tab(sub, col, ycol, q=5):
        s = sub.dropna(subset=[col, ycol]).copy()
        s["b"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        t = s.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), mean=(ycol, "mean"), sd=(ycol, "std"), n=(ycol, "size"))
        t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")
    G5 = D[D.pos % 5 == 0]
    out["choppy depth -> x5 (grid)"] = tab(G5[G5.choppy], "depth", "x5")
    out["nonchoppy depth -> x5 (grid)"] = tab(G5[~G5.choppy], "depth", "x5")
    out["choppy depth -> x1"] = tab(D[D.choppy], "depth", "x1")
    out["nonchoppy depth -> x1"] = tab(D[~D.choppy], "depth", "x1")
    out["all ret5p(sd units) -> x5 grid"] = tab(G5, "ret5p", "x5")
    out["all r1 -> x1"] = tab(D.assign(r1z=D.r1), "r1z", "x1")
    out["all vol_rel -> x5 grid"] = tab(G5, "vol_rel", "x5")
    out["all rngpos -> x5 grid"] = tab(G5, "rngpos", "x5")
    out["weekday -> x1"] = D.dropna(subset=["x1"]).groupby("wd")["x1"].agg(["mean", "count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    DD = pd.concat(dd)
    bk = DD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    # positions: realized short pnl by depth bucket
    D["pnl"] = D["alloc"] * D["f1"]
    act = D[D.alloc < 0]
    out["active pnl by depth"] = tab(act, "depth", "pnl")
    out["active pnl by year"] = act.groupby("year")["pnl"].agg(["mean", "count"])
    return out

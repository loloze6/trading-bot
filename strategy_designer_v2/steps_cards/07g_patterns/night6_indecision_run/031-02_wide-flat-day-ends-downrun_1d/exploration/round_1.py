def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b.open, b.high, b.low, b.close
            rng = (h - l)
            d = pd.DataFrame({"coin": coin, "win": w})
            d["pos"] = np.arange(len(b))
            d["r1"] = c / c.shift(1) - 1
            d["r5p"] = c / c.shift(5) - 1
            d["r20p"] = c / c.shift(20) - 1
            d["rr"] = rng / rng.rolling(20).mean()
            d["flat"] = 1 - (c - o).abs() / rng.replace(0, np.nan)
            d["clv"] = (c - l) / rng.replace(0, np.nan)
            d["vol20"] = d["r1"].rolling(20).std()
            d["fwd5"] = c.shift(-5) / c - 1
            d["wd"] = pd.to_datetime(b.timestamp).dt.weekday.values
            d["fc"] = b.forecast.values
            rows.append(d)
    P = pd.concat(rows, ignore_index=True)
    G = P[(P.pos % 5 == 0) & P.fwd5.notna()].copy()
    st = G.groupby("coin").fwd5.agg(["mean", "std"])
    G["u"] = (G.fwd5 - G.coin.map(st["mean"])) / G.coin.map(st["std"])
    def q(col, k=5):
        return G.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), k, labels=False))
    def summ(key):
        g = G.dropna(subset=["u"]).groupby(key).u
        r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r[["mean", "t", "count"]].round(3)
    out = {}
    for col in ["r1", "r5p", "r20p", "rr", "flat", "clv", "vol20"]:
        G["q_" + col] = q(col)
        out["strength by quintile of " + col] = summ("q_" + col)
    out["by weekday"] = summ("wd")
    G["run"] = np.where(G.r5p > 0, "up", "down")
    G["wide"] = np.where(G.rr >= 1, "wide", "narrow")
    G["fl"] = np.where(G.flat >= 0.9, "flat", "body")
    out["run x wide x flat"] = summ(["run", "wide", "fl"])
    out["r5p quintile x vol20 tercile"] = (G.assign(vt=q("vol20", 3)).dropna(subset=["u"])
        .groupby(["q_r5p", "vt"]).u.agg(["mean", "count"]).round(3).unstack())
    out["clv quintile x rr wide"] = G.dropna(subset=["u"]).groupby(["q_clv", "wide"]).u.mean().round(3).unstack()
    out["r20p quintile by coin"] = G.groupby(["coin", "q_r20p"]).u.mean().round(2).unstack()
    T = pd.concat([t.assign(coin=k) for k, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = T.groupby("coin").net_profit_loss_percent.agg(["mean", "count"]).round(3)
    return out

def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b.open.values, b.high.values, b.low.values, b.close.values
            cs = pd.Series(c)
            rng = pd.Series(h - l)
            n = len(b)
            d = pd.DataFrame(index=range(n))
            d["coin"] = coin
            d["win"] = w
            d["pos"] = np.arange(n)
            d["r1"] = (cs / cs.shift(1) - 1).values
            d["r5p"] = (cs / cs.shift(5) - 1).values
            d["r20p"] = (cs / cs.shift(20) - 1).values
            d["rr"] = (rng / rng.rolling(20).mean()).values
            rz = rng.replace(0, np.nan)
            d["flat"] = (1 - pd.Series(np.abs(c - o)) / rz).values
            d["clv"] = ((cs - pd.Series(l)) / rz).values
            d["vol20"] = d["r1"].rolling(20).std().values
            d["fwd5"] = (cs.shift(-5) / cs - 1).values
            d["fwd1"] = (cs.shift(-1) / cs - 1).values
            ts = pd.to_datetime(b.timestamp)
            d["wd"] = ts.dt.weekday.values
            d["yr"] = ts.dt.year.values
            d["fc"] = b.forecast.values
            d["alloc"] = b.postRebalance_current_allocation.values
            rows.append(d)
    P = pd.concat(rows, ignore_index=True)
    out = {}
    G = P[(P.pos % 5 == 0) & P.fwd5.notna()].copy()
    st = G.groupby("coin").fwd5.agg(["mean", "std"])
    G["u"] = (G.fwd5 - G.coin.map(st["mean"])) / G.coin.map(st["std"])
    G["raw"] = G.fwd5 - G.coin.map(st["mean"])
    def q(df, col, k=5):
        return df.groupby("coin")[col].transform(
            lambda s: pd.qcut(s.rank(method="first"), k, labels=False) if s.notna().sum() > k else s * np.nan)
    def summ(df, key, val="u"):
        g = df.dropna(subset=[val]).groupby(key)[val]
        r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r[["mean", "t", "count"]].round(3)
    for col in ["r1", "r5p", "r20p", "rr", "flat", "clv", "vol20"]:
        try:
            G["q_" + col] = q(G, col)
            out["5d strength by quintile of " + col] = summ(G, "q_" + col)
        except Exception as e:
            out["err " + col] = str(e)[:80]
    try:
        G["run"] = np.where(G.r5p > 0, "up", "down")
        G["wide"] = np.where(G.rr >= 1, "wide", "narrow")
        G["fl"] = np.where(G.flat >= 0.9, "flat", "body")
        out["run x wide x flat (5d strength)"] = summ(G, ["run", "wide", "fl"])
    except Exception as e:
        out["err rwf"] = str(e)[:80]
    try:
        G["vt"] = q(G, "vol20", 3)
        out["r20p quintile x vol tercile mean"] = G.dropna(subset=["u"]).groupby(["q_r20p", "vt"]).u.mean().round(3).unstack()
        out["r20p top vs bottom quintile by year"] = G[G.q_r20p.isin([0, 4])].groupby(["yr", "q_r20p"]).u.mean().round(3).unstack()
        out["r20p quintile by coin"] = G.groupby(["coin", "q_r20p"]).u.mean().round(2).unstack()
        out["clv quintile x wide"] = G.dropna(subset=["u"]).groupby(["q_clv", "wide"]).u.mean().round(3).unstack()
        out["vol tercile x r5p quintile"] = G.dropna(subset=["u"]).groupby(["q_r5p", "vt"]).u.mean().round(3).unstack()
    except Exception as e:
        out["err cross"] = str(e)[:80]
    try:
        D = P.dropna(subset=["fwd1", "r1"]).copy()
        sd = D.groupby("coin").fwd1.transform("std")
        D["u1"] = (D.fwd1 - D.groupby("coin").fwd1.transform("mean")) / sd
        D["q1"] = q(D, "r1", 10)
        out["next-day strength by decile of today's return"] = summ(D, "q1", "u1")
        out["next-day strength by weekday"] = summ(D, "wd", "u1")
    except Exception as e:
        out["err daily"] = str(e)[:80]
    try:
        A = P[P.fc > 0]
        out["active bars: fwd5 raw mean, count"] = pd.Series({"mean": A.fwd5.mean(), "count": A.fwd5.notna().sum()}).round(4)
    except Exception as e:
        out["err act"] = str(e)[:80]
    try:
        T = pd.concat([t.assign(coin=k) for k, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
        out["trades by coin"] = T.groupby("coin").net_profit_loss_percent.agg(["mean", "count"]).round(3)
    except Exception as e:
        out["err trades"] = str(e)[:80]
    return out

import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    allrows = []
    for H in [3, 5, 10]:
        for coin, wins in data["bars"].items():
            frames = []
            for w, b in wins.items():
                b = b.reset_index(drop=True).copy()
                c = b["close"]; v = b["volume"]
                b["fwd"] = c.shift(-H) / c - 1
                b["r1"] = c.pct_change()
                b["r10"] = c / c.shift(10) - 1
                b["up20"] = np.log(c / c.rolling(20).min())
                b["up10"] = np.log(c / c.rolling(10).min())
                b["up40"] = np.log(c / c.rolling(40).min())
                sd = b["r1"].rolling(20).std()
                b["up20s"] = b["up20"] / (sd * np.sqrt(20))
                b["vr3"] = np.log(v.rolling(3).mean() / v.shift(3).rolling(20).mean())
                b["vr1"] = np.log(v / v.shift(1).rolling(20).mean())
                b["grid"] = (np.arange(len(b)) % H) == 0
                b["fc"] = b["regime"].isin(["trending", "unknown"])
                b["coin"] = coin; b["win"] = w; b["H"] = H
                b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
                b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
                frames.append(b)
            cb = pd.concat(frames)
            mu = cb.loc[cb["grid"] & cb["fwd"].notna(), "fwd"].mean()
            cb["ex"] = cb["fwd"] - mu
            allrows.append(cb)
    D = pd.concat(allrows)
    def clus_t(s, f):
        s = s[[f, "ex", "day"]].dropna()
        x = s[f] - s[f].mean()
        beta = (x * s["ex"]).sum() / (x ** 2).sum()
        e = s["ex"] - s["ex"].mean() - beta * x
        sc = (x * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (x ** 2).sum()
        return beta / se, len(s), s["day"].nunique()
    res = []
    for H in [3, 5, 10]:
        for inside in [True, False]:
            G = D[(D["H"] == H) & D["grid"] & (D["fc"] == inside) & D["ex"].notna()]
            for f in ["up10", "up20", "up40", "up20s", "r10"]:
                t, n, nd = clus_t(G, f)
                res.append({"H": H, "fallcalm": inside, "feat": f, "t_clus": round(t, 2), "n": n, "days": nd})
    out["up_by_horizon"] = pd.DataFrame(res)
    G = D[(D["H"] == 5) & D["grid"] & D["fc"] & D["ex"].notna()].dropna(subset=["up20"])
    out["up20_by_coin"] = G.groupby("coin").apply(lambda s: pd.Series({"n": len(s), "rho": stats.spearmanr(s["up20"], s["ex"])[0]})).round(3)
    out["up20_by_year"] = G.groupby("yr").apply(lambda s: pd.Series({"n": len(s), "rho": stats.spearmanr(s["up20"], s["ex"])[0]})).round(3)
    G["q"] = pd.qcut(G["up20"], 3, labels=False)
    out["up20_terc_size"] = G.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), up20=("up20", "mean"), fwd=("fwd", "mean")).round(4)
    # heavy-volume up days fade: all grid offsets pooled per coin-day not possible; use grid, H=5 and 3
    res = []
    for H in [3, 5, 10]:
        G2 = D[(D["H"] == H) & D["grid"] & D["fc"] & D["ex"].notna() & (D["r1"] > 0)]
        for f in ["vr1", "vr3"]:
            t, n, nd = clus_t(G2, f)
            res.append({"H": H, "feat": f, "t_clus": round(t, 2), "n": n})
        G3 = D[(D["H"] == H) & D["grid"] & ~D["fc"] & D["ex"].notna() & (D["r1"] > 0)]
        t, n, nd = clus_t(G3, "vr3")
        res.append({"H": H, "feat": "vr3 outside fc", "t_clus": round(t, 2), "n": n})
    out["upday_volume"] = pd.DataFrame(res)
    U = D[(D["H"] == 5) & D["grid"] & D["fc"] & D["ex"].notna() & (D["r1"] > 0)].dropna(subset=["vr3"])
    out["upday_vr3_by_coin"] = U.groupby("coin").apply(lambda s: pd.Series({"n": len(s), "rho": stats.spearmanr(s["vr3"], s["ex"])[0]})).round(3)
    return out

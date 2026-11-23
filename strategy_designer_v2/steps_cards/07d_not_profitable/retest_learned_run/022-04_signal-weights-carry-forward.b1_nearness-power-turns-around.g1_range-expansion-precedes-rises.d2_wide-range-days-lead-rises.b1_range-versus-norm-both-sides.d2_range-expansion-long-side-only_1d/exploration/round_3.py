import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    wins = sorted(list(bars[coins[0]].keys()), key=lambda s: int(s[1:]))
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            df = pd.DataFrame({
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                "f": b["forecast"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "fwd1": (cl.shift(-1)/cl - 1).values,
                "r30": (cl/cl.shift(30) - 1).values,
                "r60": (cl/cl.shift(60) - 1).values,
                "fwd": (cl.shift(-3)/cl - 1).values})
            df["coin"] = c; df["w"] = w; df["wi"] = wins.index(w); df["pos"] = np.arange(len(df))
            recs.append(df)
    G = pd.concat(recs, ignore_index=True)
    G["held"] = G["alloc"] > 0
    G["fpos"] = G["f"] > 0
    out["held bars by forecast>0"] = G[G["held"]].groupby("fpos").apply(
        lambda x: pd.Series({"n": len(x), "mean_alloc": x["alloc"].mean(),
                             "mean_gain": (x["alloc"]*x["fwd1"]).mean()}))
    cost = 0.0019/2

    def book(mask):
        a = G["alloc"].where(mask, 0.0).fillna(0.0)
        H = G[["coin","w","wi","day","fwd1"]].copy()
        H["a"] = a.values
        H["aprev"] = H.groupby(["coin","w"])["a"].shift(1).fillna(0.0)
        H["g"] = H["a"]*H["fwd1"].fillna(0.0) - (H["a"]-H["aprev"]).abs()*cost
        dd = H.groupby(["wi","day"])["g"].mean().sort_index()
        v = (1+dd).cumprod().values
        ddv = v/np.maximum.accumulate(v) - 1
        mdd = ddv.min()
        yr = v[-1]**(365/len(v)) - 1
        return pd.Series({"sharpe": dd.mean()/dd.std()*np.sqrt(365), "yearly": yr, "maxdd": mdd,
                          "calmar": yr/abs(mdd), "held_share": (H["a"] > 0).mean()})

    r30ok = G["r30"].fillna(0) >= 0
    r60ok = G["r60"].fillna(0) >= 0
    out["approx books"] = pd.DataFrame({
        "as tested": book(pd.Series(True, index=G.index)),
        "only r30>=0": book(r30ok),
        "only r60>=0": book(r60ok),
        "only f>0": book(G["fpos"]),
        "f>0 and r30>=0": book(G["fpos"] & r30ok),
    }).T

    g = G[G["pos"] % 3 == 0].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    res = {}
    for nm, cond in [("r60>=0", g["r60"] >= 0), ("r60<0", g["r60"] < 0)]:
        for s, sc in [("sig", g["f"] > 0), ("nosig", g["f"] <= 0)]:
            x = g[cond & sc]
            res[nm+"|"+s] = pd.Series({"n": len(x), "mean_ex": x["ex"].mean(),
                                       "t": stats.ttest_1samp(x["ex"], 0).statistic})
    out["r60 splits"] = pd.DataFrame(res).T

    s = g[(g["f"] > 0) & (g["r30"] >= 0)].copy()
    s["fq"] = pd.qcut(s["f"], 3, labels=False, duplicates="drop")
    out["r30>=0 sig by forecast tercile"] = s.groupby("fq")["ex"].agg(["count", "mean"])
    s2 = g[(g["f"] > 0) & (g["r30"] < 0)].copy()
    s2["fq"] = pd.qcut(s2["f"], 3, labels=False, duplicates="drop")
    out["r30<0 sig by forecast tercile"] = s2.groupby("fq")["ex"].agg(["count", "mean"])

    F = G[G["w"].isin(["w1","w2","w7","w14"]) & G["held"]].copy()
    F["r30neg"] = F["r30"] < 0
    out["bad windows held: r30<0, gain"] = F.groupby(["r30neg","fpos"]).apply(
        lambda x: pd.Series({"n": len(x), "mean_gain": (x["alloc"]*x["fwd1"]).mean(),
                             "sum_gain": (x["alloc"]*x["fwd1"]).sum()}))
    return out

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
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "f": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "prev": b["previous_allocation"],
                "fwd1": cl.shift(-1)/cl - 1,
                "r30": cl/cl.shift(30) - 1,
                "r60": cl/cl.shift(60) - 1,
                "fwd": cl.shift(-3)/cl - 1})
            df["coin"] = c; df["w"] = w; df["wi"] = wins.index(w); df["pos"] = np.arange(len(df))
            recs.append(df)
    G = pd.concat(recs)
    G["held"] = G["alloc"] > 0
    out["held bars by forecast>0"] = G[G["held"]].groupby(G["f"] > 0).apply(
        lambda x: pd.Series({"n": len(x), "mean_alloc": x["alloc"].mean(), "mean_gain": (x["alloc"]*x["fwd1"]).mean()}))
    G["chg"] = (G["alloc"] - G["prev"]).abs()
    cost = 0.0019/2

    def book(mask_fn):
        a = G["alloc"].where(mask_fn(G), 0.0).fillna(0)
        # turnover from changed positions
        H = G.assign(a=a)
        H["aprev"] = H.groupby(["coin","w"])["a"].shift(1).fillna(0)
        H["g"] = H["a"]*H["fwd1"].fillna(0) - (H["a"]-H["aprev"]).abs()*cost
        dd = H.groupby(["wi","day"])["g"].mean().sort_index()
        v = (1+dd).cumprod().values
        mdd = (v/np.maximum.accumulate(v) - 1).min()
        yr = v[-1]**(365/len(v)) - 1
        return pd.Series({"sharpe": dd.mean()/dd.std()*np.sqrt(365), "yearly": yr, "maxdd": mdd,
                          "calmar": yr/abs(mdd), "held_share": (H["a"] > 0).mean()})

    out["approx books"] = pd.DataFrame({
        "as tested": book(lambda H: pd.Series(True, index=H.index)),
        "only r30>=0": book(lambda H: H["r30"].fillna(0) >= 0),
        "only r60>=0": book(lambda H: H["r60"].fillna(0) >= 0),
        "only f>0": book(lambda H: H["f"] > 0),
        "f>0 and r30>=0": book(lambda H: (H["f"] > 0) & (H["r30"].fillna(0) >= 0)),
    }).T

    # condition alone on grid: r60 splits
    g = G[G["pos"] % 3 == 0].dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    g = g.assign(ex=g["fwd"] - g["coin"].map(drift))
    res = {}
    for nm, cond in [("r60>=0", g["r60"] >= 0), ("r60<0", g["r60"] < 0)]:
        for s, sc in [("sig", g["f"] > 0), ("nosig", g["f"] <= 0)]:
            x = g[cond & sc]
            res[nm+"|"+s] = pd.Series({"n": len(x), "mean_ex": x["ex"].mean(),
                                       "t": stats.ttest_1samp(x["ex"], 0).statistic})
    out["r60 splits"] = pd.DataFrame(res).T

    # weighted measure within r30>=0 by quartile of forecast
    s = g[(g["f"] > 0) & (g["r30"] >= 0)].copy()
    s["fq"] = pd.qcut(s["f"], 3, labels=False, duplicates="drop")
    out["r30>=0 sig by forecast tercile"] = s.groupby("fq")["ex"].agg(["count", "mean"])

    # in the w1-w2 fall, share of held bars with r30<0
    F = G[G["w"].isin(["w1","w2","w7","w14"]) & G["held"]]
    out["bad windows held: r30<0 share, gain"] = F.groupby(F["r30"] < 0).apply(
        lambda x: pd.Series({"n": len(x), "mean_gain": (x["alloc"]*x["fwd1"]).mean()}))
    return out

def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ret"] = b["close"]/b["close"].shift(1)-1
            b["nret"] = b["close"].shift(-1)/b["close"] - 1
            b["n3"] = b["close"].shift(-3)/b["close"] - 1
            b["vol20"] = b["ret"].rolling(20).std()
            b["move"] = b["ret"]/b["vol20"].shift(1)
            b["vrank"] = b["vol20"].rolling(365, min_periods=91).rank(pct=True)
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"]*b["nret"]
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["grid3"] = (np.arange(len(b)) % 3) == 0
            b["coin"] = coin; b["w"] = w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["nret"].transform("mean")
    B["ex"] = B["nret"] - cm
    B["vr3"] = pd.cut(B["vrank"], [0, 1/3, 2/3, 1.0001], labels=["lo","mid","hi"])
    B["mside"] = np.where(B["move"] < 0, "fall", "rise")
    def tt(x):
        x = x.dropna(); return x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
    g = B.groupby(["vr3","mside"])
    out["ex_by_vrank_side"] = g.agg(n=("ex","count"), ex=("ex","mean"), gross=("gross","mean"), fee=("fee","mean")).assign(t=g["ex"].apply(tt))
    # graded within falls: slope of ex on |move|*vrank
    for s in ["fall","rise"]:
        S = B[(B.mside==s)].dropna(subset=["ex","move","vrank"])
        x = S["move"].abs()*S["vrank"]
        sl, ic, r, p, se = __import__("scipy").stats.linregress(x, S["ex"])
        out[f"slope_{s}"] = pd.Series({"slope": sl, "t": sl/se, "n": len(S)})
    # 3-day after, grid
    G = B[B.grid3].dropna(subset=["n3","vrank"])
    G["ex3"] = G["n3"] - G.groupby("coin")["n3"].transform("mean")
    g3 = G.groupby(["vr3","mside"])
    out["ex3_by_vrank_side"] = g3.agg(n=("ex3","count"), ex3=("ex3","mean")).assign(t=g3["ex3"].apply(tt))
    # long-only and short-only contributions, with fees attributed by side
    B["side"] = np.sign(B["pos"])
    out["by_side_fee"] = B.groupby("side").agg(n=("gross","size"), gross=("gross","mean"), fee=("fee","mean"), net=("gross", lambda x: np.nan))
    out["by_side_fee"]["net"] = out["by_side_fee"]["gross"] - out["by_side_fee"]["fee"]
    # turnover concentration: fee by size of |move|
    B["amq"] = pd.qcut(B["move"].abs(), 4, labels=False, duplicates="drop")
    out["fee_by_absmove"] = B.groupby("amq").agg(absmove=("move", lambda x: x.abs().mean()), fee=("fee","mean"), gross=("gross","mean"), abspos=("pos", lambda x: x.abs().mean()))
    # autocorrelation of position (persistence)
    out["pos_autocorr"] = float(B.groupby(["coin","w"])["pos"].apply(lambda s: s.autocorr()).mean())
    return out

def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["ret1"]
            b["r10p"] = b["close"]/b["close"].shift(10)-1
            b["r30p"] = b["close"]/b["close"].shift(30)-1
            b["f10"] = b["close"].shift(-10)/b["close"]-1
            b["coin"]=coin; b["w"]=w
            rows.append(b[["coin","w","pos","ret1","gain","forecast","r10p","r30p"]])
            g = b.iloc[::10][["forecast","f10","r30p","r10p"]].copy(); g["coin"]=coin
            grid.append(g)
    B = pd.concat(rows, ignore_index=True).dropna(subset=["ret1"])
    G = pd.concat(grid, ignore_index=True).dropna(subset=["f10","forecast"])
    G["ex"] = G["f10"] - G.groupby("coin")["f10"].transform("mean")
    G["fq"] = pd.qcut(G["forecast"].rank(method="first"),5,labels=False)
    out["grid_fq"] = G.groupby("fq").agg(n=("ex","size"), fc=("forecast","mean"), ex=("ex","mean"),
                                         t=("ex", lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    G2 = G.dropna(subset=["r30p"]).copy()
    G2["trend"] = np.where(G2["r30p"]>0,"up30","down30")
    out["grid_trend_fq"] = G2.groupby(["trend","fq"]).agg(n=("ex","size"), ex=("ex","mean")).reset_index()
    B2 = B.dropna(subset=["r30p"]).copy()
    B2["trend"] = np.where(B2["r30p"]>0,"up30","down30")
    B2["side"] = np.where(B2["pos"]>0,"long",np.where(B2["pos"]<0,"short","flat"))
    out["day_trend_side"] = B2.groupby(["trend","side"]).agg(n=("gain","size"), gain=("gain","mean"),
                                                            ret=("ret1","mean"), pos=("pos","mean")).reset_index()
    # book drawdowns per coin-window chain
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            r = d["book_return"].fillna(0)
            v = (1+r).cumprod(); m = (v/v.cummax()-1).min()
            dd.append((coin, w, m, d["coin_return"].mean()))
    DD = pd.DataFrame(dd, columns=["coin","w","maxdd","coinret"])
    out["worst_dd"] = DD.sort_values("maxdd").head(12)
    out["dd_vs_coinret_corr"] = float(DD["maxdd"].corr(DD["coinret"]))
    return out

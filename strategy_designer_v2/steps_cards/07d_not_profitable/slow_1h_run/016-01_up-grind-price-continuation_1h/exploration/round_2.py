def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    B = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b[["timestamp","close","forecast","postRebalance_current_allocation","previous_allocation",
                   "total_portfolio_value","postRebalance_total_value",
                   "debug_info.components.grind_share.last_history_value"]].copy()
            b.columns = ["ts","close","fc","pos","prev","tv","ptv","raw"]
            b["r1"] = b.close.shift(-1)/b.close - 1
            b["gross"] = b.pos*b.r1
            b["fee"] = (b.tv - b.ptv)/b.tv
            b["turn"] = (b.pos - b.prev).abs()
            b["f72"] = b.close.shift(-72)/b.close - 1
            b["p72"] = b.close/b.close.shift(72) - 1
            act = (b.fc > 0).astype(int)
            grp = (act != act.shift()).cumsum()
            b["age"] = act.groupby(grp).cumcount()
            b["coin"] = c; b["w"] = w
            b["hour"] = pd.to_datetime(b.ts).dt.hour
            B.append(b)
    B = pd.concat(B)
    ndays = B.groupby(["coin","w",pd.to_datetime(B.ts).dt.floor("D")]).ngroups
    out["per day: gross, fee, turnover"] = pd.Series({"gross/day": B.gross.sum()/ndays, "fee/day": B.fee.sum()/ndays,
                                                      "turnover/day": B.turn.sum()/ndays, "share hours active": (B.fc>0).mean()})
    A = B[B.fc > 0].copy()
    out["active hourly gain by fc decile"] = A.groupby(pd.qcut(A.fc.rank(method="first"), 5, labels=False)).agg(
        gain=("gross","mean"), r1=("r1","mean"), fc=("fc","mean"), raw=("raw","mean"), pos=("pos","mean"), n=("r1","size"))
    A["ageb"] = pd.cut(A.age, [-1,0,5,23,71,10000])
    out["active hourly r1 by hours since activation"] = A.groupby("ageb").agg(r1=("r1","mean"), gain=("gross","mean"), n=("r1","size"))
    A["rawq"] = pd.qcut(A.raw.rank(method="first"), 5, labels=False)
    out["active r1 by raw fifth"] = A.groupby("rawq").agg(r1=("r1","mean"), raw=("raw","mean"), fc=("fc","mean"))
    out["inactive r1 mean"] = B.loc[B.fc<=0,"r1"].mean()
    out["all r1 mean"] = B.r1.mean()
    # grid over active: pos past-return thirds among fc>0
    G = []
    for (c,w), b in B.groupby(["coin","w"], sort=False):
        g = b.iloc[::72]
        G.append(g)
    G = pd.concat(G).dropna(subset=["f72","p72"])
    Ga = G[G.fc>0].copy()
    Ga["pq"] = pd.qcut(Ga.p72.rank(method="first"),3,labels=False)
    Ga["rq"] = pd.qcut(Ga.raw.rank(method="first"),3,labels=False)
    out["grid fc>0: f72 by past third x raw third"] = Ga.pivot_table(index="pq",columns="rq",values="f72",aggfunc="mean")
    out["grid fc>0 n, f72 mean"] = pd.Series({"n":len(Ga),"f72":Ga.f72.mean(),"raw0 share":(Ga.raw<=0).mean()})
    out["grid fc==0 & raw>0 f72"] = G[(G.fc<=0)&(G.raw>0)].f72.agg(["mean","count"])
    out["grid raw>0 f72 by raw third"] = G[G.raw>0].groupby(pd.qcut(G[G.raw>0].raw.rank(method="first"),3,labels=False)).f72.agg(["mean","count"])
    return out

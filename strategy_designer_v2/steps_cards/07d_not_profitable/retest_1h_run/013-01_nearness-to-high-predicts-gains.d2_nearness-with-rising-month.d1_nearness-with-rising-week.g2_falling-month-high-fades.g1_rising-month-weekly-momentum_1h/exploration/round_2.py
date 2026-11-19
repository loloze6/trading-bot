def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"]
            r1 = cl.shift(-1)/cl-1
            pos = b["postRebalance_current_allocation"].fillna(0)
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).clip(lower=0)/b["total_portfolio_value"]
            df = pd.DataFrame({"coin":c,"win":int(w[1:]),"i":np.arange(len(b)),"pos":pos,"gain":pos*r1,"fee":fee,
                "w7":cl/cl.shift(168)-1,"m30":cl/cl.shift(720)-1,"fc":b["forecast"],
                "raw":b["debug_info.components.week.last_history_value"],
                "chg":(pos-b["previous_allocation"].fillna(0)).abs(),
                "f168":cl.shift(-168)/cl-1,"m90":cl/cl.shift(2160)-1,
                "w7p":(cl.shift(168)/cl.shift(336)-1)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["net"]=A["gain"]-A["fee"]
    A["fcb"]=pd.cut(A["fc"],[-0.1,0,2,5,10,20.1],labels=["0","0-2","2-5","5-10","10-20"])
    out["by_fc_level"]=A.groupby("fcb").agg(n=("gain","size"),gain=("gain","mean"),fee=("fee","mean"),net=("net","mean"),pos=("pos","mean"),turn=("chg","mean"))
    # raw week sign while long
    L=A[A.pos>0]
    out["long_rawweek_neg_share"]=(L["raw"]<0).mean()
    out["long_by_rawsign"]=L.groupby(L["raw"]>0).agg(n=("gain","size"),gain=("gain","mean"),fee=("fee","mean"),pos=("pos","mean"))
    # drawdown windows 5-10 vs others
    A["ddwin"]=A["win"].between(5,10)
    out["dd_vs_other"]=A.groupby("ddwin").agg(gain=("gain","mean"),fee=("fee","mean"),long=("pos",lambda x:(x>0).mean()),pos=("pos","mean"),m30=("m30","mean"),m90=("m90","mean"))
    # 168 grid, long-start: fwd by m90 sign and by previous week
    G=A[(A.i%168)==0].dropna(subset=["f168","w7","m30"])
    T=G[G.m30>0].copy()
    def tt(x): return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["trend_grid_f168_by_m90sign"]=T.dropna(subset=["m90"]).groupby(T["m90"]>0)["f168"].apply(tt).unstack()
    T["w7q"]=pd.qcut(T["w7"].rank(method="first"),4,labels=False)
    out["trend_grid_by_w7q_m90"]=T.dropna(subset=["m90"]).groupby(["w7q",T["m90"]>0])["f168"].apply(tt).unstack()
    out["trend_grid_by_w7q_m30q"]=T.groupby(["w7q",pd.qcut(T["m30"],2,labels=["m30lo","m30hi"])])["f168"].apply(tt).unstack()
    # turnover share of fees from small changes
    out["fee_share_when_fc_small"]=A.loc[A.fc.between(1e-9,2),"fee"].sum()/A["fee"].sum()
    out["fee_share_fc0"]=A.loc[A.fc==0,"fee"].sum()/A["fee"].sum()
    return out

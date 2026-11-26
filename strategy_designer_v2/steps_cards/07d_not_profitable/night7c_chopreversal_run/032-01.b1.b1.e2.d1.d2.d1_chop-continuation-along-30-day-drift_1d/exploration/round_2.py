def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c]}, key=lambda s:int(s[1:]))
    recs=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change()
            ret7=cl/cl.shift(7)-1; ret30=cl/cl.shift(30)-1
            er=(cl-cl.shift(30)).abs()/cl.diff().abs().rolling(30).sum()
            vol=r1.rolling(30).std()
            fwd1=cl.shift(-1)/cl-1; fwd7=cl.shift(-7)/cl-1
            pos=b.postRebalance_current_allocation
            d=pd.DataFrame({"coin":c,"win":w,"pos":pos,"pnl":pos*fwd1,"fc":b.forecast,"reg":b.regime,
                "ret7":ret7,"ret30":ret30,"er":er,"scaled":ret7/(vol*np.sqrt(7)),
                "r30s":ret30/(vol*np.sqrt(30)),"fwd7":fwd7,"fwd1":fwd1,"idx":np.arange(len(b))})
            recs.append(d)
    D=pd.concat(recs,ignore_index=True)
    D["side"]=np.sign(D.pos)
    D["fall"]=D.win.isin(["w12","w13","w14"])
    H=D[D.side!=0].copy()
    H["inchop"]=H.reg=="chop"
    out["held pnl: in chop vs held after chop"]=H.groupby(["inchop","side"]).pnl.agg(["count","mean","sum","std"])
    out["fall windows w12-14 by side"]=H.groupby(["fall","side"]).pnl.agg(["count","mean","sum"])
    out["fall windows by chop"]=H.groupby(["fall","inchop"]).pnl.agg(["count","mean","sum"])
    # side vs sign of ret30 against longer trend: scaled 30d return magnitude, side x r30s tercile
    H["r30q"]=pd.qcut(H.r30s.abs(),3,labels=False)
    out["held pnl side x |r30s| tercile"]=H.groupby(["side","r30q"]).pnl.agg(["count","mean","sum","std"])
    # mean daily pnl per |fc| quartile restricted to chop bars only
    C=H[H.inchop].copy()
    C["fq"]=pd.qcut(C.fc.abs().rank(method="first"),3,labels=False)
    out["chop bars pnl by |fc| tercile"]=C.groupby("fq").pnl.agg(["count","mean","sum","std"])
    # grid: condition check -- |r30s| alone vs with signal
    G=D[D.idx%7==0].dropna(subset=["fwd7","ret7","ret30","er","r30s"]).copy()
    drift=G.groupby("coin").fwd7.mean(); G["un"]=G.fwd7-G.coin.map(drift)
    G["sig"]=(G.er<0.3)&(np.sign(G.ret7)==np.sign(G.ret30))
    G["s7"]=np.sign(G.ret7)*G.un; G["s30"]=np.sign(G.ret30)*G.un
    G["r30q"]=pd.qcut(G.r30s.abs(),3,labels=False)
    out["grid s7 by sig x |r30s| tercile"]=G.groupby(["sig","r30q"]).s7.agg(["count","mean","std"])
    out["grid s30 (30d sign alone) by |r30s| tercile, no sig"]=G[~G.sig].groupby("r30q").s30.agg(["count","mean","std"])
    G["sq"]=pd.qcut(G.scaled.abs(),3,labels=False)
    out["grid s7 sig by |scaled7| tercile"]=G[G.sig].groupby("sq").s7.agg(["count","mean","std"])
    # cumulative chop days per day holding, daily book dd during fall: days in position & mean abs pos
    out["mean |pos| fall vs not"]=D.groupby("fall").pos.apply(lambda x:x.abs().mean())
    out["share bars chop"]=D.groupby("fall").reg.apply(lambda x:(x=="chop").mean())
    return out

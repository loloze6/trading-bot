def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r1=c.pct_change(); rng=(h-l).replace(0,np.nan); loc=(c-l)/rng
            vol20=r1.rolling(20).std()
            r5s=(c/c.shift(5)-1)/(vol20*np.sqrt(5))
            r20s=(c/c.shift(20)-1)/(vol20*np.sqrt(20))
            r60=c/c.shift(60)-1
            v30=r1.rolling(30).std(); vpct=v30.rolling(365,min_periods=120).rank(pct=True)
            d=pd.DataFrame({"coin":coin,"pos":np.arange(len(b)),"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                            "loc":loc,"r5s":r5s,"r20s":r20s,"r60":r60,"vpct":vpct,
                            "fwd3":c.shift(-3)/c-1,"fwd5":c.shift(-5)/c-1})
            rows.append(d)
    D=pd.concat(rows)
    def ct(x,col):
        x=x.dropna(subset=[col]); n=len(x)
        if n<10: return pd.Series({"n":n,"days":np.nan,"mean":np.nan,"t":np.nan})
        m=x[col].mean(); dev=x.groupby("day")[col].apply(lambda v:(v-m).sum()); D_=len(dev)
        se=np.sqrt((dev**2).sum()*D_/(D_-1))/n
        return pd.Series({"n":n,"days":D_,"mean":m,"t":m/se})
    out={}
    for h in [3,5]:
        G=D[D.pos%h==0].dropna(subset=["fwd%d"%h,"r5s"]).copy()
        G["ex"]=G["fwd%d"%h]-G.coin.map(G.groupby("coin")["fwd%d"%h].mean())
        G["trend"]=np.where(G.r60>0.10,"rising",np.where(G.r60<-0.10,"falling",np.where(G.r60.notna(),"choppy","na")))
        G["agi"]=np.where(G.vpct>0.5,"agi",np.where(G.vpct.notna(),"calm","na"))
        G["r20q"]=pd.qcut(G.r20s,5,labels=False)
        out["h%d_r20q"%h]=G.groupby("r20q").apply(lambda x:ct(x,"ex"))
        S=G[G.r5s<=-1].copy(); S["sh"]=-S["ex"]  # short-direction
        S["locb"]=pd.cut(S["loc"],[-0.01,0.5,0.75,1.01])
        out["h%d_fall_locb"%h]=S.groupby("locb").apply(lambda x:ct(x,"ex"))
        out["h%d_fall_locb_prof"%h]=S.groupby(["trend","agi",S["loc"]>=0.75]).apply(lambda x:ct(x,"ex"))
        R=G[G.r5s>=1].copy()
        out["h%d_rise_prof_loc"%h]=R.groupby(["trend","agi",R["loc"]>=0.75]).apply(lambda x:ct(x,"ex"))
    return out

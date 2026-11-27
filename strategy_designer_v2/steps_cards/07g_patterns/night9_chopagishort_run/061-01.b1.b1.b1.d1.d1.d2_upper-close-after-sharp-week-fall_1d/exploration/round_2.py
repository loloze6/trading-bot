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
            r60=c/c.shift(60)-1
            v30=r1.rolling(30).std(); vrel=v30/r1.expanding(30).std()
            fwd3=c.shift(-3)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                            "loc":loc,"r5s":r5s,"r60":r60,"vrel":vrel,"fwd3":fwd3,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows)
    G=D[D.pos%3==0].dropna(subset=["fwd3","r5s"]).copy()
    drift=G.groupby("coin")["fwd3"].mean(); sd=G.groupby("coin")["fwd3"].std()
    G["ex"]=G["fwd3"]-G["coin"].map(drift); G["exs"]=G["ex"]/G["coin"].map(sd)
    G["r5q"]=pd.qcut(G["r5s"],5,labels=False)
    G["locq"]=pd.qcut(G["loc"],5,labels=False)
    def ct(x,col="ex"):
        s=x.groupby("day")[col].sum(); n=len(x); D_=len(s)
        if D_<3: return pd.Series({"n":n,"days":D_,"mean":np.nan,"t":np.nan})
        m=x[col].mean(); dev=x.groupby("day")[col].apply(lambda v:(v-m).sum())
        se=np.sqrt((dev**2).sum()*D_/(D_-1))/n
        return pd.Series({"n":n,"days":D_,"mean":m,"t":m/se})
    out={}
    out["r5q_dayclustered"]=G.groupby("r5q").apply(ct)
    G["trend"]=np.where(G.r60>0.10,"rising",np.where(G.r60< -0.10,"falling",np.where(G.r60.notna(),"choppy","na")))
    G["agi"]=np.where(G.vrel>1,"agi",np.where(G.vrel.notna(),"calm","na"))
    G["r5sign"]=np.sign(G.r5s)
    G["mom"]=G["ex"]*np.sign(G["r5s"])  # move in direction of 5d return
    G["big"]=G.r5s.abs()>1
    out["mom_by_trend_big"]=G.groupby(["trend","big"]).apply(lambda x:ct(x,"mom"))
    out["mom_by_agi_big"]=G.groupby(["agi","big"]).apply(lambda x:ct(x,"mom"))
    out["mom_by_year_big"]=G[G.big].groupby("yr").apply(lambda x:ct(x,"mom"))
    out["mom_by_sign_big"]=G[G.big].groupby("r5sign").apply(lambda x:ct(x,"mom"))
    # graded: r5s abs buckets
    G["absq"]=pd.cut(G.r5s.abs(),[0,0.5,1,1.5,2,10])
    out["mom_by_abs"]=G.groupby("absq").apply(lambda x:ct(x,"mom"))
    # tested idea situation, all profiles
    S=G[(G.r5s<=-1)]
    S["locq2"]=pd.cut(S["loc"],[-0.01,0.25,0.5,0.75,1.01])
    out["fall_by_loc"]=S.groupby("locq2").apply(ct)
    out["fall_by_loc_trend"]=S.groupby(["trend",S["loc"]>=0.5]).apply(ct)
    R=G[(G.r5s>=1)]
    out["rise_by_loc"]=R.groupby(pd.cut(R["loc"],[-0.01,0.25,0.5,0.75,1.01])).apply(ct)
    out["rise_by_trend"]=R.groupby("trend").apply(ct)
    out["mom_by_coin_big"]=G[G.big].groupby("coin").apply(lambda x:ct(x,"mom"))
    return out

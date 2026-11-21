def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs=[];hrs=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            ts=pd.to_datetime(df["timestamp"])
            r24=c/c.shift(24)-1
            mad=r24.abs().rolling(720,min_periods=360).mean()
            r7=c/c.shift(168)-1
            r7z=r7/(mad*np.sqrt(7))
            r30=c/c.shift(720)-1
            n=np.arange(len(df))
            d=pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year,"wd":ts.dt.weekday,"r7":r7,"r7z":r7z,"r30":r30,
                            "f96":c.shift(-96)/c-1,"f240":c.shift(-240)/c-1,"g96":n%96==0,"g240":n%240==0})
            recs.append(d)
            hrs.append(pd.DataFrame({"coin":coin,"year":ts.dt.year,"hour":ts.dt.hour,"r":c.shift(-1)/c-1}))
    A=pd.concat(recs)
    out={}
    def tt(v):
        v=v.dropna();n=len(v)
        return pd.Series({"n":n,"mean":v.mean(),"t":v.mean()/(v.std()/np.sqrt(n)) if n>2 else np.nan})
    res={}
    for h,g in [("f96","g96"),("f240","g240")]:
        G=A[A[g]].dropna(subset=[h,"r7z"]).copy()
        G["u"]=G[h]-G.groupby("coin")[h].transform("mean")
        usual=G.groupby("coin")[h].transform("std")
        G["s"]=G["u"]/usual
        G["q"]=G.groupby("coin")["r7z"].transform(lambda x:pd.qcut(x,5,labels=False))
        res[h]=G
        out[f"{h} u by r7z quintile"]=G.groupby("q")["u"].apply(tt).unstack()
        out[f"{h} strength by r7z quintile"]=G.groupby("q")["s"].apply(tt).unstack()
        sp={}
        for coin,x in G.groupby("coin"):
            rho,p=stats.spearmanr(x.r7z,x.u);sp[coin]=[len(x),rho,p,x.loc[x.q==4,"u"].mean()-x.loc[x.q==0,"u"].mean()]
        for y,x in G.groupby("year"):
            rho,p=stats.spearmanr(x.r7z,x.u);sp[f"y{y}"]=[len(x),rho,p,x.loc[x.q==4,"u"].mean()-x.loc[x.q==0,"u"].mean()]
        out[f"{h} spearman r7z vs u by coin/year"]=pd.DataFrame(sp,index=["n","rho","p","top-bottom"]).T
    G=res["f96"]
    G["up30"]=G.r30>0
    out["f96 u by r7z quintile x up30"]=G.groupby(["up30","q"])["u"].apply(tt).unstack()
    sat=G[G.wd==5]
    out["saturday u96 by coin"]=sat.groupby("coin")["u"].apply(tt).unstack()
    out["saturday u96 by year"]=sat.groupby("year")["u"].apply(tt).unstack()
    Hh=pd.concat(hrs).dropna(subset=["r"])
    e=Hh[Hh.hour.isin([20,21])]
    out["hours 20-21 by year"]=e.groupby("year")["r"].apply(tt).unstack()
    out["hours 20-21 by coin"]=e.groupby("coin")["r"].apply(tt).unstack()
    T=[]
    for coin,ws in data["trades"].items():
        for w,df in ws.items():
            if len(df): T.append(df.assign(coin=coin))
    T=pd.concat(T)
    rho,p=stats.spearmanr(T.entry_forecast,T.net_profit_loss_percent)
    T["dq"]=pd.qcut(T.duration_minutes.rank(method="first"),4,labels=False)
    out["trade spearman fc vs net"]=pd.Series({"rho":rho,"p":p,"n":len(T)})
    out["trades by duration quartile"]=T.groupby("dq").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),median=("net_profit_loss_percent","median"),hours=("duration_minutes",lambda v:v.median()/60))
    return out

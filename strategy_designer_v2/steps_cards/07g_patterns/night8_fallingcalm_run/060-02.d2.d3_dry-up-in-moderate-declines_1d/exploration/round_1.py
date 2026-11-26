import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            fwd=c.shift(-5)/c-1
            r60=c/c.shift(60)-1; r10=c/c.shift(10)-1; r1=c/c.shift(1)-1
            m30=v.rolling(30).mean(); shr=-np.log(m30/m30.shift(30))
            sd30=r1.rolling(30).std()
            sdw=r1.std()
            rng=(b["high"]-b["low"])/c
            loc=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            yr=pd.to_datetime(b["timestamp"]).dt.year
            idx=np.arange(0,len(b),5)
            d=pd.DataFrame({"coin":coin,"w":w,"fwd":fwd.iloc[idx].values,"r60":r60.iloc[idx].values,
              "r10":r10.iloc[idx].values,"shr":shr.iloc[idx].values,"fc":b["forecast"].iloc[idx].values,
              "r1":r1.iloc[idx].values,"agit":(sd30/sdw).iloc[idx].values,"rng":rng.iloc[idx].values,
              "loc":loc.iloc[idx].values,"wd":wd.iloc[idx].values,"yr":yr.iloc[idx].values,
              "reg":b["regime"].iloc[idx].values,"ts":b["timestamp"].iloc[idx].values})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["drift"]=D.groupby("coin")["fwd"].transform("mean")
    D["ex"]=D["fwd"]-D["drift"]
    D["prof"]=np.where(D.r60>0.1,"rising",np.where(D.r60<-0.1,"falling","choppy"))
    D.loc[D.r60.isna(),"prof"]="na"
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["by_profile"]=D.groupby("prof").apply(summ)
    D["shrq"]=D.groupby("prof")["shr"].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["prof_x_shrink_q"]=D.groupby(["prof","shrq"]).apply(summ)
    F=D[D.prof=="falling"].copy()
    F["r10q"]=pd.qcut(F.r10,4,labels=False)
    out["falling_r10q"]=F.groupby("r10q").apply(summ)
    F["agq"]=pd.qcut(F.agit,3,labels=False)
    out["falling_agit_x_shrq"]=F.groupby(["agq","shrq"]).apply(summ)
    out["falling_active_vs_not"]=F.groupby(F.fc<0).apply(summ)
    out["by_yr_falling_short_signal"]=F[F.fc<0].groupby("yr").apply(summ)
    D["r1q"]=D.groupby("prof")["r1"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["prof_x_r1q"]=D.groupby(["prof","r1q"]).apply(summ)
    D["locq"]=pd.qcut(D["loc"],3,labels=False)
    out["prof_x_locq"]=D.groupby(["prof","locq"]).apply(summ)
    # correlations shr vs ex within profiles
    cr={}
    for p,g in D.dropna(subset=["shr","ex"]).groupby("prof"):
        r,pv=stats.spearmanr(g.shr,g.ex); cr[p]=(len(g),round(r,3),round(pv,4))
    out["spearman_shr_ex"]=pd.DataFrame(cr,index=["n","rho","p"]).T
    return out

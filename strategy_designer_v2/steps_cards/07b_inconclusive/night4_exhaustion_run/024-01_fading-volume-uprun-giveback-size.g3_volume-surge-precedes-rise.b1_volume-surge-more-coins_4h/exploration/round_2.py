import numpy as np, pandas as pd

def explore(data):
    H=18
    bars=data["bars"]
    drift={}; usual={}
    for c in bars:
        rs=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-H,H)
            rs+=list(cl[idx+H]/cl[idx]-1)
        drift[c]=np.mean(rs); usual[c]=np.std(rs)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            f=df["forecast"].fillna(0).values
            cl=df["close"].values; vol=df["volume"].values
            n=len(df)
            prev=np.r_[0,f[:-1]]
            sig=(f-prev)>=2
            seen=set()
            vm=pd.Series(vol).shift(1).rolling(180,min_periods=45).mean().values
            r6=pd.Series(cl).pct_change(6).values
            r180=pd.Series(cl).pct_change(180).values
            s6=pd.Series(cl).pct_change().rolling(180,min_periods=45).std().values*np.sqrt(6)
            for t in np.where(sig)[0]:
                cell=t//H
                if cell in seen or t+H>=n: continue
                seen.add(cell)
                rows.append({"coin":c,"f":f[t],"vr":vol[t]/vm[t] if vm[t]>0 else np.nan,
                    "r6":r6[t],"z6":r6[t]/s6[t] if s6[t]>0 else np.nan,"r180":r180[t],
                    "x18":cl[t+H]/cl[t]-1-drift[c],"s18":(cl[t+H]/cl[t]-1-drift[c])/usual[c]})
    D=pd.DataFrame(rows)
    def agg(g):
        x=g["x18"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"strength":g["s18"].mean()})
    out={}
    D["trend30"]=np.where(D["r180"]>0,"up30","down30")
    out["by_trend30"]=D.dropna(subset=["r180"]).groupby("trend30").apply(agg)
    D["r180q"]=pd.qcut(D["r180"],5,labels=False)
    out["by_r30_q"]=D.groupby("r180q").apply(lambda g: pd.concat([agg(g),pd.Series({"med":g["r180"].median()})]))
    D["vrq"]=pd.qcut(D["vr"],5,labels=False)
    D["z6q"]=pd.qcut(D["z6"],5,labels=False)
    out["by_z6_q"]=D.groupby("z6q").apply(lambda g: pd.concat([agg(g),pd.Series({"med":g["z6"].median()})]))
    out["vrq_x_trend30"]=D.dropna(subset=["r180"]).groupby(["trend30","vrq"]).apply(agg)
    D["z6side"]=np.where(D["z6"]<-1,"fall",np.where(D["z6"]>1,"rise","flat"))
    out["z6side_x_vrq"]=D.groupby(["z6side","vrq"]).apply(agg)
    out["corr_vr_x18_by_trend"]=D.dropna(subset=["r180"]).groupby("trend30").apply(lambda g: pd.Series({"spearman":g[["vr","x18"]].corr("spearman").iloc[0,1],"n":len(g)}))
    return out

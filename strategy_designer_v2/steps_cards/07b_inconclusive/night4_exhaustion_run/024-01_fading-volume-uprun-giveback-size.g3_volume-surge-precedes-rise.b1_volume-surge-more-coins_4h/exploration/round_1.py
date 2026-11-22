import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=18
    bars=data["bars"]
    # coin mean 18-bar return over all windows, non-overlapping grid
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
            r1=pd.Series(cl).pct_change().values
            r6=pd.Series(cl).pct_change(6).values
            for t in np.where(sig)[0]:
                cell=t//H
                if cell in seen: continue
                seen.add(cell)
                d={"coin":c,"w":w,"year":pd.Timestamp(df["timestamp"].iloc[t]).year,"f":f[t],
                   "vr":vol[t]/vm[t] if vm[t]>0 else np.nan,"r1":r1[t],"r6":r6[t]}
                for h in (1,3,6,12,18,36):
                    d[f"x{h}"]=(cl[t+h]/cl[t]-1-drift[c]*h/H) if t+h<n else np.nan
                d["s18"]=d["x18"]/usual[c] if not np.isnan(d["x18"]) else np.nan
                rows.append(d)
    D=pd.DataFrame(rows)
    def agg(g,col="x18"):
        x=g[col].dropna(); fw=g.loc[x.index,"f"]
        y=fw*x/fw.mean()
        return pd.Series({"n":len(x),"mean":x.mean(),"wmean":y.mean(),"t_w":y.mean()/(y.std()/np.sqrt(len(y))) if len(y)>2 else np.nan})
    out={}
    out["forecast_dist"]=D["f"].describe()
    out["share_f_at_cap"]=float((D["f"]>=19.99).mean())
    out["horizons"]=pd.DataFrame({h:agg(D,f"x{h}") for h in (1,3,6,12,18,36)}).T
    out["by_coin"]=D.groupby("coin").apply(agg)
    out["by_year"]=D.groupby("year").apply(agg)
    D["vrq"]=pd.qcut(D["vr"],5,labels=False,duplicates="drop")
    out["by_volratio_q"]=D.groupby("vrq").apply(lambda g: pd.concat([agg(g),pd.Series({"vr_med":g["vr"].median()})]))
    D["bar_dir"]=np.where(D["r1"]>0,"up_bar","down_bar")
    out["by_signal_bar_dir"]=D.groupby("bar_dir").apply(agg)
    D["r6q"]=pd.qcut(D["r6"],5,labels=False)
    out["by_prior24h_ret_q"]=D.groupby("r6q").apply(lambda g: pd.concat([agg(g),pd.Series({"r6_med":g["r6"].median()})]))
    out["strength_mean"]=float(D["s18"].mean())
    return out

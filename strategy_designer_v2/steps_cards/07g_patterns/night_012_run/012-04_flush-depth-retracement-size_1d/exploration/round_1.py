def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); o=b["open"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std().shift(1)
            z=r/sd
            vr=v/v.shift(1).rolling(20).median()
            rng=(h-l).replace(0,np.nan)
            lw=(np.minimum(o,c)-l)/rng
            uw=(h-np.maximum(o,c))/rng
            r5=c/c.shift(5)-1
            volreg=sd/ r.rolling(120,min_periods=40).std().shift(1)
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for H in (1,3,7):
                fwd=c.shift(-H)/c-1
                idx=np.arange(0,n,H)
                d=pd.DataFrame({"coin":coin,"w":w,"H":H,"fwd":fwd.iloc[idx].values,"z":z.iloc[idx].values,
                  "vr":vr.iloc[idx].values,"lw":lw.iloc[idx].values,"uw":uw.iloc[idx].values,"r5":r5.iloc[idx].values,
                  "volreg":volreg.iloc[idx].values,"wd":ts.iloc[idx].dt.weekday.values,
                  "reg":b["regime"].iloc[idx].values,"fc":b["forecast"].iloc[idx].values})
                rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd"])
    out={}
    # excess vs coin mean
    D["ex"]=D["fwd"]-D.groupby(["coin","H"])["fwd"].transform("mean")
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    D["zb"]=pd.cut(D["z"],[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["z_bucket"]=D.groupby(["H","zb"]).apply(summ).unstack(0)
    D["vrb"]=pd.qcut(D["vr"],5,labels=False,duplicates="drop")
    out["volratio_q"]=D.groupby(["H","vrb"]).apply(summ).unstack(0)
    D["r5b"]=pd.qcut(D["r5"],5,labels=False)
    out["r5_q"]=D.groupby(["H","r5b"]).apply(summ).unstack(0)
    D["vlb"]=pd.qcut(D["volreg"],5,labels=False)
    out["volregime_q"]=D.groupby(["H","vlb"]).apply(summ).unstack(0)
    D["lwb"]=pd.qcut(D["lw"],5,labels=False,duplicates="drop")
    out["lowwick_q"]=D.groupby(["H","lwb"]).apply(summ).unstack(0)
    D["uwb"]=pd.qcut(D["uw"],5,labels=False,duplicates="drop")
    out["upwick_q"]=D.groupby(["H","uwb"]).apply(summ).unstack(0)
    out["weekday_H1"]=D[D.H==1].groupby("wd").apply(summ)
    # sharp falls: flush vs non flush
    sf=D[(D.z<=-2)]
    sf=sf.assign(flush=(sf.vr>=2)&(sf.lw>=0.3))
    out["sharpfall_flush"]=sf.groupby(["H","flush"]).apply(summ).unstack(0)
    # by coin, H=3, z<=-1.5
    out["coin_drop_H3"]=D[(D.H==3)&(D.z<=-1.5)].groupby("coin").apply(summ)
    out["coin_rise_H3"]=D[(D.H==3)&(D.z>=1.5)].groupby("coin").apply(summ)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for H in [1,3,5,10]:
            rr=[]
            for w, b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-H,H)
                rr+=list(c[idx+H]/c[idx]-1)
            drift[(coin,H)]=(np.mean(rr),np.std(rr))
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()
            r1=c/c.shift(1)-1
            fc=b["regime"]!="chop"
            r5p=c/c.shift(5)-1
            for H in [1,3,5,10]:
                f=c.shift(-H)/c-1
                for i in range(0,len(b)-H,H):
                    if not fc.iloc[i] or pd.isna(vr.iloc[i]) or pd.isna(r1.iloc[i]): continue
                    rows.append(dict(coin=coin,w=w,H=H,i=i,day=str(b["timestamp"].iloc[i])[:10],
                        vr=vr.iloc[i],r1=r1.iloc[i],r5p=r5p.iloc[i],
                        unusual=f.iloc[i]-drift[(coin,H)][0],year=str(b["timestamp"].iloc[i])[:4]))
    d=pd.DataFrame(rows)
    def grp(g):
        x=g["unusual"]
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    d["kind"]=np.where(d.r1>0,np.where(d.vr>1,"up_heavy","up_light"),np.where(d.vr>1,"down_heavy","down_light"))
    out={}
    out["kind_by_H"]=d.groupby(["H","kind"]).apply(grp)
    up=d[d.r1>0].copy()
    up["vq"]=up.groupby("H")["vr"].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["up_vol_quartile_by_H"]=up.groupby(["H","vq"]).apply(grp)
    dn=d[d.r1<=0].copy()
    dn["vq"]=dn.groupby("H")["vr"].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["down_vol_quartile_by_H"]=dn.groupby(["H","vq"]).apply(grp)
    h5=d[(d.H==5)&(d.kind=="up_heavy")]
    out["upheavy5_coin"]=h5.groupby("coin").apply(grp)
    out["upheavy5_year"]=h5.groupby("year").apply(grp)
    h5=h5.copy(); h5["r1q"]=pd.qcut(h5.r1,3,labels=False)
    out["upheavy5_by_daymove_tercile"]=h5.groupby("r1q").apply(grp)
    h5["pastq"]=pd.qcut(h5.r5p,3,labels=False)
    out["upheavy5_by_past5d_tercile"]=h5.groupby("pastq").apply(grp)
    out["spearman_vr_unusual_upH"]=pd.DataFrame({H:stats.spearmanr(d[(d.H==H)&(d.r1>0)].vr,d[(d.H==H)&(d.r1>0)].unusual) for H in [1,3,5,10]},index=["rho","p"])
    out["spearman_vr_unusual_allH"]=pd.DataFrame({H:stats.spearmanr(d[d.H==H].vr,d[d.H==H].unusual) for H in [1,3,5,10]},index=["rho","p"])
    a5=d[d.H==5].copy(); a5["r1q"]=pd.qcut(a5.r1,5,labels=False)
    out["all5_by_daymove_quintile"]=a5.groupby("r1q").apply(grp)
    return out

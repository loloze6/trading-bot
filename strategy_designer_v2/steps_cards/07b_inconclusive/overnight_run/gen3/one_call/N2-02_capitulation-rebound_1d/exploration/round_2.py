def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    allr=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; o=df["open"].values; h=df["high"].values; l=df["low"].values
            n=len(df)
            dep=df["debug_info.components.depth.last_history_value"] if "debug_info.components.depth.last_history_value" in df else pd.Series(np.nan,index=df.index)
            for i in range(0,n-10,10):
                r=c[i+10]/c[i]-1
                r5=c[i+5]/c[i]-1
                rng=h[i]-l[i]
                rows.append(dict(coin=coin,w=w,ts=pd.Timestamp(df["timestamp"].iloc[i]),f=df["forecast"].iloc[i],
                    reg=df["regime"].iloc[i],r=r,r5=r5,depth=dep.iloc[i],
                    up1=c[i]>o[i],clpos=(c[i]-l[i])/rng if rng>0 else np.nan,
                    p1=(c[i]/c[i-1]-1) if i>=1 else np.nan,
                    p3=(c[i]/c[i-3]-1) if i>=3 else np.nan))
    d=pd.DataFrame(rows)
    d["ex"]=d.r-d.groupby("coin").r.transform("mean")
    d["ex5"]=d.r5-d.groupby("coin").r5.transform("mean")
    # market: cross-coin mean return over same start timestamp
    d["day"]=d.ts.dt.floor("D")
    mk=d.groupby("day").r.transform("mean"); cnt=d.groupby("day").r.transform("count")
    d["rel"]=np.where(cnt>=3,d.r-mk,np.nan)
    def s(x):
        x=x.dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),med=x.median(),t=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,pos=(x>0).mean()))
    top=d[d.f>=10]; ir=d[d.reg=="mean_reversion"]
    out={}
    out["top_ex_ex5_rel"]=pd.DataFrame({"ex10":s(top.ex),"ex5":s(top.ex5),"rel_mkt":s(top.rel)})
    out["top_mkt_share"]=pd.Series(dict(corr_r_mk=np.corrcoef(top.r[cnt[top.index]>=3],mk[top.index][cnt[top.index]>=3])[0,1],
        sd_r=top.r.std(),sd_rel=top.rel.std()))
    out["top_by_up1"]=top.groupby("up1").ex.apply(s).unstack()
    out["top_by_clpos_half"]=top.groupby(top.clpos>0.5).ex.apply(s).unstack()
    out["top_by_p3_sign"]=top.groupby(top.p3>0).ex.apply(s).unstack()
    out["inreg_depth_q"]=ir.groupby(pd.qcut(ir.depth,5,labels=False,duplicates="drop")).ex.apply(s).unstack()
    out["inreg_depthq_p5"]=ir.assign(dn=ir.p3<0).groupby([pd.qcut(ir.depth,5,labels=False,duplicates="drop"),"dn"]).ex.apply(s).unstack()
    out["inreg_f5_clpos"]=ir[ir.f>=5].groupby(ir.clpos>0.5).ex.apply(s).unstack()
    out["inreg_f5_rel"]=s(ir[ir.f>=5].rel)
    return out

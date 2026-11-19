def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df["close"].values.astype(float); vol=df["volume"].values.astype(float)
            n=len(cl)
            lr=np.r_[np.nan,np.log(cl[1:]/cl[:-1])]
            s=pd.Series(lr)
            sd168=s.rolling(168,min_periods=100).std().values
            sd720m=pd.Series(sd168).rolling(720,min_periods=200).mean().values
            absmax24=s.abs().rolling(24).max().values
            sumabs24=s.abs().rolling(24).sum().values
            v=pd.Series(vol)
            vmax24=v.rolling(24).max().values; vsum24=v.rolling(24).sum().values
            v168=v.rolling(168,min_periods=100).mean().values
            idx=np.arange(0,n-24,24)
            idx=idx[idx>=24]
            past=np.log(cl[idx]/cl[idx-24])
            past72=np.where(idx>=72,np.log(cl[idx]/cl[np.maximum(idx-72,0)]),np.nan)
            fwd=cl[idx+24]/cl[idx]-1
            fwd2=np.where(idx+72<n,cl[np.minimum(idx+72,n-1)]/cl[np.minimum(idx+24,n-1)]-1,np.nan)
            rows.append(pd.DataFrame({"coin":c,"w":w,"past":past,"z":past/(sd168[idx]*np.sqrt(24)),
               "vr":sd168[idx]/sd720m[idx],"jump":absmax24[idx]/sumabs24[idx],
               "eff":np.abs(past)/sumabs24[idx],"vburst":vmax24[idx]/vsum24[idx],
               "vlev":(vsum24[idx]/24)/v168[idx],"past72":past72,
               "fwd":fwd,"fwd2":fwd2,"wd":pd.to_datetime(df["timestamp"].values[idx]).weekday}))
    d=pd.concat(rows,ignore_index=True)
    d["x"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d["x2"]=d["fwd2"]-d.groupby("coin")["fwd2"].transform("mean")
    d=d.dropna(subset=["z","x"])
    def tt(a): a=a.dropna(); return pd.Series({"mean":a.mean(),"n":len(a),"t":a.mean()/a.std()*np.sqrt(len(a))})
    d["zq"]=d.groupby("coin")["z"].transform(lambda s:pd.qcut(s.rank(method="first"),5,labels=False))
    out["z_quint_fwd24"]=d.groupby("zq")["x"].apply(tt).unstack()
    out["z_quint_fwd24to96"]=d.groupby("zq")["x2"].apply(tt).unstack()
    # signed reversal -sign(z)*x, conditioned on path shape terciles
    d["rev"]=-np.sign(d["z"])*d["x"]
    big=d[d["zq"].isin([0,4])].copy()
    for col in ["jump","eff","vburst","vlev","vr"]:
        big[col+"_t"]=big.groupby("coin")[col].transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=False))
        out["rev_by_"+col]=big.groupby([col+"_t","zq"])["rev"].apply(tt).unstack()
    # regression on all grid bars: x ~ z + z*eff + z*vburst + z*vr
    dd=d.dropna(subset=["eff","vburst","vr","vlev"]).copy()
    for col in ["z","eff","vburst","vr","vlev"]:
        dd[col+"s"]=(dd[col]-dd[col].mean())/dd[col].std()
    X=np.column_stack([np.ones(len(dd)),dd.zs,dd.zs*dd.effs,dd.zs*dd.vbursts,dd.zs*dd.vrs,dd.zs*dd.vlevs,dd.vrs])
    y=dd.x.values
    b,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@b; cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-X.shape[1]))
    out["reg"]=pd.DataFrame({"b":b,"t":b/np.sqrt(np.diag(cov))},index=["c","z","z*eff","z*vburst","z*vr","z*vlev","vr"])
    out["by_weekday"]=d.groupby("wd")["x"].apply(tt).unstack()
    out["rev_by_coin"]=big.groupby(["coin","zq"])["rev"].mean().unstack()
    return out

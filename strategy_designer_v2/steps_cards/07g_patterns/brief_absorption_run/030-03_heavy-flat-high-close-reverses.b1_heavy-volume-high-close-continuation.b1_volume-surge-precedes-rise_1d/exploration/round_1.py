def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            lvr=np.log(v/v.shift(1).rolling(20).mean())
            rng=(h-l)
            cl=((c-l)/rng.replace(0,np.nan))*2-1
            r1=c/c.shift(1)-1
            r10p=c/c.shift(10)-1
            vol20=r1.rolling(20).std()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"lvr":lvr,"cl":cl,"r1":r1,"r10p":r10p,"vol20":vol20,
                             "rngrel":rng/c,"fwd":fwd,"fc":b["forecast"],"wd":ts.dt.weekday,"yr":ts.dt.year})
            df=df.iloc[::H]
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d["z"]=d["ex"]/d.groupby("coin")["fwd"].transform("std")
    out={}
    def tm(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def slope(col,sub=None):
        s=d if sub is None else sub
        s=s.dropna(subset=[col,"z"])
        r=stats.linregress(s[col],s["z"]); return pd.Series({"n":len(s),"slope":r.slope,"t":r.slope/r.stderr})
    sl={}
    for col in ["lvr","cl","r1","r10p","vol20","rngrel"]:
        s=d.copy(); s[col]=s.groupby("coin")[col].transform(lambda x:(x-x.mean())/x.std())
        sl[col]=slope(col,s)
    out["slopes_z_on_feature"]=pd.DataFrame(sl).T
    d["lvrq"]=pd.qcut(d["lvr"],5,labels=False)
    out["by_lvr_quint"]=d.groupby("lvrq")["z"].apply(tm).unstack()
    d["clq"]=pd.qcut(d["cl"],3,labels=["low","mid","high"])
    hv=d[d["lvr"]>d["lvr"].quantile(0.7)]
    out["heavy_by_close"]=hv.groupby("clq")["z"].apply(tm).unstack()
    out["light_by_close"]=d[d["lvr"]<=d["lvr"].quantile(0.7)].groupby("clq")["z"].apply(tm).unstack()
    d["r1s"]=np.sign(d["r1"])
    out["heavy_by_daysign"]=hv.assign(s=np.sign(hv["r1"])).groupby("s")["z"].apply(tm).unstack()
    d["volq"]=d.groupby("coin")["vol20"].transform(lambda x:pd.qcut(x,3,labels=False))
    out["by_volterc"]=d.groupby("volq")["z"].apply(tm).unstack()
    out["lvr_slope_by_volterc"]=pd.DataFrame({q:slope("lvr",d[d.volq==q]) for q in [0,1,2]}).T
    d["mq"]=d.groupby("coin")["r10p"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["by_r10p_quint"]=d.groupby("mq")["z"].apply(tm).unstack()
    out["by_year"]=d.groupby("yr")["z"].apply(tm).unstack()
    out["lvr_slope_by_coin"]=pd.DataFrame({c:slope("lvr",d[d.coin==c]) for c in d.coin.unique()}).T
    return out

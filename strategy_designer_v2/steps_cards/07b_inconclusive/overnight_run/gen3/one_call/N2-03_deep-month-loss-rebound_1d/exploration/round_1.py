def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H=20
    rows=[]
    btc={}
    for w,b in data["bars"]["BTCUSD"].items():
        b=b.sort_values("timestamp").reset_index(drop=True)
        c=b["close"].values
        fr=pd.Series(c).shift(-H)/c-1
        btc[w]=pd.Series(fr.values,index=pd.to_datetime(b["timestamp"]))
        btc[w+"_r60"]=pd.Series((pd.Series(c)/pd.Series(c).shift(60)-1).values,index=pd.to_datetime(b["timestamp"]))
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),
                "ts":pd.to_datetime(b["timestamp"]),"f":b["forecast"].values,
                "fr":(c.shift(-H)/c-1).values,"r20":(c/c.shift(20)-1).values,
                "r60":(c/c.shift(60)-1).values,"r100":(c/c.shift(100)-1).values})
            d["btcfr"]=btc[w].reindex(d["ts"]).values
            d["btcr60"]=btc[w+"_r60"].reindex(d["ts"]).values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["mu"]=D.groupby("coin")["fr"].transform("mean")
    D["ex"]=D["fr"]-D["mu"]
    D["exb"]=D["fr"]-D["btcfr"]
    pos=D[D.f>0]
    q90=pos.f.quantile(0.9)
    D["top"]=D.f>=q90
    N=D[(D.i%H==0)&D.fr.notna()]
    T=N[N.top]
    def st(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"med":x.median(),"hit":(x>0).mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    out["top_all"]=pd.DataFrame({"ex":st(T.ex),"ex_vs_btc":st(T[T.coin!="BTCUSD"].exb)})
    out["top_by_coin"]=T.groupby("coin").ex.apply(st).unstack()
    T2=T.copy();T2["yr"]=T2.ts.dt.year
    out["top_by_year"]=T2.groupby("yr").ex.apply(st).unstack()
    out["top_by_window"]=T.groupby("w").ex.apply(st).unstack()
    Nz=N[N.f>0].copy()
    Nz["fq"]=pd.qcut(Nz.f.rank(method="first"),5,labels=False)
    out["nz_by_fquint"]=Nz.groupby("fq").ex.apply(st).unstack()
    out["zero_f"]=st(N[N.f==0].ex).to_frame("ex")
    Tc=T.copy()
    Tc["long_tr"]=np.where(Tc.r100.isna(),"na",np.where(Tc.r100>0,"r100_up","r100_dn"))
    out["top_by_r100"]=Tc.groupby("long_tr").ex.apply(st).unstack()
    Tc["btc_tr"]=np.where(Tc.btcr60.isna(),"na",np.where(Tc.btcr60>0,"btc60_up","btc60_dn"))
    out["top_by_btc60"]=Tc.groupby("btc_tr").ex.apply(st).unstack()
    Tc["r20b"]=pd.qcut(Tc.r20,3,labels=["deepest","mid","shallow"])
    out["top_by_rawfall"]=Tc.groupby("r20b").ex.apply(st).unstack()
    out["q90"]=float(q90)
    out["sd_ex_top_vs_btcfr_corr"]=float(T[["fr","btcfr"]].corr().iloc[0,1])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            vr=b["volume"]/b["volume"].rolling(30,min_periods=30).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            wick=(np.minimum(b["open"],c)-b["low"])/rng
            r10=c/c.shift(10)-1
            r10z=r10/(sd*np.sqrt(10))
            f3=c.shift(-3)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":r/sd,"vr":vr,"wick":wick,"r10z":r10z,"sd":sd,
                            "f3":f3,"fc":b["forecast"],"wd":ts.dt.weekday,"yr":ts.dt.year})
            d=d.iloc[::3]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["f3"])
    D["ex"]=D["f3"]-D.groupby("coin")["f3"].transform("mean")
    D["sdq"]=D.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    def tab(g):
        x=g["ex"]; return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    Z=D.dropna(subset=["z"])
    Z["zb"]=pd.cut(Z["z"],[-99,-2.5,-1.5,-0.75,0,0.75,1.5,2.5,99])
    out["by_z"]=Z.groupby("zb").apply(tab)
    S=Z[Z["z"]<-1].dropna(subset=["vr","wick"])
    S["vrq"]=pd.qcut(S["vr"],3,labels=False); S["wq"]=pd.qcut(S["wick"],3,labels=False)
    out["fall_z<-1_by_vr_tercile"]=S.groupby("vrq").apply(tab)
    out["fall_z<-1_by_wick_tercile"]=S.groupby("wq").apply(tab)
    U=Z[Z["z"]>1].dropna(subset=["vr"]); U["vrq"]=pd.qcut(U["vr"],3,labels=False)
    out["rise_z>1_by_vr_tercile"]=U.groupby("vrq").apply(tab)
    R=D.dropna(subset=["r10z"]); R["q"]=pd.qcut(R["r10z"],5,labels=False)
    out["by_10d_ret_z_quintile"]=R.groupby("q").apply(tab)
    out["by_vol_quintile"]=D.dropna(subset=["sdq"]).groupby("sdq").apply(tab)
    out["by_weekday_3d"]=D.groupby("wd").apply(tab)
    out["by_coin_fc>0"]=D[D["fc"]>0].groupby("coin").apply(tab)
    out["by_year_fc>0"]=D[D["fc"]>0].groupby("yr").apply(tab)
    # book
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    B=pd.concat(dd); B["yr"]=pd.to_datetime(B["day"]).dt.year
    P=B.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna().reset_index()
    P["yr"]=pd.to_datetime(P["day"]).dt.year; P["wd"]=pd.to_datetime(P["day"]).dt.weekday
    out["book_by_year"]=P.groupby("yr")[["book_return","coin_return"]].agg(["mean","count"])
    out["book_by_window"]=P.groupby("w")[["book_return","coin_return"]].mean()
    out["coin_daily_by_weekday"]=P.groupby("wd")[["book_return","coin_return"]].mean()
    return out

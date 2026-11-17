def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df[["timestamp","close","volume"]].copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d=d.sort_values("ts").reset_index(drop=True)
            d["r"]=d["close"].pct_change()
            d["r2b"]=d["close"]/d["close"].shift(2)-1
            d["rn1"]=d["close"].shift(-1)/d["close"]-1
            d["rn2"]=d["close"].shift(-2)/d["close"]-1
            d["vol20"]=d["r"].rolling(20,min_periods=10).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["z2"]=d["r2b"]/(d["vol20"].shift(2)*np.sqrt(2))
            d["vrel"]=d["volume"]/d["volume"].rolling(30,min_periods=10).median().shift(1)
            d["wd"]=d["ts"].dt.weekday; d["year"]=d["ts"].dt.year
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["ex1"]=A["rn1"]-A.groupby("coin")["rn1"].transform("mean")
    A["ex2"]=A["rn2"]-A.groupby("coin")["rn2"].transform("mean")
    out={}
    def slope_by(df,x,y,by):
        res={}
        for k,s in df.dropna(subset=[x,y]).groupby(by):
            if len(s)<30: continue
            sl=stats.linregress(s[x].clip(-5,5),s[y]); res[k]={"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(s)}
        return pd.DataFrame(res).T
    S=A[A["wd"]==6]
    out["sun: 2-day weekend z -> mon-tue ex, by year"]=slope_by(S,"z2","ex2","year")
    S2=S.dropna(subset=["z2","ex2"])
    out["sun: weekend z2 -> mon-tue ex, pooled"]=slope_by(S2.assign(k=1),"z2","ex2","k")
    out["sun: z2 -> mon-tue ex, by coin"]=slope_by(S,"z2","ex2","coin")
    # falls only vs rises only
    F=S2[S2["z2"]<0]; R=S2[S2["z2"]>0]
    out["sun: falls / rises slope"]=pd.concat([slope_by(F.assign(k="fall"),"z2","ex2","k"),slope_by(R.assign(k="rise"),"z2","ex2","k")])
    # volume interaction on sunday
    S3=S2.dropna(subset=["vrel"]).copy()
    S3["vq"]=pd.qcut(S3["vrel"].rank(method="first"),3,labels=False)
    out["sun: z2->mon-tue slope by weekend vol tercile"]=slope_by(S3,"z2","ex2","vq")
    # Saturday z -> sunday, by year
    out["sat z -> sun ex1, by year"]=slope_by(A[A["wd"]==5],"z","ex1","year")
    # Friday z -> saturday, by year
    out["fri z -> sat ex1, by year"]=slope_by(A[A["wd"]==4],"z","ex1","year")
    # weekday-of-day mean by year (day returned = wd+1)
    t=A.dropna(subset=["ex1"]).groupby(["year","wd"])["ex1"].mean().unstack()
    out["next-day ex mean by year x cond weekday"]=t
    # weekday non-weekend reversal: all weekday slopes Mon-Thu pooled
    out["mon-thu z -> next ex1 pooled"]=slope_by(A[A["wd"].isin([0,1,2,3])].assign(k=1),"z","ex1","k")
    return out

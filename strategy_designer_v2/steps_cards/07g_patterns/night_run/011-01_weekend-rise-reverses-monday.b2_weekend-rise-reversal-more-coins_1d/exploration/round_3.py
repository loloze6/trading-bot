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
            d["rn1"]=d["close"].shift(-1)/d["close"]-1
            d["rn2"]=d["close"].shift(-2)/d["close"]-1
            d["vol20"]=d["r"].rolling(20,min_periods=10).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["vrel"]=d["volume"]/d["volume"].rolling(28,min_periods=10).median().shift(1)
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
    W=A[A["wd"].isin([5,6])]
    out["sat+sun z -> next-day ex, by year"]=slope_by(W,"z","ex1","year")
    bc=slope_by(W,"z","ex1","coin")
    out["sat+sun z -> next-day ex, by coin"]=bc
    out["coins negative slope (of n)"]=f"{int((bc['slope']<0).sum())} of {len(bc)}"
    S=W.dropna(subset=["vrel","z","ex1"]).copy()
    S["vq"]=S.groupby("wd")["vrel"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["sat+sun z -> next ex by own-volume tercile"]=slope_by(S,"z","ex1","vq")
    D=A[A["wd"].isin([0,1,2,3])].dropna(subset=["vrel","z","ex1"]).copy()
    D["vq"]=pd.qcut(D["vrel"].rank(method="first"),3,labels=False)
    out["mon-thu z -> next ex by volume tercile"]=slope_by(D,"z","ex1","vq")
    # weekend z quintile -> next day ex
    B=W.dropna(subset=["z","ex1"]).copy()
    B["q"]=pd.qcut(B["z"],5,labels=False)
    g=B.groupby("q")["ex1"]
    out["sat+sun z quintile -> next-day ex"]=pd.DataFrame({"z":B.groupby("q")["z"].mean(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # difference weekend slope vs weekday slope
    a=stats.linregress(W.dropna(subset=["z","ex1"])["z"].clip(-5,5),W.dropna(subset=["z","ex1"])["ex1"])
    b=stats.linregress(A[A["wd"].isin([0,1,2,3])].dropna(subset=["z","ex1"])["z"].clip(-5,5),A[A["wd"].isin([0,1,2,3])].dropna(subset=["z","ex1"])["ex1"])
    out["weekend minus mon-thu slope, z"]=pd.Series({"wkend":a.slope,"wkday":b.slope,"diff":a.slope-b.slope,"z":(a.slope-b.slope)/np.sqrt(a.stderr**2+b.stderr**2)})
    # friday continuation by coin
    fc=slope_by(A[A["wd"]==4],"z","ex1","coin")
    out["fri z -> sat, coins positive"]=f"{int((fc['slope']>0).sum())} of {len(fc)}"
    return out

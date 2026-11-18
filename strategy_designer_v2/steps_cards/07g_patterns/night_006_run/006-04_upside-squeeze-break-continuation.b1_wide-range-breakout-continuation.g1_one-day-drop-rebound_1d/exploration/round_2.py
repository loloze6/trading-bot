def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r1=c.pct_change(); fwd=c.shift(-1)/c-1
            sd=r1.rolling(60,min_periods=20).std()
            rng=(b["high"]-b["low"])/c
            rngz=rng.rolling(5).mean()/rng.rolling(60,min_periods=20).mean()
            volz=b["volume"].rolling(5).mean()/b["volume"].rolling(60,min_periods=20).mean()
            vol1=b["volume"]/b["volume"].rolling(60,min_periods=20).mean()
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            fwd5=c.shift(-5)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"z":r1/sd,"fwd":fwd,"rngz":rngz,"volz":volz,"vol1":vol1,
                "clv":clv,"sd":sd,"pos":np.arange(len(b)),"f5":fwd5.abs()/(sd*np.sqrt(5)),
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "sdrel":sd/sd.rolling(365,min_periods=60).median()})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["fwd","z","sd"])
    mu=d.groupby("coin")["fwd"].mean(); d["ex"]=d["fwd"]-d["coin"].map(mu)
    d["fall"]=(-d["z"]).clip(lower=0); d["rise"]=d["z"].clip(lower=0)
    out={}
    # joint regression
    x=d.dropna(subset=["rngz","volz","clv"]).copy()
    X=np.column_stack([np.ones(len(x)),x["fall"],x["rise"],x["rngz"]-1,x["volz"]-1,x["clv"]-0.5])
    beta,res,_,_=np.linalg.lstsq(X,x["ex"].values,rcond=None)
    e=x["ex"].values-X@beta; s2=e@e/(len(x)-X.shape[1]); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["joint OLS"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","fall","rise","rngz","volz","clv"])
    # fall slope by own-vol relative tercile (sd vs its own 1y median)
    def sl(x):
        x=x[x["z"]<0]
        if len(x)<30: return pd.Series({"slope":np.nan,"t":np.nan,"n":len(x)})
        r=stats.linregress(x["fall"],x["ex"]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(x)})
    y=d.dropna(subset=["sdrel"]).copy()
    y["t3"]=pd.qcut(y["sdrel"].rank(method="first"),3,labels=False)
    out["fall slope by vol vs own 1y median tercile"]=y.groupby("t3").apply(sl)
    # fall slope by 1-day volume tercile
    y=d.dropna(subset=["vol1"]).copy()
    y["t3"]=y.groupby("coin")["vol1"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fall slope by day volume tercile"]=y.groupby("t3").apply(sl)
    # close location on down days
    y=d[(d["z"]<0)].dropna(subset=["clv"]).copy()
    y["q"]=pd.qcut(y["clv"].rank(method="first"),5,labels=False)
    o=y.groupby("q")["ex"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["down days: ex by close-location quint"]=o.drop(columns="std")
    # compression -> 5d abs move, non-overlapping grid
    g=d[d["pos"]%5==0].dropna(subset=["rngz","f5"]).copy()
    g["q"]=g.groupby("coin")["rngz"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["5d abs move (in sd units) by range-compression quint, non-overlap"]=g.groupby("q")["f5"].agg(["mean","median","count"])
    # book: by year, worst days
    br=[]
    for coin, ws in data["days"].items():
        for w,dd in ws.items():
            t=dd[["day","book_return","coin_return"]].copy(); t["w"]=w; t["coin"]=coin; br.append(t)
    br=pd.concat(br); bk=br.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["yr"]=pd.to_datetime(bk["day"]).dt.year
    out["book by year"]=bk.groupby("yr").agg(mean=("book_return","mean"),sd=("book_return","std"),hold=("coin_return","mean"),n=("book_return","count"))
    q=bk["book_return"].quantile([0.01,0.99])
    out["book worst1% mean, best1% mean, coin same days"]=pd.DataFrame({
        "book":[bk.loc[bk.book_return<=q[0.01],"book_return"].mean(),bk.loc[bk.book_return>=q[0.99],"book_return"].mean()],
        "coin":[bk.loc[bk.book_return<=q[0.01],"coin_return"].mean(),bk.loc[bk.book_return>=q[0.99],"coin_return"].mean()]},index=["worst","best"])
    return out

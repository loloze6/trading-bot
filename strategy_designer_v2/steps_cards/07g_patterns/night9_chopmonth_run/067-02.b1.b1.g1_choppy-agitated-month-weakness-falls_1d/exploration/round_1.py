def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "r1":r1,"r7p":c/c.shift(7)-1,"r30":c/c.shift(30)-1,"r60":c/c.shift(60)-1,
                "vol30":r1.rolling(30).std(),"fc":b["forecast"],"inprof":(b["regime"]=="unknown"),
                "pos":b["postRebalance_current_allocation"],
                "rng":(b["high"]-b["low"])/c,"clpos":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            df["volrel"]=df["vol30"]/df["vol30"].expanding(30).median()
            df["f1"]=r1.shift(-1); df["f7"]=c.shift(-7)/c-1
            df["i"]=np.arange(len(df))
            daily.append(df)
    D=pd.concat(daily,ignore_index=True)
    D["day"]=D["ts"].dt.floor("D")
    G=D[(D["i"]%7==0)&D["f7"].notna()].copy()
    G["drift"]=G.groupby("coin")["f7"].transform("mean")
    G["ex"]=G["f7"]-G["drift"]
    def tday(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna().groupby("d")["v"].mean()
        n=len(x); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"days":n})
    out={}
    def bucket(df,col,q=5,lab=""):
        d=df.dropna(subset=[col,"ex"]).copy()
        d["b"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        r=d.groupby("b").apply(lambda g: pd.concat([pd.Series({"x_mean":g[col].mean(),"n":len(g)}),tday(g["ex"],g["day"])]))
        return r
    out["ex7 by r30 quint, all"]=bucket(G,"r30")
    out["ex7 by r30 quint, in profile"]=bucket(G[G.inprof],"r30",4)
    # trend buckets
    G["trend"]=pd.cut(G["r60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G["agit"]=np.where(G["volrel"]>1,"ag","calm")
    out["ex7 by trend x agit"]=G.dropna(subset=["trend"]).groupby(["trend","agit"]).apply(lambda g: tday(g["ex"],g["day"]))
    out["ex7 by r7 past quint"]=bucket(G,"r7p")
    out["ex7 by volrel quint"]=bucket(G,"volrel")
    out["ex7 by range/vol quint"]=bucket(G.assign(rz=G["rng"]/G["vol30"]),"rz")
    # daily: next-day return after big 1d move scaled by vol
    D["z1"]=D["r1"]/D["vol30"].shift(1)
    D["f1ex"]=D["f1"]-D.groupby("coin")["f1"].transform("mean")
    d1=D.dropna(subset=["z1","f1ex"]).copy(); d1["b"]=pd.qcut(d1["z1"],5,labels=False)
    out["next-day ex by z1 quint"]=d1.groupby("b").apply(lambda g: pd.concat([pd.Series({"z":g["z1"].mean()}),tday(g["f1ex"],g["day"])]))
    D["wd"]=D["ts"].dt.dayofweek
    out["daily ret by weekday"]=D.dropna(subset=["r1"]).groupby("wd").apply(lambda g: tday(g["r1"],g["day"]))
    d1["cb"]=pd.qcut(d1["clpos"],5,labels=False,duplicates="drop")
    out["next-day ex by close-in-range quint"]=d1.dropna(subset=["cb"]).groupby("cb").apply(lambda g: tday(g["f1ex"],g["day"]))
    # book
    days=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            days.append(d.assign(coin=coin,w=w))
    Y=pd.concat(days); bk=Y.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["mean","std","count"])
    return out

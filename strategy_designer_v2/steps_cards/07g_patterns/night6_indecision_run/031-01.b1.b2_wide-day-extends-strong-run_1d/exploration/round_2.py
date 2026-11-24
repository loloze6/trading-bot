import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["fwd3"]=c.shift(-3)/c-1
            d["r5"]=c/c.shift(5)-1
            d["r1"]=c/c.shift(1)-1
            d["r20"]=c/c.shift(20)-1
            d["rm"]=(h-l)/(h-l).rolling(20,min_periods=20).mean()
            d["body"]=(c-o)/(h-l).replace(0,np.nan)
            d["clv"]=(c-l)/(h-l).replace(0,np.nan)
            lr=np.log(c).diff()
            d["volratio"]=lr.rolling(5).std()/lr.rolling(60,min_periods=30).std()
            d["fc"]=b["forecast"].astype(float)
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["grid"]=(np.arange(len(b))%3==0)
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    G=A[A["grid"]&A["fwd3"].notna()].copy()
    drift=G.groupby("coin")["fwd3"].mean(); usual=G.groupby("coin")["fwd3"].std()
    G["u"]=G["fwd3"]-G["coin"].map(drift)
    G["s"]=G["u"]/G["coin"].map(usual)
    G["day"]=G["ts"].dt.floor("D")
    def summ(df):
        n=len(df)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan,"days":0,"strength":np.nan})
        m=df["u"].mean()
        g=df.groupby("day")["u"]
        ds=g.sum(); cnt=g.count()
        se=np.sqrt(((ds-cnt*m)**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t":m/se if se>0 else np.nan,"days":len(ds),"strength":df["s"].mean()})
    out={}
    for f in ["r5","rm","body","clv","r1","r20","volratio"]:
        q=pd.qcut(G[f],5,labels=False,duplicates="drop")
        out["q "+f]=G.groupby(q).apply(summ)
    for name,sub in [("up5",G[G["r5"]>0]),("down5",G[G["r5"]<0])]:
        sub=sub.copy()
        sub["wide"]=pd.qcut(sub["rm"],3,labels=False)
        sub["flat"]=np.where(sub["body"].abs()<0.25,"flat","body")
        out[name+": rangetercile x flat"]=sub.groupby(["wide","flat"]).apply(summ)
    out["weekday"]=G.groupby(G["ts"].dt.dayofweek).apply(summ)
    out["coin"]=G.groupby("coin").apply(summ)
    G["pos"]=np.where(G["alloc"]>0,"long","flat")
    out["position"]=G.groupby("pos").apply(summ)
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; dd.append(d)
    D=pd.concat(dd,ignore_index=True); D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    out["book coin corr"]=float(bk.corr().iloc[0,1])
    q=pd.qcut(bk["coin_return"],5,labels=False)
    out["book by coin-day quintile"]=bk.groupby(q).agg(["mean","count"])
    out["book by year"]=bk.groupby(bk.index.year).agg(["mean","std","count"])
    return out

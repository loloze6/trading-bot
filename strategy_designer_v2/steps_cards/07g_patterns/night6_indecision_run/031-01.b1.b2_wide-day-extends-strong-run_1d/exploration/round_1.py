import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            rng=(h-l)/c
            d=pd.DataFrame({"coin":coin,"win":w})
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["fwd3"]=c.shift(-3)/c-1
            d["r5"]=c/c.shift(5)-1
            d["r1"]=c/c.shift(1)-1
            d["r20"]=c/c.shift(20)-1
            d["rm"]=(h-l)/(h-l).rolling(20,min_periods=20).mean()
            d["body"]=(c-o)/(h-l).replace(0,np.nan)  # signed body share
            d["clv"]=((c-l)/(h-l).replace(0,np.nan))  # close location
            d["vol20"]=np.log(c).diff().rolling(20).std()
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
        if len(df)<5: return pd.Series({"n":len(df),"mean":np.nan,"t":np.nan,"days":0})
        ds=df.groupby("day")["u"].sum(); nd=len(ds)
        m=df["u"].mean()
        # clustered t: sum per day, mean over cases
        se=np.sqrt((ds - df.groupby("day")["u"].count()*m).pow(2).sum())/len(df)
        return pd.Series({"n":len(df),"mean":m,"t":m/se if se>0 else np.nan,"days":nd,"strength":df["s"].mean()})
    out={}
    for f in ["r5","rm","body","clv","r1","r20","vol20"]:
        q=pd.qcut(G[f],5,labels=False,duplicates="drop")
        out["by quintile "+f]=G.groupby(q).apply(summ)
    # brief's concept: after a 5-day run up, wide flat day
    up=G[G["r5"]>0].copy()
    up["wide"]=pd.qcut(up["rm"],3,labels=["narrow","mid","wide"])
    up["flat"]=np.where(up["body"].abs()<0.25,"flat","body")
    out["up-run: range x flat"]=up.groupby(["wide","flat"]).apply(summ)
    dn=G[G["r5"]<0].copy()
    dn["wide"]=pd.qcut(dn["rm"],3,labels=["narrow","mid","wide"])
    dn["flat"]=np.where(dn["body"].abs()<0.25,"flat","body")
    out["down-run: range x flat"]=dn.groupby(["wide","flat"]).apply(summ)
    out["by weekday"]=G.groupby(G["ts"].dt.dayofweek).apply(summ)
    out["by coin"]=G.groupby("coin").apply(summ)
    # in-position vs not
    G["pos"]=np.where(G["alloc"]>0,"long","flat")
    out["by position"]=G.groupby("pos").apply(summ)
    # book daily: largest gain/loss days context
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; dd.append(d)
    D=pd.concat(dd); D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    out["book vs coin daily corr"]=float(bk.corr().iloc[0,1])
    q=pd.qcut(bk["coin_return"],5,labels=False)
    out["book by coin-day quintile"]=bk.groupby(q).agg(["mean","count"])
    out["book by year"]=bk.groupby(bk.index.year).agg(["mean","std","count"])
    return out

import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.reset_index(drop=True).copy()
            c=d["close"]; r1=c.pct_change()
            vol=r1.rolling(20,min_periods=20).std()
            d["z"]=r1/vol
            d["vr"]=d["volume"]/d["volume"].shift(1).rolling(20,min_periods=20).mean()
            rng=(d["high"]-d["low"]).replace(0,np.nan)
            d["wick"]=(np.minimum(d["open"],c)-d["low"])/rng
            d["uwick"]=(d["high"]-np.maximum(d["open"],c))/rng
            d["vol20"]=vol
            d["r5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["f3"]=c.shift(-3)/c-1
            d["f1"]=c.shift(-1)/c-1
            d["pos"]=np.arange(len(d))
            d["coin"]=coin; d["win"]=w
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.dayofweek
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d[["coin","win","pos","z","vr","wick","uwick","vol20","r5","r20","f3","f1","wd","yr","postRebalance_current_allocation"]])
    A=pd.concat(rows,ignore_index=True)
    g3=A[A.pos%3==0].dropna(subset=["f3"]).copy()
    g3["ex"]=g3["f3"]-g3.groupby("coin")["f3"].transform("mean")
    g1=A.dropna(subset=["f1"]).copy()
    g1["ex"]=g1["f1"]-g1.groupby("coin")["f1"].transform("mean")
    def summ(df,key):
        o=df.groupby(key)["ex"].agg(["mean","std","count"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o.drop(columns="std")
    out={}
    G=g3.dropna(subset=["z"]).copy()
    G["zq"]=G.groupby("coin")["z"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["f3ex_by_zquint"]=summ(G,"zq")
    G["vq"]=G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False))
    out["f3ex_by_volterc"]=summ(G,"vq")
    G2=G.dropna(subset=["r20"]).copy()
    G2["mq"]=G2.groupby("coin")["r20"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["f3ex_by_r20quint"]=summ(G2,"mq")
    G2["m5"]=G2.groupby("coin")["r5"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["f3ex_by_r5quint"]=summ(G2,"m5")
    G3=G.dropna(subset=["vr"]).copy()
    G3["vrq"]=G3.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["f3ex_by_vrquint"]=summ(G3,"vrq")
    G3["wq"]=G3.groupby("coin")["wick"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["f3ex_by_lowerwickquint"]=summ(G3,"wq")
    G3["uq"]=G3.groupby("coin")["uwick"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["f3ex_by_upperwickquint"]=summ(G3,"uq")
    sf=G3[G3.z<=-1.5].copy()
    sf["grp"]=np.where(sf.vr>=2,"hiV","loV")+np.where(sf.wick>=0.3,"_wick","_nowick")
    out["sharpfall_groups_f3ex"]=summ(sf,"grp")
    su=G3[G3.z>=1.5].copy()
    su["grp"]=np.where(su.vr>=2,"hiV","loV")
    out["sharprise_groups_f3ex"]=summ(su,"grp")
    out["f1ex_by_weekday"]=summ(g1,"wd")
    out["f3ex_by_coin_zslope"]=G.groupby("coin").apply(lambda d: pd.Series(stats.linregress(d.z,d.ex)[:4:3] if False else [stats.linregress(d.z,d.ex).slope, stats.linregress(d.z,d.ex).slope/stats.linregress(d.z,d.ex).stderr, len(d)],index=["slope","t","n"]))
    out["f3ex_by_year"]=summ(G,"yr")
    # book
    days=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy(); x["coin"]=coin; days.append(x)
    D=pd.concat(days).dropna(subset=["book_return"])
    out["book_by_coin"]=D.groupby("coin").agg(mean_book=("book_return","mean"),mean_coin=("coin_return","mean"),active=("book_return",lambda s:(s!=0).mean()))
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): x=t.copy(); x["coin"]=coin; tr.append(x)
    T=pd.concat(tr)
    T["dur_d"]=T.duration_minutes/1440
    out["trades"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda s:(s>0).mean()),dur=("dur_d","median"))
    return out

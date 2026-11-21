def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        recs=[]
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=10).std()
            past5=c/c.shift(5)-1
            past1=r1
            hi30=c.rolling(30,min_periods=15).max(); lo30=c.rolling(30,min_periods=15).min()
            pos30=(c-lo30)/(hi30-lo30)
            fwd=c.shift(-H)/c-1
            rng=(df["high"]-df["low"])/c
            vchg=np.log(df["volume"].replace(0,np.nan)/df["volume"].rolling(20,min_periods=10).mean())
            ts=pd.to_datetime(df["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"fwd":fwd,"fc":df["forecast"],"vol":vol,
                            "p5z":past5/(vol*np.sqrt(5)),"p1z":past1/vol,"pos30":pos30,
                            "rng":rng/vol,"vchg":vchg,"wd":ts.dt.weekday,"alloc":df["postRebalance_current_allocation"]})
            d=d.iloc[::H]
            recs.append(d)
        cd=pd.concat(recs)
        g=cd["fwd"].dropna()
        cd["unus"]=(cd["fwd"]-g.mean())/g.std()
        cd["unus_raw"]=cd["fwd"]-g.mean()
        rows.append(cd)
    A=pd.concat(rows).dropna(subset=["fwd"])
    def summ(key,q=5):
        x=A.dropna(subset=[key]).copy()
        if q: x["b"]=x.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        else: x["b"]=x[key]
        out=x.groupby("b").agg(n=("unus","size"),strength=("unus","mean"),unus_pct=("unus_raw",lambda s:100*s.mean()),sd=("unus","std"))
        out["t"]=out.strength/(out.sd/np.sqrt(out.n))
        return out.drop(columns="sd").round(3)
    res={}
    res["p5z"]=summ("p5z"); res["p1z"]=summ("p1z"); res["vol"]=summ("vol")
    res["pos30"]=summ("pos30"); res["rng"]=summ("rng"); res["vchg"]=summ("vchg")
    res["weekday"]=summ("wd",q=None)
    A["fcpos"]=(A.fc>0).astype(int); res["fc_on"]=summ("fcpos",q=None)
    res["per_coin_p5z_top_minus_bottom"]=A.dropna(subset=["p5z"]).groupby("coin").apply(lambda x: pd.Series({"corr":x["p5z"].corr(x["unus"]),"n":len(x)})).round(3)
    return res

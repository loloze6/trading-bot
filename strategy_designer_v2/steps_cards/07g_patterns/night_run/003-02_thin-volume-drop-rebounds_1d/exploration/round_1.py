def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float); v=b["volume"].astype(float)
            r1=cl.pct_change()
            vr=v/v.shift(1).rolling(30,min_periods=20).mean()
            r5p=cl/cl.shift(5)-1
            vol20=r1.rolling(20,min_periods=10).std()
            fwd=cl.shift(-5)/cl-1
            n=len(b)
            for i in range(0,n,5):
                if i+5<n:
                    rows.append(dict(coin=c,win=w,r1=r1[i],vr=vr[i],r5p=r5p[i],vol=vol20[i],
                        fwd=fwd[i],fc=b["forecast"][i],wd=pd.Timestamp(b["timestamp"][i]).weekday(),
                        yr=pd.Timestamp(b["timestamp"][i]).year))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d=d.dropna(subset=["r1","vr","ex"])
    def g(df,key):
        o=df.groupby(key)["ex"].agg(["mean","std","count"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o.round(4)
    # within-coin ranks
    d["r1q"]=d.groupby("coin")["r1"].transform(lambda s: pd.qcut(s,5,labels=False))
    d["vrq"]=d.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,3,labels=False))
    d["r5q"]=d.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s,5,labels=False))
    d["volq"]=d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False))
    out={}
    out["by r1 quintile"]=g(d,"r1q")
    out["by r1q x vr tercile"]=g(d,["r1q","vrq"])
    out["by 5d past ret quintile"]=g(d,"r5q")
    out["by vol tercile"]=g(d,"volq")
    out["by vol tercile x r1 extreme"]=g(d[d.r1q.isin([0,4])],["volq","r1q"])
    out["by weekday"]=g(d,"wd")
    out["by coin"]=g(d,"coin")
    out["by year, fc>0"]=g(d[d.fc>0],"yr")
    # correlation tests
    for k in ["r1","r5p","vr"]:
        rr=stats.spearmanr(d[k],d["ex"],nan_policy="omit")
        out["spearman "+k]=f"{rr.correlation:.4f} p={rr.pvalue:.4f} n={d[k].notna().sum()}"
    # book
    bk=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["book_return","coin_return"]].copy(); x["coin"]=c; bk.append(x)
    bk=pd.concat(bk).dropna()
    out["book vs coin corr"]=f"{bk.book_return.corr(bk.coin_return):.3f}"
    q=bk.book_return.quantile([0.01,0.99])
    out["book tails"]=f"p1={q.iloc[0]:.4f} p99={q.iloc[1]:.4f} mean={bk.book_return.mean():.6f}"
    return out

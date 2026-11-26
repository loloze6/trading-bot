def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            n=len(b)
            r60=c/c.shift(60)-1
            r10=c/c.shift(10)-1
            r1=c.pct_change()
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            vol30=r1.rolling(30).std()
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            f5=c.shift(-5)/c-1
            for i in range(0,n-5,5):
                rows.append(dict(coin=coin,w=w,r60=r60[i],r10=r10[i],r1=r1[i],vr=vr[i],vol30=vol30[i],
                    rng=rng[i],clpos=clpos[i],f5=f5[i],fc=b["forecast"][i],
                    al=b["postRebalance_current_allocation"][i],
                    wd=pd.Timestamp(b["timestamp"][i]).dayofweek))
    d=pd.DataFrame(rows).dropna(subset=["f5"])
    drift=d.groupby("coin")["f5"].mean()
    d["u5"]=d["f5"]-d["coin"].map(drift)
    def tab(g):
        x=g["u5"]; return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    d["trend"]=pd.cut(d["r60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["by trend"]=d.groupby("trend").apply(tab)
    d["vrq"]=pd.qcut(d["vr"],5,labels=False)
    out["trend x volratio quintile"]=d.groupby(["trend","vrq"]).apply(tab)
    d["r10q"]=pd.qcut(d["r10"],5,labels=False)
    out["trend x r10 quintile"]=d.groupby(["trend","r10q"]).apply(tab)
    d["r1q"]=pd.qcut(d["r1"],5,labels=False)
    out["trend x r1 quintile"]=d.groupby(["trend","r1q"]).apply(tab)
    d["volq"]=d.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["trend x vol30 tercile"]=d.groupby(["trend","volq"]).apply(tab)
    d["clq"]=pd.qcut(d["clpos"],4,labels=False)
    out["trend x close position"]=d.groupby(["trend","clq"]).apply(tab)
    out["weekday"]=d.groupby("wd").apply(tab)
    inpos=d[d["al"]>0]
    inpos["fcq"]=pd.qcut(inpos["fc"],4,labels=False,duplicates="drop")
    out["in position by forecast quartile"]=inpos.groupby("fcq").apply(tab)
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    out["book by window"]=D.groupby("w").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    out["book by coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    t=[]
    for coin,wins in data["trades"].items():
        for w,x in wins.items():
            if len(x): x=x.copy(); x["coin"]=coin; t.append(x)
    T=pd.concat(t)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    T["efq"]=pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
    out["trades by entry forecast quartile"]=T.groupby("efq")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out

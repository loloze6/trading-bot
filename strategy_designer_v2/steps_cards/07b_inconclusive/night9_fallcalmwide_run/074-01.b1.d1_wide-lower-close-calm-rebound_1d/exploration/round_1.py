def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        drift[coin]=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            width=(h-l)/c/sd
            loc=(h-c)/(h-l)
            fc=b["forecast"].astype(float)
            for i in range(len(b)):
                if fc.iloc[i]>0:
                    d={"coin":coin,"w":w,"year":pd.Timestamp(b["timestamp"].iloc[i]).year,
                       "fc":fc.iloc[i],"width":width.iloc[i],"loc":loc.iloc[i],
                       "dayret":c.iloc[i]/c.iloc[i-1]-1 if i>0 else np.nan,
                       "body":(c.iloc[i]-o.iloc[i])/(h.iloc[i]-l.iloc[i]),
                       "day":pd.Timestamp(b["timestamp"].iloc[i]).normalize()}
                    for H in (1,2,3,5,10):
                        d[f"r{H}"]=(c.iloc[i+H]/c.iloc[i]-1-H*drift[coin]) if i+H<len(b) else np.nan
                    rows.append(d)
    df=pd.DataFrame(rows)
    def summ(g):
        out={}
        for H in (1,2,3,5,10):
            x=g[f"r{H}"].dropna()
            out[f"m{H}"]=x.mean(); out[f"t{H}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"]=len(g)
        return pd.Series(out)
    res={"all":summ(df).to_frame().T}
    res["by_coin"]=df.groupby("coin").apply(summ)
    res["by_window"]=df.groupby("w").apply(summ)
    res["by_year"]=df.groupby("year").apply(summ)
    df["wq"]=pd.qcut(df["width"].rank(method="first"),4,labels=["q1","q2","q3","q4"])
    res["by_width_q"]=df.groupby("wq").apply(summ)
    df["lq"]=pd.cut(df["loc"],[0.5,0.7,0.85,1.01],labels=["mid","low","verylow"])
    res["by_loc"]=df.groupby("lq").apply(summ)
    df["dq"]=pd.qcut(df["dayret"].rank(method="first"),3,labels=["bigfall","mid","rise_or_small"])
    res["by_dayret"]=df.groupby("dq").apply(summ)
    res["by_weekday"]=df.groupby(df["day"].dt.dayofweek).apply(summ)
    res["corr"]=pd.Series({k:df[[k,"r1"]].dropna().corr().iloc[0,1] for k in ["fc","width","loc","dayret","body"]})
    return res

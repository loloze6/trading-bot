def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            n=len(c)
            for i in range(0,n-7,7):
                allr.append(c[i+7]/c[i]-1)
        drift=np.mean(allr) if allr else np.nan
        sd=np.std(allr,ddof=1) if len(allr)>2 else np.nan
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            lr=np.log(c[1:]/c[:-1])
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n-7,7):
                fwd=c[i+7]/c[i]-1
                r30=c[i]/c[i-30]-1 if i>=30 else np.nan
                r7=c[i]/c[i-7]-1 if i>=7 else np.nan
                r1=c[i]/c[i-1]-1 if i>=1 else np.nan
                v30=np.std(lr[i-30:i]) if i>=30 else np.nan
                hi=b["high"].values[i];lo=b["low"].values[i]
                rows.append(dict(coin=coin,w=w,day=ts[i].date(),wd=ts[i].weekday(),
                  reg=b["regime"].iloc[i],fwd=fwd,ex=fwd-drift,z=(fwd-drift)/sd,
                  r30=r30,r7=r7,r1=r1,v30=v30,clpos=(c[i]-lo)/(hi-lo) if hi>lo else np.nan,
                  fc=b["forecast"].iloc[i]))
    d=pd.DataFrame(rows)
    out={}
    out["regime counts"]=d.groupby("reg").size()
    def slope(df,x):
        df=df.dropna(subset=[x,"z"])
        if len(df)<20: return pd.Series(dict(n=len(df)))
        r=stats.linregress(df[x],df["z"])
        return pd.Series(dict(n=len(df),days=df["day"].nunique(),slope=r.slope,t=r.slope/r.stderr,corr=r.rvalue))
    res={}
    for reg in d["reg"].unique():
        for x in ["r30","r7","r1","v30","clpos"]:
            res[(reg,x)]=slope(d[d.reg==reg],x)
    for x in ["r30","r7","r1","clpos"]:
        res[("all",x)]=slope(d,x)
    out["slopes of z on feature"]=pd.DataFrame(res).T
    d["q30"]=d.groupby("reg")["r30"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["r30 quintile x regime: mean z, n"]=d.groupby(["reg","q30"])["z"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d["q7"]=pd.qcut(d["r7"],5,labels=False)
    out["r7 quintile all: mean z"]=d.groupby("q7")["z"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d["qv"]=d.groupby("coin")["v30"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["vol tercile (per coin): mean z, mean ex"]=d.groupby("qv")[["z","ex"]].agg(["mean","count"])
    out["weekday: mean z"]=d.groupby("wd")["z"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["window: mean z"]=d.groupby("w")["z"].agg(["mean","count"])
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;t["w"]=w;dd.append(t)
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    br=D.dropna(subset=["book_return"])
    out["book daily by window"]=br.groupby("w")["book_return"].agg(["mean","std","count"])
    q=br["book_return"]
    big=br[q.abs()>q.abs().quantile(0.98)]
    out["largest book days: sign counts, mean coin ret"]=big.groupby(np.sign(big["book_return"]))["coin_return"].agg(["count","mean"])
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy();t["coin"]=coin;tr.append(t)
    T=pd.concat(tr)
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out

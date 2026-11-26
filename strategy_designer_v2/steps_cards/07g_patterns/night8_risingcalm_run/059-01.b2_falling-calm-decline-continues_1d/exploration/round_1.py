def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30).std()
            b["s14"]=(c/c.shift(14)-1)/(sd30*np.sqrt(14))
            b["r60"]=c/c.shift(60)-1
            b["r1"]=r1
            b["r1z"]=r1/sd30
            b["sd30"]=sd30
            b["rng"]=(b["high"]-b["low"])/c/sd30
            b["clpos"]=(c-b["low"])/(b["high"]-b["low"])
            b["fwd"]=c.shift(-H)/c-1
            b["fwd1"]=c.shift(-1)/c-1
            b["inprof"]=(b["regime"]=="unknown").astype(int)
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"]=coin; b["w"]=w
            g=b.iloc[::H]
            rows.append(g)
    d=pd.concat(rows)
    d=d.dropna(subset=["fwd"])
    mu=d.groupby("coin")["fwd"].mean()
    d["ex"]=d["fwd"]-d["coin"].map(mu)
    sdv=d.groupby("coin")["fwd"].std()
    d["exz"]=d["ex"]/d["coin"].map(sdv)
    d["volrank"]=d.groupby("coin")["sd30"].rank(pct=True)
    d["agit"]=(d["volrank"]>0.5).astype(int)
    d["trend"]=np.where(d["r60"]>0.1,"rising",np.where(d["r60"]<-0.1,"falling","choppy"))
    d.loc[d["r60"].isna(),"trend"]="na"
    out={}
    def summ(gb):
        a=gb["ex"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a[["mean","count","t"]].round(4)
    dd=d.dropna(subset=["s14"]).copy()
    dd["s14q"]=pd.qcut(dd["s14"],8,labels=False)
    out["all: s14 octile -> 5d excess"]=summ(dd.groupby("s14q"))
    out["in profile vs out: s14 octile"]=summ(dd.groupby(["inprof","s14q"]))
    out["trend x s14 octile (agit proxy all)"]=summ(dd[dd.trend!="na"].groupby(["trend","s14q"]))
    out["agit proxy x s14 octile"]=summ(dd.groupby(["agit","s14q"]))
    # correlations by group
    def corr(x):
        x=x.dropna(subset=["s14","ex"])
        if len(x)<20: return pd.Series({"n":len(x),"r":np.nan,"t":np.nan})
        r=np.corrcoef(x["s14"],x["ex"])[0,1]; n=len(x)
        return pd.Series({"n":n,"r":r,"t":r*np.sqrt((n-2)/(1-r*r))})
    out["corr s14 vs ex by trend x agit"]=dd[dd.trend!="na"].groupby(["trend","agit"]).apply(corr).round(3)
    # 1-day move z
    dd["r1q"]=pd.qcut(dd["r1z"],8,labels=False,duplicates="drop")
    out["1d move z octile -> 5d ex"]=summ(dd.groupby("r1q"))
    dd["rngq"]=pd.qcut(dd["rng"],5,labels=False,duplicates="drop")
    out["range/sd30 quintile -> 5d ex"]=summ(dd.groupby("rngq"))
    dd["volq"]=pd.qcut(dd["volrank"],5,labels=False)
    out["vol rank quintile -> 5d ex"]=summ(dd.groupby("volq"))
    out["weekday -> 5d ex"]=summ(dd.groupby("wd"))
    out["year -> in profile mean ex & count"]=summ(dd[dd.inprof==1].groupby("yr"))
    dd["r60q"]=pd.qcut(dd["r60"],6,labels=False)
    out["60d return sextile -> 5d ex"]=summ(dd.dropna(subset=["r60"]).groupby("r60q"))
    # book: daily returns
    dl=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dl.append(x)
    D=pd.concat(dl)
    out["book by window: mean daily ret, coin ret"]=D.groupby("w")[["book_return","coin_return"]].mean().round(5)
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    T["fq"]=pd.qcut(T["entry_forecast"],4,labels=False,duplicates="drop")
    out["trades by entry forecast quartile"]=T.groupby("fq")[["net_profit_loss_percent","entry_forecast"]].agg(["mean","count"]).round(3)
    return out

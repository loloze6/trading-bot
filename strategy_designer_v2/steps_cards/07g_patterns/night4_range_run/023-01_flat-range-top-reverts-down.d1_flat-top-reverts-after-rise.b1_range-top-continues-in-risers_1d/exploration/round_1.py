def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            b["coin"]=coin; b["win"]=w
            b["pos"]=np.arange(len(b))
            b["fwd5"]=c.shift(-5)/c-1
            b["r1"]=c.pct_change()
            b["r5"]=c/c.shift(5)-1
            b["r20"]=c/c.shift(20)-1
            mx=c.rolling(30,min_periods=30).max(); mn=c.rolling(30,min_periods=30).min()
            b["rp"]=(c-mn)/(mx-mn)
            b["width"]=mx/mn-1
            b["vol"]=b["r1"].rolling(20,min_periods=15).std()
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","pos","fwd5","r1","r5","r20","rp","width","vol","year","regime","forecast","postRebalance_current_allocation"]])
    df=pd.concat(rows,ignore_index=True)
    g=df[(df["pos"]%5==0)&df["fwd5"].notna()].copy()
    g["m"]=g.groupby("coin")["fwd5"].transform("mean")
    g["dm"]=g["fwd5"]-g["m"]
    g["sv"]=g["dm"]/(g["vol"]*np.sqrt(5))
    def summ(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    def slope(d,xc,yc="dm"):
        d=d[[xc,yc]].dropna()
        if len(d)<20: return pd.Series({"n":len(d),"slope":np.nan,"t":np.nan})
        r=stats.linregress(d[xc],d[yc]); return pd.Series({"n":len(d),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    g["rpq"]=pd.cut(g["rp"],[-.01,.2,.4,.6,.8,1.01],labels=["q1","q2","q3","q4","q5"])
    out["rp quintile x regime"]=g.groupby(["regime","rpq"])["dm"].apply(summ).unstack()
    out["slope rp by regime"]=g.groupby("regime").apply(lambda d:slope(d,"rp"))
    out["slope rp trending by coin"]=g[g.regime=="trending"].groupby("coin").apply(lambda d:slope(d,"rp"))
    out["slope rp trending by year"]=g[g.regime=="trending"].groupby("year").apply(lambda d:slope(d,"rp"))
    g["volq"]=g.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    g["widq"]=g.groupby("coin")["width"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["slope rp by regime x vol tercile"]=g.groupby(["regime","volq"]).apply(lambda d:slope(d,"rp"))
    out["slope rp by regime x width tercile"]=g.groupby(["regime","widq"]).apply(lambda d:slope(d,"rp"))
    g["z1"]=g["r1"]/g["vol"]; g["z5"]=g["r5"]/(g["vol"]*np.sqrt(5)); g["z20"]=g["r20"]/(g["vol"]*np.sqrt(20))
    out["slope z1 by regime"]=g.groupby("regime").apply(lambda d:slope(d,"z1"))
    out["slope z5 by regime"]=g.groupby("regime").apply(lambda d:slope(d,"z5"))
    out["slope z20 by regime"]=g.groupby("regime").apply(lambda d:slope(d,"z20"))
    out["slope vol (level) on dm by regime"]=g.groupby("regime").apply(lambda d:slope(d,"vol"))
    # days / book
    dl=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; dl.append(d)
    D=pd.concat(dl,ignore_index=True)
    D["wd"]=pd.to_datetime(D["day"]).dt.dayofweek
    out["book by weekday"]=D.groupby("wd")["book_return"].apply(summ).unstack()
    out["coin by weekday"]=D.groupby("wd")["coin_return"].apply(summ).unstack()
    bb=D.groupby(["win","day"])["book_return"].mean().dropna()
    out["book daily n/mean/sd/skew"]=pd.Series({"n":len(bb),"mean":bb.mean(),"sd":bb.std(),"skew":stats.skew(bb),"top5pct share of sum":bb[bb>=bb.quantile(.95)].sum()/bb.sum(),"bottom5pct share":bb[bb<=bb.quantile(.05)].sum()/bb.sum()})
    # trades
    tl=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; tl.append(t)
    T=pd.concat(tl,ignore_index=True)
    T["ef"]=pd.cut(T["entry_forecast"].abs(),[0,5,10,15,20.1])
    out["trades by |entry forecast|"]=T.groupby(["side","ef"])["net_profit_loss_percent"].apply(summ).unstack()
    T["days"]=T["duration_minutes"]/1440
    T["dq"]=pd.cut(T["days"],[0,5.5,10,20,40,1000])
    out["trades by duration"]=T.groupby("dq")["net_profit_loss_percent"].apply(summ).unstack()
    return out

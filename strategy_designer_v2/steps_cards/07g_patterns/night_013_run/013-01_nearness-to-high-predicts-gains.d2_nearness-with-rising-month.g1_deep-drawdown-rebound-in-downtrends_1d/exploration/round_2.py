def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    # weekday robustness on daily coin returns
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy();d["coin"]=coin;d["w"]=w;dd.append(d)
    D=pd.concat(dd).dropna(subset=["coin_return"])
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["y"]=pd.to_datetime(D["day"]).dt.year
    D["sat"]=(D.wd==5)
    def wt(x):
        a=x.loc[x.sat,"coin_return"];b=x.loc[~x.sat,"coin_return"]
        return pd.Series({"sat":a.mean(),"other":b.mean(),"t":stats.ttest_ind(a,b,equal_var=False).statistic,"n_sat":len(a)})
    out["sat vs other by coin"]=D.groupby("coin").apply(wt)
    out["sat vs other by year"]=D.groupby("y").apply(wt)
    # market-day level (avg across coins) to remove cross-coin correlation
    M=D.groupby(["day","w"]).agg(r=("coin_return","mean"),wd=("wd","first")).reset_index()
    mt=M.groupby("wd")["r"].agg(["mean","count","std"]);mt["t"]=mt["mean"]/(mt["std"]/np.sqrt(mt["count"]))
    out["weekday avg-of-coins days"]=mt
    # sat return vs prior 7-day return (graded?)
    # ret30 momentum per coin / per year on 7-bar grid
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float);v=b["volume"].astype(float);n=len(c)
            ret30=c/c.shift(30)-1;ret14=c/c.shift(14)-1;ret60=c/c.shift(60)-1
            vrel=v/v.rolling(20).mean()
            fwd7=c.shift(-7)/c-1
            y=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0,n,7):
                if i+7>=n: break
                rows.append(dict(coin=coin,w=w,y=y[i],ret30=ret30[i],ret14=ret14[i],ret60=ret60[i],vrel=vrel[i],fwd7=fwd7[i]))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd7"]-g.groupby("coin")["fwd7"].transform("mean")
    def sl(d,col):
        d=d.dropna(subset=[col,"ex"])
        if len(d)<20: return pd.Series({"slope":np.nan,"t":np.nan,"n":len(d)})
        r=stats.linregress(d[col],d["ex"])
        return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(d)})
    out["ret30 slope by coin"]=g.groupby("coin").apply(lambda d:sl(d,"ret30"))
    out["ret30 slope by year"]=g.groupby("y").apply(lambda d:sl(d,"ret30"))
    out["ret14 slope"]=sl(g,"ret14")
    out["ret60 slope"]=sl(g,"ret60")
    g["lvrel"]=np.log(g["vrel"])
    out["log vrel slope"]=sl(g,"lvrel")
    out["log vrel by coin"]=g.groupby("coin").apply(lambda d:sl(d,"lvrel"))
    # rank-based slope for ret30 to check outliers
    g2=g.dropna(subset=["ret30","ex"]).copy();g2["rk"]=g2.groupby("coin")["ret30"].rank(pct=True)
    out["ret30 rank slope"]=sl(g2,"rk")
    return out

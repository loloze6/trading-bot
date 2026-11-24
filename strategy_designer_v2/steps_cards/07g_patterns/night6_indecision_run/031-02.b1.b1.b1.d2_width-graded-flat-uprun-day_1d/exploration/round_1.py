def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b.timestamp)})
            d["flat"]=1-(c-o).abs()/rng.replace(0,np.nan)
            d["rise5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["width"]=rng/rng.rolling(20).mean()
            d["r1"]=c/c.shift(1)-1
            d["clv"]=(c-l)/rng.replace(0,np.nan)
            d["vol20"]=d.r1.rolling(20).std()
            d["fwd3"]=c.shift(-3)/c-1
            d["pos"]=np.arange(len(b))
            d["fc"]=b.forecast.values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%3==0)&D.fwd3.notna()].copy()
    G["norm"]=G.groupby("coin").fwd3.transform("mean")
    G["unu"]=G.fwd3-G.norm
    G["day"]=G.ts.dt.floor("D")
    G["volq"]=G.groupby("coin").vol20.transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    def stat(df):
        n=len(df)
        if n<5: return pd.Series({"n":n})
        s=df.groupby("day").unu.sum(); nd=len(s)
        m=df.unu.mean()
        se=np.sqrt((s-s.mean()*0).pow(2).sum()- (s.sum()**2)/nd)/np.sqrt(nd-1)*np.sqrt(nd)/n if nd>1 else np.nan
        # day-clustered se of mean
        dev=df.unu-m; sd=dev.groupby(df.day).sum()
        se=np.sqrt((sd**2).sum())/n
        return pd.Series({"n":n,"days":nd,"mean_unu":m,"t":m/se,"hit":(df.fwd3>0).mean()})
    out={}
    G["side"]=np.sign(G.rise5)
    G["wq"]=pd.cut(G.width,[0,0.7,1,1.4,2,99])
    flat=G[G.flat>=0.9]
    out["doji by run side x width"]=flat.groupby(["side","wq"]).apply(stat)
    G["clvq"]=pd.cut(G.clv,[-.01,.2,.4,.6,.8,1.01])
    wide=G[G.width>1.4]
    out["wide days by side x clv"]=wide.groupby(["side","clvq"]).apply(stat)
    G["r1q"]=G.groupby("coin").r1.transform(lambda s:pd.qcut(s,5,labels=False))
    out["by r1 quintile"]=G.groupby("r1q").apply(stat)
    G["r5q"]=G.groupby("coin").rise5.transform(lambda s:pd.qcut(s,5,labels=False))
    out["by rise5 quintile x volq"]=G.groupby(["volq","r5q"]).apply(stat)
    G["wd"]=G.ts.dt.weekday
    out["by weekday"]=G.groupby("wd").apply(stat)
    G["r20s"]=np.sign(G.r20)
    out["doji wide by r20 side x rise5 side"]=G[(G.flat>=0.9)&(G.width>1)].groupby(["r20s","side"]).apply(stat)
    return out

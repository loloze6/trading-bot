def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            rng=(h-l).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "loc":(c-l)/rng,"vsr":r/sd,"r1":r,"rng_sd":(rng/c)/sd,
                "body":(c-o)/rng,
                "inprof":(b["regime"]!="chop").astype(int),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year})
            for H in (2,5,10):
                df[f"f{H}"]=c.shift(-H)/c-1
            df["r5p"]=c/c.shift(5)-1
            df["r5p_sd"]=df["r5p"]/(sd*np.sqrt(5))
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    out={}
    def stat(g,col):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean() if n else np.nan,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    # drift per coin on 10-grid
    for H in (2,10):
        g=A[A.pos%H==0].copy()
        drift=g.groupby("coin")[f"f{H}"].mean()
        g["u"]=g[f"f{H}"]-g.coin.map(drift)
        g["locb"]=pd.cut(g["loc"],[0,0.2,0.4,0.6,0.8,1.0001],include_lowest=True)
        g["vsrb"]=pd.cut(g["vsr"],[-99,-2,-1,0,1,2,99])
        out[f"H{H} loc x prof"]=g.groupby(["inprof","locb"]).apply(lambda x:stat(x,"u")).round(3)
        out[f"H{H} vsr x prof"]=g.groupby(["inprof","vsrb"]).apply(lambda x:stat(x,"u")).round(3)
        g["r5b"]=pd.cut(g["r5p_sd"],[-99,-1.5,-0.5,0.5,1.5,99])
        out[f"H{H} past5 x prof"]=g.groupby(["inprof","r5b"]).apply(lambda x:stat(x,"u")).round(3)
    g=A[A.pos%10==0].copy(); drift=g.groupby("coin")["f10"].mean(); g["u"]=g["f10"]-g.coin.map(drift)
    gp=g[g.inprof==1]
    out["H10 inprof by year"]=gp.groupby("yr").apply(lambda x:stat(x,"u")).round(3)
    out["H10 inprof by coin"]=gp.groupby("coin").apply(lambda x:stat(x,"u")).round(3)
    out["share inprof"]=A.inprof.mean()
    g2=A[A.pos%2==0].copy(); d2=g2.groupby("coin")["f2"].mean(); g2["u"]=g2["f2"]-g2.coin.map(d2)
    out["H2 weekday inprof"]=g2[g2.inprof==1].groupby("wd").apply(lambda x:stat(x,"u")).round(3)
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D); D=D.dropna(subset=["book_return"])
    act=D[D.book_return.abs()>1e-9]
    out["book active days by coin"]=act.groupby("coin").book_return.agg(["count","mean","sum"]).round(5)
    out["book by window sum"]=D.groupby("w").book_return.sum().round(4)
    q=act.book_return.quantile([0.05,0.95])
    out["book tails: coin return on big gain/loss"]=pd.Series({"big gain mean coin ret":act[act.book_return>=q[0.95]].coin_return.mean(),
        "big loss mean coin ret":act[act.book_return<=q[0.05]].coin_return.mean(),
        "n each":int((act.book_return>=q[0.95]).sum())})
    return out

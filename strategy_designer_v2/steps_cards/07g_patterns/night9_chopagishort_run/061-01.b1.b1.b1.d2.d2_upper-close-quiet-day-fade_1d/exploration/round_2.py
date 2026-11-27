def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change(); sd=r.rolling(20,min_periods=20).std()
            rng=(h-l).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "loc":(c-l)/rng,"vsr":r/sd,
                "inprof":(b["regime"]!="chop").astype(int),
                "yr":pd.to_datetime(b["timestamp"]).dt.year})
            for H in (2,10): df[f"f{H}"]=c.shift(-H)/c-1
            df["r5_sd"]=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            df["r60"]=c/c.shift(60)-1
            df["vol30"]=r.rolling(30).std(); df["vol30_rel"]=df["vol30"]/r.rolling(90,min_periods=60).std()
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["trend"]=np.where(A.r60>0.10,"rising",np.where(A.r60<-0.10,"falling",np.where(A.r60.notna(),"choppy",None)))
    A["agit"]=np.where(A.vol30_rel>1,"agit",np.where(A.vol30_rel.notna(),"calm",None))
    out={}
    def stat(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean() if n else np.nan,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    for H in (2,10):
        g=A[A.pos%H==0].copy(); dr=g.groupby("coin")[f"f{H}"].mean(); g["u"]=g[f"f{H}"]-g.coin.map(dr)
        g["r5b"]=pd.cut(g["r5_sd"],[-99,-1.5,-0.5,0.5,1.5,99])
        out[f"H{H} r5b overall"]=g.groupby("r5b")["u"].apply(stat).unstack().round(3)
        out[f"H{H} r5b x trend"]=g.groupby(["trend","r5b"])["u"].apply(stat).unstack().round(3)
        out[f"H{H} r5b x agit"]=g.groupby(["agit","r5b"])["u"].apply(stat).unstack().round(3)
        # correlation slope of u on r5_sd, by window sign
        def slope(x):
            x=x.dropna(subset=["u","r5_sd"]); 
            if len(x)<10: return np.nan
            return np.corrcoef(x.r5_sd,x.u)[0,1]
        sw=g.groupby("w").apply(slope)
        out[f"H{H} corr u~r5 by window"]=sw.round(3)
        out[f"H{H} corr u~r5 pooled"]=float(slope(g))
        g["locb"]=pd.cut(g["loc"],[0,0.5,0.8,1.0001],include_lowest=True)
        out[f"H{H} loc x trend x agit (no inprof)"]=g[g.inprof==0].groupby(["trend","agit","locb"])["u"].apply(stat).unstack().round(3)
    return out

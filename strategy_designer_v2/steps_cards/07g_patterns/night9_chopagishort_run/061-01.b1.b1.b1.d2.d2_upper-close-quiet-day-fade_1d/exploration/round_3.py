def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change(); sd=r.rolling(20,min_periods=20).std()
            rng=(h-l).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),
                "loc":(c-l)/rng,"vsr":r/sd,"inprof":(b["regime"]!="chop").astype(int),"yr":ts.dt.year})
            for H in (2,3,5,10): df[f"f{H}"]=c.shift(-H)/c-1
            df["r5_sd"]=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            df["r3_sd"]=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            df["r60"]=c/c.shift(60)-1
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["trend"]=np.where(A.r60>0.10,"rising",np.where(A.r60<-0.10,"falling",np.where(A.r60.notna(),"choppy",None)))
    out={}
    def cstat(g):
        g=g.dropna(subset=["u"]); n=len(g)
        if n<3: return pd.Series({"n":n,"days":np.nan,"mean%":np.nan,"t_day":np.nan})
        m=g.u.mean(); s=(g.u-m).groupby(g.day).sum(); G=len(s)
        se=np.sqrt(G/(G-1)*(s**2).sum())/n if G>1 else np.nan
        return pd.Series({"n":n,"days":G,"mean%":100*m,"t_day":m/se})
    for H in (2,3,5):
        g=A[A.pos%H==0].copy(); dr=g.groupby("coin")[f"f{H}"].mean(); g["u"]=g[f"f{H}"]-g.coin.map(dr)
        g["r5b"]=pd.cut(g["r5_sd"],[-99,-2,-1.5,-1,-0.5,0,0.5,1,1.5,99])
        sub=g[g.trend.isin(["choppy","falling"])]
        out[f"H{H} choppy+falling r5b fine"]=sub.groupby("r5b").apply(cstat).round(3)
        mod=sub[(sub.r5_sd>-1.5)&(sub.r5_sd<=-0.5)]
        out[f"H{H} mod fall chop+fall by window"]=mod.groupby("w").apply(cstat).round(3)
        out[f"H{H} mod fall chop+fall by coin"]=mod.groupby("coin").apply(cstat).round(3)
    g=A[A.pos%10==0].copy(); dr=g.groupby("coin")["f10"].mean(); g["u"]=g["f10"]-g.coin.map(dr)
    big=g[g.r5_sd>1.5]
    out["H10 big rise by window"]=big.groupby("w").apply(cstat).round(3)
    g=A[A.pos%2==0].copy(); dr=g.groupby("coin")["f2"].mean(); g["u"]=g["f2"]-g.coin.map(dr)
    ca=g[g.inprof==1].copy(); ca["locb"]=pd.cut(ca["loc"],[0,0.5,0.8,1.0001],include_lowest=True)
    out["H2 inprof loc"]=ca.groupby("locb").apply(cstat).round(3)
    return out

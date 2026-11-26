def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    rows=[]
    # coin drift per 5 bars over all windows (non-overlapping grid)
    for coin in bars:
        for w,df in bars[coin].items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            sma=c.rolling(20).mean()
            dist=(c/sma-1)*100
            r1=c.pct_change()*100
            r5p=(c/c.shift(5)-1)*100
            r20p=(c/c.shift(20)-1)*100
            vol20=r1.rolling(20).std()
            fwd5=(c.shift(-5)/c-1)*100
            fwd1=(c.shift(-1)/c-1)*100
            rng=(df["high"]-df["low"])/df["close"]*100
            clpos=(df["close"]-df["low"])/(df["high"]-df["low"]).replace(0,np.nan)
            ts=pd.to_datetime(df["timestamp"])
            for i in range(0,len(df),5):
                rows.append(dict(coin=coin,w=w,reg=df["regime"].iloc[i],dist=dist.iloc[i],r1=r1.iloc[i],r5p=r5p.iloc[i],
                                 r20p=r20p.iloc[i],vol20=vol20.iloc[i],rng=rng.iloc[i],clpos=clpos.iloc[i],
                                 fwd5=fwd5.iloc[i],fwd1=fwd1.iloc[i],wd=ts.iloc[i].weekday(),yr=ts.iloc[i].year,
                                 fc=df["forecast"].iloc[i]))
    G=pd.DataFrame(rows)
    G["drift"]=G.groupby("coin")["fwd5"].transform("mean")
    G["ex5"]=G["fwd5"]-G["drift"]
    G=G.dropna(subset=["ex5"])
    out={}
    out["regime counts"]=G.groupby("reg")["ex5"].agg(["count","mean"])
    def qtab(col,sub,q=5):
        s=sub.dropna(subset=[col]).copy()
        s["q"]=pd.qcut(s[col],q,labels=False,duplicates="drop")
        t=s.groupby("q").agg(n=("ex5","size"),lo=(col,"min"),hi=(col,"max"),mean_ex5=("ex5","mean"),sd=("ex5","std"))
        t["t"]=t.mean_ex5/(t.sd/np.sqrt(t.n))
        return t.drop(columns="sd")
    def reg(col,sub):
        s=sub.dropna(subset=[col,"ex5"])
        r=stats.linregress(s[col],s["ex5"]); return f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(s)}"
    ra=G[G.reg=="unknown"]; ot=G[G.reg!="unknown"]
    for col in ["dist","r1","r5p","r20p","vol20","rng","clpos"]:
        out[f"reg {col} RA"]=reg(col,ra); out[f"reg {col} other"]=reg(col,ot)
    out["dist q RA"]=qtab("dist",ra); out["dist q other"]=qtab("dist",ot)
    out["r20p q all"]=qtab("r20p",G); out["vol20 q all"]=qtab("vol20",G)
    out["r1 q all"]=qtab("r1",G); out["clpos q all"]=qtab("clpos",G)
    out["weekday"]=G.groupby("wd")["ex5"].agg(["count","mean"])
    out["by window RA"]=ra.groupby("w")["ex5"].agg(["count","mean"])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]
    for coin in bars:
        for w,df in bars[coin].items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r20p=(c/c.shift(20)-1)*100
            r60p=(c/c.shift(60)-1)*100
            r10p=(c/c.shift(10)-1)*100
            vol20=(c.pct_change()*100).rolling(20).std()
            fwd5=(c.shift(-5)/c-1)*100
            fwd10=(c.shift(-10)/c-1)*100
            clpos=(df["close"]-df["low"])/(df["high"]-df["low"]).replace(0,np.nan)
            for i in range(0,len(df),5):
                rows.append(dict(coin=coin,w=w,reg=df["regime"].iloc[i],r20p=r20p.iloc[i],r60p=r60p.iloc[i],
                                 r10p=r10p.iloc[i],vol20=vol20.iloc[i],fwd5=fwd5.iloc[i],clpos=clpos.iloc[i],
                                 z20=r20p.iloc[i]/(vol20.iloc[i]*np.sqrt(20)) if vol20.iloc[i]>0 else np.nan))
    G=pd.DataFrame(rows)
    G["drift"]=G.groupby("coin")["fwd5"].transform("mean")
    G["ex5"]=G["fwd5"]-G["drift"]
    G=G.dropna(subset=["ex5"])
    G["trend"]=np.where(G.r60p>10,"rising",np.where(G.r60p< -10,"falling",np.where(G.r60p.notna(),"choppy","na")))
    out={}
    def reg(col,s):
        s=s.dropna(subset=[col,"ex5"])
        if len(s)<20: return "n<20"
        r=stats.linregress(s[col],s["ex5"]); return f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(s)}"
    for col in ["r20p","z20","r10p","clpos"]:
        out[f"{col} all"]=reg(col,G)
        for tr in ["rising","choppy","falling"]:
            out[f"{col} {tr}"]=reg(col,G[G.trend==tr])
    # per window sign of r20p slope
    ws=[]
    for w,s in G.dropna(subset=["z20"]).groupby("w"):
        if len(s)>15:
            r=stats.linregress(s["z20"],s["ex5"]); ws.append(dict(w=w,n=len(s),slope=r.slope,t=r.slope/r.stderr))
    out["z20 slope by window"]=pd.DataFrame(ws).set_index("w")
    cs=[]
    for c_,s in G.dropna(subset=["z20"]).groupby("coin"):
        r=stats.linregress(s["z20"],s["ex5"]); cs.append(dict(coin=c_,n=len(s),slope=r.slope,t=r.slope/r.stderr))
    out["z20 slope by coin"]=pd.DataFrame(cs).set_index("coin")
    s=G.dropna(subset=["z20"]).copy(); s["q"]=pd.qcut(s.z20,5,labels=False)
    t=s.groupby("q").agg(n=("ex5","size"),lo=("z20","min"),hi=("z20","max"),m=("ex5","mean"),sd=("ex5","std")); t["t"]=t.m/(t.sd/np.sqrt(t.n))
    out["z20 q all"]=t.drop(columns="sd")
    f=s[s.trend=="falling"].copy()
    if len(f)>50:
        f["q"]=pd.qcut(f.z20,4,labels=False)
        t=f.groupby("q").agg(n=("ex5","size"),lo=("z20","min"),hi=("z20","max"),m=("ex5","mean"),sd=("ex5","std")); t["t"]=t.m/(t.sd/np.sqrt(t.n))
        out["z20 q falling"]=t.drop(columns="sd")
    # weekday daily coin returns
    D=pd.concat([d.assign(coin=c_) for c_ in days for d in days[c_].values()])
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["cr"]=D["coin_return"]*100
    t=D.groupby("wd")["cr"].agg(["count","mean","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["weekday daily coin ret"]=t.drop(columns="std")
    # book: book daily return vs coin return
    B=D.dropna(subset=["book_return"])
    out["book mean daily %"]=float(B.book_return.mean()*100)
    out["book corr with coin"]=float(B[["book_return","coin_return"]].corr().iloc[0,1])
    return out

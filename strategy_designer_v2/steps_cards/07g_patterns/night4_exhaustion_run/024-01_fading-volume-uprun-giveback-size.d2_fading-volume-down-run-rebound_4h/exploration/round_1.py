def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; hb=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            d=df[["timestamp","close","volume","high","low"]].copy().reset_index(drop=True)
            c=d.close; r=c.pct_change()
            d["r"]=r
            d["usual"]=r.abs().rolling(180,min_periods=45).mean()
            d["fwd"]=c.shift(-H)/c-1
            d["past6"]=(c/c.shift(6)-1)/(d.usual*np.sqrt(6))
            d["past18"]=(c/c.shift(18)-1)/(d.usual*np.sqrt(18))
            d["past180"]=(c/c.shift(180)-1)
            d["volz"]=np.log(d.volume.replace(0,np.nan)).sub(np.log(d.volume.replace(0,np.nan)).rolling(180,min_periods=45).mean())
            d["vol_ratio"]=r.abs().rolling(18).mean()/d.usual
            d["rng"]=((d.high-d.low)/c)/((d.high-d.low)/c).rolling(180,min_periods=45).mean()
            s=np.sign(r).fillna(0).values; L=np.zeros(len(d)); cum=np.zeros(len(d))
            for i in range(1,len(d)):
                if s[i]!=0 and s[i]==s[i-1]: L[i]=L[i-1]+s[i]; cum[i]=cum[i-1]+r.iloc[i]
                else: L[i]=s[i]; cum[i]=r.iloc[i] if not np.isnan(r.iloc[i]) else 0
            d["streak"]=L; d["streakz"]=cum/d.usual
            d["hour"]=pd.to_datetime(d.timestamp).dt.hour
            d["wd"]=pd.to_datetime(d.timestamp).dt.weekday
            d["year"]=pd.to_datetime(d.timestamp).dt.year
            d["next"]=r.shift(-1)
            d["coin"]=coin; d["w"]=w
            hb.append(d[["coin","hour","wd","next","r","volz"]])
            g.append(d.iloc[::H])
        g=pd.concat(g); g["drift"]=g.fwd.mean(); g["sd"]=g.fwd.std()
        rows.append(g)
    G=pd.concat(rows).dropna(subset=["fwd"]); G["u"]=(G.fwd-G.drift)
    G["us"]=G.u/G.sd
    def tab(col,q=5):
        x=G.dropna(subset=[col]).copy(); x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        a=x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("u","size"),mean_u=("u","mean"),sd=("u","std"),str=("us","mean"))
        a["t"]=a.mean_u/(a.sd/np.sqrt(a.n)); return a.drop(columns="sd").round(4)
    out={}
    for col in ["past6","past18","past180","volz","vol_ratio","rng","streakz"]:
        out["fwd18 by "+col]=tab(col)
    x=G.copy(); x["sl"]=x.streak.clip(-5,5)
    a=x.groupby("sl").agg(n=("u","size"),mean_u=("u","mean"),sd=("u","std")); a["t"]=a.mean_u/(a.sd/np.sqrt(a.n)); out["fwd18 by streak len"]=a.drop(columns="sd").round(4)
    a=G.groupby("year").agg(n=("u","size"),mean_u=("u","mean"),sd=("u","std")); a["t"]=a.mean_u/(a.sd/np.sqrt(a.n)); out["fwd18 by year"]=a.drop(columns="sd").round(4)
    HB=pd.concat(hb).dropna(subset=["next"])
    for k in ["hour","wd"]:
        a=HB.groupby(k).agg(n=("next","size"),m=("next","mean"),sd=("next","std")); a["t"]=a.m/(a.sd/np.sqrt(a.n)); out["next bar by "+k]=a.drop(columns="sd").round(5)
    # next bar after large volume shock by sign of bar
    HB["sg"]=np.sign(HB.r); HB["vq"]=pd.qcut(HB.volz,5,labels=False)
    HB["signed_next"]=HB.next*HB.sg
    a=HB.groupby("vq").agg(n=("next","size"),m=("signed_next","mean"),sd=("signed_next","std")); a["t"]=a.m/(a.sd/np.sqrt(a.n)); out["next bar continuation by volz q"]=a.drop(columns="sd").round(5)
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            dd=df.copy(); dd["w"]=w; dd["coin"]=coin; D.append(dd)
    D=pd.concat(D); D["wd"]=pd.to_datetime(D.day).dt.weekday
    a=D.groupby("wd").agg(n=("book_return","count"),book=("book_return","mean"),coin=("coin_return","mean")); out["book by weekday"]=a.round(5)
    return out

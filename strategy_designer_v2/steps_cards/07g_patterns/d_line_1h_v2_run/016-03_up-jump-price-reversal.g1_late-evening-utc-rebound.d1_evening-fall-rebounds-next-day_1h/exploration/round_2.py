def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-24,24)
            g+=list(c[idx+24]/c[idx]-1)
        mu=np.mean(g)
        for w,df in ws.items():
            d=pd.DataFrame({"close":df["close"].values,"vol":df["volume"].values})
            ts=pd.to_datetime(df["timestamp"])
            d["hour"]=ts.dt.hour.values; d["wd"]=ts.dt.weekday.values; d["yr"]=ts.dt.year.values
            r1=d.close.pct_change()
            d["r24"]=d.close/d.close.shift(24)-1
            d["fwd"]=d.close.shift(-24)/d.close-1-mu
            d["r1n"]=d.close.shift(-1)/d.close-1
            sd=r1.rolling(24*30,min_periods=200).std()
            d["sd"]=sd
            d["z"]=d.r24/(sd*np.sqrt(24))
            ab=r1.abs()
            d["jump"]=ab.rolling(24).max()/ab.rolling(24).sum()
            d["vjump"]=d.vol.rolling(24).max()/d.vol.rolling(24).sum()
            d["volreg"]=sd/sd.rolling(24*90,min_periods=200).median()
            d["coin"]=coin; d["w"]=w; d["pos"]=np.arange(len(d))
            rows.append(d)
    B=pd.concat(rows)
    A=B.dropna(subset=["z","fwd","jump","vjump"])
    out={}
    def sl(s,x="z"):
        if len(s)<50: return pd.Series({"n":len(s),"bp":np.nan,"t":np.nan})
        r=stats.linregress(s[x],s.fwd); return pd.Series({"n":len(s),"bp":r.slope*1e4,"t":r.slope/r.stderr})
    H=A[A.hour==1]
    out["hour1 slope fwd~z by year"]=H.groupby("yr").apply(sl)
    out["hour1 slope by coin"]=H.groupby("coin").apply(sl)
    H19=A[A.hour==19]
    out["hour19 slope by year"]=H19.groupby("yr").apply(sl)
    # vjump interaction at hour1, per coin
    def inter(s):
        s=s.copy(); s["vjc"]=s.vjump-s.vjump.mean(); s["zv"]=s.z*s.vjc
        X=np.column_stack([np.ones(len(s)),s.z,s.vjc,s.zv]); y=s.fwd.values
        b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b; s2=e@e/(len(y)-4)
        se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.Series({"n":len(s),"t_z":b[1]/se[1],"t_zxvjump":b[3]/se[3]})
    G=A[A.pos%24==0]
    out["grid z*vjump by coin"]=G.groupby("coin").apply(inter)
    out["grid z*vjump by year"]=G.groupby("yr").apply(inter)
    G=G.copy(); G["vtq"]=pd.qcut(G.vjump,3,labels=False)
    out["grid slope by vjump tercile"]=G.groupby("vtq").apply(sl)
    G["vq"]=pd.qcut(G.volreg,3,labels=False)
    out["grid slope by volregime tercile"]=G.groupby("vq").apply(sl)
    out["grid slope by volregime x year (t)"]=G.groupby(["yr","vq"]).apply(sl)["t"].unstack()
    # hour 20-21 next hour return by year and coin
    B2=B.copy(); B2.loc[B2.w!=B2.w.shift(-1),"r1n"]=np.nan
    E=B2[B2.hour.isin([20,21])].dropna(subset=["r1n"])
    f=lambda s: pd.Series({"n":len(s),"bp":s.r1n.mean()*1e4,"t":s.r1n.mean()/(s.r1n.std()/np.sqrt(len(s)))})
    out["h20-21 next1h by year"]=E.groupby("yr").apply(f)
    out["h20-21 next1h by coin"]=E.groupby("coin").apply(f)
    # friday fwd24 by year
    F=A[(A.pos%24==0)]
    ff=lambda s: pd.Series({"n":len(s),"bp":s.fwd.mean()*1e4,"t":s.fwd.mean()/(s.fwd.std()/np.sqrt(len(s)))})
    out["fwd24 grid weekday x year t"]=F.groupby(["yr","wd"]).apply(ff)["t"].unstack()
    return out

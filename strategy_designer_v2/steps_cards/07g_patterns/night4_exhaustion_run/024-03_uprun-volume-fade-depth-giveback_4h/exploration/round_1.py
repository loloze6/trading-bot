def explore(data):
    import numpy as np, pandas as pd
    H=18
    rows=[]; bars_all=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); v=b["volume"].astype(float).replace(0,np.nan)
            r1=c.pct_change(); lr=np.log(c).diff()
            sgn=np.sign(lr).fillna(0)
            grp=(sgn!=sgn.shift()).cumsum()
            slen=sgn.groupby(grp).cumcount()+1
            slen=slen*sgn
            sgain=lr.groupby(grp).cumsum()
            usual=lr.abs().rolling(180,min_periods=45).mean()
            gz=sgain/usual
            # volume at streak start
            vstart=v.groupby(grp).transform('first')
            fade=np.log(vstart/v)
            r6p=c/c.shift(6)-1; r18p=c/c.shift(18)-1
            sd1=r1.rolling(180,min_periods=45).std()
            z6=r6p/(sd1*np.sqrt(6)); z18=r18p/(sd1*np.sqrt(18))
            volratio=r1.rolling(30,min_periods=15).std()/sd1
            vz=np.log(v/v.rolling(180,min_periods=45).median())
            f18=c.shift(-H)/c-1; f6=c.shift(-6)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame(dict(coin=coin,w=w,slen=slen,gz=gz,fade=fade,z6=z6,z18=z18,volratio=volratio,vz=vz,
                f18=f18,f6=f6,r1n=r1.shift(-1),hour=ts.dt.hour,wd=ts.dt.weekday,pos=np.arange(len(b)),
                fc=b["forecast"],alloc=b["postRebalance_current_allocation"]))
            bars_all.append(d)
    A=pd.concat(bars_all,ignore_index=True)
    G=A[A.pos%H==0].dropna(subset=["f18"]).copy()
    st=G.groupby("coin")["f18"].agg(["mean","std"])
    G["ex"]=(G.f18-G.coin.map(st["mean"]))/G.coin.map(st["std"])
    def tab(g,key):
        o=G.dropna(subset=[key]).groupby(g)["ex"].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); return o[["mean","t","count"]].round(4)
    out={}
    G["slb"]=G.slen.clip(-6,6)
    out["streak_len_signed->ex18 (strength units)"]=tab("slb","slen")
    G["gzq"]=pd.qcut(G.gz,10,labels=False,duplicates="drop"); out["streak gain deciles->ex18"]=tab("gzq","gz")
    up=G[(G.slen>=3)].copy(); up["fadeq"]=np.sign(up.fade)
    o=up.groupby("fadeq")["ex"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); out["up streak>=3 by fade sign"]=o.round(4)
    dn=G[(G.slen<=-3)].copy(); dn["fadeq"]=np.sign(dn.fade)
    o=dn.groupby("fadeq")["ex"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); out["down streak>=3 by fade sign"]=o.round(4)
    for k in ["z6","z18","volratio","vz"]:
        G[k+"q"]=pd.qcut(G[k],10,labels=False,duplicates="drop"); out[k+" deciles->ex18"]=tab(k+"q",k)
    # abs future move by volratio
    G["absex"]=G.f18.abs()/G.coin.map(st["std"])
    out["volratio decile -> abs f18 (units)"]=G.groupby("volratioq")["absex"].mean().round(3)
    # hour and weekday on next-bar return (all bars, overlap fine at 1 bar)
    A["r1z"]=A.r1n/A.groupby("coin")["r1n"].transform("std")
    for k in ["hour","wd"]:
        o=A.dropna(subset=["r1z"]).groupby(k)["r1z"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); out[k+"->next bar ret z"]=o.round(4)
    # book gain by bar
    A["gain"]=A.alloc*A.r1n
    o=A.dropna(subset=["gain"]).groupby(np.sign(A.alloc))["gain"].agg(["mean","count","sum"]); out["bar gain by position sign"]=o
    return out

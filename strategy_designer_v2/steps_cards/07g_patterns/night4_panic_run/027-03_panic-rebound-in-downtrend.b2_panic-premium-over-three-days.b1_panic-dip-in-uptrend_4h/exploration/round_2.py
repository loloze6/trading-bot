def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); rg=(b["high"]-b["low"])/c
            rr=rg.rolling(6).mean()/rg.rolling(180).mean()
            r6=c/c.shift(6)-1
            z6=r6/r6.abs().rolling(180).mean()
            prior=c.shift(6)/c.shift(186)-1
            ts=pd.to_datetime(b["timestamp"])
            f1=c.shift(-1)/c-1
            r1=c/c.shift(1)-1
            rv=r1.abs().rolling(180).mean()
            rows.append(pd.DataFrame({"coin":coin,"w":w,"rr":rr,"z6":z6,"prior":prior,
                "f18":c.shift(-18)/c-1,"f1":f1,"r1s":r1/rv,"r6":r6,"pos":b.index,"h":ts.dt.hour,
                "yr":ts.dt.year,"wd":ts.dt.dayofweek,"rv":rv}))
    A=pd.concat(rows,ignore_index=True)
    g=A[A.pos%18==0].dropna(subset=["f18"])
    A["x18"]=A.f18-A.coin.map(g.groupby("coin").f18.mean())
    A["x1"]=A.f1-A.coin.map(A.groupby("coin").f1.mean())
    def summ(d,col):
        d=d.dropna(subset=[col]); n=len(d); m=d[col].mean(); s=d[col].std()
        return pd.Series({"n":n,"mean":m,"t":m/(s/np.sqrt(n)) if n>1 else np.nan})
    out={}
    G=A[A.pos%18==0].copy()
    F=G[(G.z6<0)].copy()
    F["rrb"]=pd.cut(F.rr,[0,1,1.5,99]); F["zb"]=pd.cut(F.z6,[-99,-2,-1,0])
    out["fall_rr_x_z"]=F.groupby(["rrb","zb"]).apply(lambda d:summ(d,"x18"))
    S=F[F.rr>1.5]
    out["fallrr15_by_coin"]=S.groupby("coin").apply(lambda d:summ(d,"x18"))
    out["fallrr15_by_year"]=S.groupby("yr").apply(lambda d:summ(d,"x18"))
    S2=S.copy(); S2["pu"]=S2.prior>0
    out["fallrr15_by_prior"]=S2.groupby("pu").apply(lambda d:summ(d,"x18"))
    # hour effect: bar 20-24 UTC (f1 at h=16) and 00-04 (f1 at h=20)
    for h,nm in [(16,"bar20to24"),(20,"bar00to04")]:
        Hh=A[A.h==h].copy()
        out[nm+"_by_coin"]=Hh.groupby("coin").apply(lambda d:summ(d,"x1"))
        out[nm+"_by_year"]=Hh.groupby("yr").apply(lambda d:summ(d,"x1"))
        Hh["q"]=Hh.groupby("coin").r6.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
        out[nm+"_by_24h_ret_quint"]=Hh.groupby("q").apply(lambda d:summ(d,"x1"))
    return out

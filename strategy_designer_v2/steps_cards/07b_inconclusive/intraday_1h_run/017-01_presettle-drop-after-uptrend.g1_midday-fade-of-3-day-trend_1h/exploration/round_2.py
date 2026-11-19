def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            c=df["close"].values
            allr.append(c[1:]/c[:-1]-1)
        cmean=np.concatenate(allr).mean()
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            ts=pd.to_datetime(df["timestamp"],utc=True)
            c=df["close"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"year":ts.dt.year,
                            "ret72":c/c.shift(72)-1,
                            "r1x":c.shift(-1)/c-1-cmean,
                            "r3x":c.shift(-3)/c-1-3*cmean,
                            "r4x":c.shift(-4)/c-1-4*cmean,
                            "r6x":c.shift(-6)/c-1-6*cmean,
                            "r24x":c.shift(-24)/c-1-24*cmean})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    H=D[D.hour==11].copy()
    for h in ["r1x","r3x","r4x","r6x","r24x"]:
        out[f"fade_from12_{h}"]=tt(-np.sign(H.ret72)*H[h])
    H=H.dropna(subset=["ret72","r4x"])
    H["z"]=-H.ret72*H.r4x
    H["f4"]=-np.sign(H.ret72)*H.r4x
    H["q"]=pd.qcut(H.ret72,10,labels=False)
    out["from12_4h_by_ret72_decile"]=H.groupby("q").agg(n=("r4x","size"),mean_ret72=("ret72","mean"),mean_r4x=("r4x","mean"))
    out["from12_4h_fade_by_coin"]=H.groupby("coin")["f4"].apply(tt).unstack()
    out["from12_4h_fade_by_year"]=H.groupby("year")["f4"].apply(tt).unstack()
    H["side"]=np.where(H.ret72>0,"after_rise","after_fall")
    out["from12_4h_fade_by_side"]=H.groupby("side")["f4"].apply(tt).unstack()
    out["from12_4h_corr_spearman"]=H[["ret72","r4x"]].corr(method="spearman").iloc[0,1]
    # same 4h fade from other start hours (bar hour b -> clock b+1)
    res={}
    for b in range(24):
        G=D[D.hour==b]
        res[b+1]=tt(-np.sign(G.ret72)*G.r4x)
    out["fade4h_by_start_clock"]=pd.DataFrame(res).T
    return out

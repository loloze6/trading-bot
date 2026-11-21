def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[]; blk=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            a=b["postRebalance_current_allocation"].fillna(0).values
            r1n=np.r_[c[1:]/c[:-1]-1,np.nan]
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            vol=pd.Series(r1).rolling(168,min_periods=42).std().values
            volq=pd.Series(vol).rolling(720,min_periods=168).rank(pct=True).values
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            ret7d=np.r_[np.full(168,np.nan),c[168:]/c[:-168]-1]
            # bar-level book gross and fee by vol tercile
            for j in range(len(c)-1):
                pass
            df=pd.DataFrame(dict(g=a*r1n,fee=fee,vq=volq,t7=np.abs(ret7d)))
            df["coin"]=coin
            rows.append(df)
            # daily-held version: alloc fixed at f/10 sampled at grid, held 24 bars
            idx=np.arange(0,len(c)-24,24)
            fs=f[idx]/10
            fr=c[idx+24]/c[idx]-1
            turn=np.abs(np.diff(np.r_[0,fs]))
            blk.append(pd.DataFrame(dict(g=fs*fr,turn=turn,vq=volq[idx],coin=coin)))
    R=pd.concat(rows).dropna()
    R["vt"]=pd.cut(R["vq"],[0,1/3,2/3,1],labels=["lowvol","midvol","hivol"])
    out["bar book per day by vol tercile"]=R.groupby("vt")[["g","fee"]].mean()*24
    R["t7t"]=pd.qcut(R["t7"],3,labels=["weak7","mid7","strong7"])
    out["bar book per day by |7d|"]=R.groupby("t7t")[["g","fee"]].mean()*24
    B=pd.concat(blk).dropna()
    s=pd.Series(dict(gross_per_day=B["g"].mean(),turn_per_day=B["turn"].mean(),
                     fee_at_0.001=B["turn"].mean()*0.001 if False else B["turn"].mean()*0.001,
                     t=B["g"].mean()/B["g"].std()*np.sqrt(len(B)),n=len(B)))
    out["daily-held f/10"]=s
    B["vt"]=pd.cut(B["vq"],[0,1/3,2/3,1],labels=["lowvol","midvol","hivol"])
    out["daily-held by vol"]=B.groupby("vt")["g"].agg(["mean","count"])
    return out

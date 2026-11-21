def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book gain split by long/short position, gross, on bars
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            cl=b["close"].values.astype(float)
            fr=np.append(cl[1:]/cl[:-1]-1,np.nan)
            a=b["postRebalance_current_allocation"].values.astype(float)
            chg=np.abs(np.diff(np.append(b["previous_allocation"].values[:1].astype(float),a)))
            rows.append(pd.DataFrame(dict(coin=c,g=a*fr,side=np.sign(a),turn=np.abs(a-b["previous_allocation"].values.astype(float)))))
    B=pd.concat(rows)
    out["gross_by_side"]=B.groupby("side").agg(n=("g","size"),gain_per_bar=("g","mean"),turn_per_bar=("turn","mean"))
    out["turnover_per_day_per_coin"]=B["turn"].mean()*24
    out["gross_per_bar_all"]=B["g"].mean()
    # grid cases: z24 sign x vol ratio
    recs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            cl=b["close"].values.astype(float); n=len(cl)
            s=pd.Series(np.diff(np.log(cl),prepend=np.nan))
            vol=s.rolling(168,min_periods=84).std(); volL=s.rolling(720,min_periods=360).std()
            for i in range(168,n-24,24):
                z=(cl[i]/cl[i-24]-1)/(vol.iloc[i]*np.sqrt(24))
                f24=cl[i+24]/cl[i]-1
                f72=cl[i+72]/cl[i]-1 if i+72<n else np.nan
                recs.append(dict(coin=c,w=int(w[1:]),z=z,vr=vol.iloc[i]/volL.iloc[i] if volL.iloc[i]>0 else np.nan,f24=f24,f72=f72))
    df=pd.DataFrame(recs)
    for H in ("f24","f72"):
        df[H]=df[H]-df.groupby("coin")[H].transform("mean")
    df=df.dropna(subset=["z","vr"])
    df["zb"]=pd.qcut(df["z"],10,labels=False)
    df["vb"]=pd.qcut(df["vr"],4,labels=False)
    def agg(x):
        v=x["f24"]; v2=x["f72"].dropna()
        return pd.Series(dict(n=len(v),m24=v.mean(),t24=v.mean()/v.std()*np.sqrt(len(v)),m72=v2.mean(),t72=v2.mean()/v2.std()*np.sqrt(len(v2))))
    out["zdecile_extremes_by_vol"]=df[df.zb.isin([0,1,8,9])].groupby(["zb","vb"]).apply(agg)
    # graded: among falls in high vol state, z size
    hv=df[(df.vb==3)&(df.z<0)].copy()
    hv["q"]=pd.qcut(hv["z"],5,labels=False)
    out["falls_highvol_graded"]=hv.groupby("q").apply(agg)
    # window consistency for bottom decile
    bd=df[df.zb==0].copy(); bd["wg"]=(bd.w-1)//6
    out["bottom_decile_by_window_group"]=bd.groupby("wg").apply(agg)
    bdv=df[(df.zb<=1)&(df.vb==3)].copy(); bdv["wg"]=(bdv.w-1)//6
    out["falls_highvol_by_window_group"]=bdv.groupby("wg").apply(agg)
    return out

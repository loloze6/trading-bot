def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                            "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                            "prof":(b["regime"]=="unknown"),"r":r,"z":z,"fc":b["forecast"].astype(float)})
            for h in [1,2,3,5]:
                d[f"f{h}"]=c.shift(-h)/c-1
            d["f2_1"]=c.shift(-2)/c.shift(-1)-1
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    drift=D.groupby("coin")["f1"].mean()
    D["x1"]=D["f1"]-D["coin"].map(drift)
    P=D[D.prof & D.z.notna() & D.f1.notna()].copy()
    out["n_profile_bars"]=len(P)
    out["profile_mean_next_day_all"]=P["x1"].mean()
    P["zq"]=pd.qcut(P["z"],6,labels=False)
    g=P.groupby("zq").agg(n=("x1","size"),zmean=("z","mean"),x1=("x1","mean"),
        f2_1=("f2_1","mean"),f3=("f3","mean"),f5=("f5","mean"))
    g["t1"]=P.groupby("zq")["x1"].apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))
    out["by_z_sextile_all_profile"]=g
    U=P[P.z>0]
    out["up_by_coin"]=U.groupby("coin").agg(n=("x1","size"),x1=("x1","mean"),
        corr_z=("x1",lambda s: np.corrcoef(s,U.loc[s.index,"z"])[0,1]))
    out["up_by_year"]=U.groupby("year").agg(n=("x1","size"),x1=("x1","mean"))
    out["up_by_window"]=U.groupby("w").agg(n=("x1","size"),x1=("x1","mean"))
    S=P[P.fc<0]
    out["short_bars_n"]=len(S)
    out["short_fc_quart"]=S.assign(q=pd.qcut(S.fc.abs(),4,labels=False)).groupby("q").agg(
        n=("x1","size"),z=("z","mean"),x1=("x1","mean"),f3=("f3","mean"))
    # outside profile up days for comparison
    O=D[~D.prof & D.z.notna() & D.f1.notna()].copy()
    O["zq"]=pd.qcut(O["z"],6,labels=False)
    out["outside_profile_by_z"]=O.groupby("zq").agg(n=("x1","size"),z=("z","mean"),x1=("x1","mean"))
    # lagged effects: z of 2-day and 3-day rise
    for k in [2,3,5]:
        pass
    return out

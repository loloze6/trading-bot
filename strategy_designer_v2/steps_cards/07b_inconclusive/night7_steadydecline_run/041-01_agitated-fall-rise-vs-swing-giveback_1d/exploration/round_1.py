def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].astype(float).reset_index(drop=True)
            allr.append((c/c.shift(1)-1).dropna())
        drift=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c/c.shift(1)-1
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            f3=c.shift(-3)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year":pd.to_datetime(b["timestamp"]).dt.year,"prof":b["regime"]=="unknown",
                "z":z,"r":r,"x1":f1-drift,"x2":f2-2*drift,"x3":f3-3*drift,"fc":b["forecast"],"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","x1"])
    out={}
    def summ(g,col="x1"):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    P=D[D.prof]
    up=P[P.z>0].copy()
    up["q"]=pd.qcut(up.z,5,labels=False)
    out["prof_up_by_zquint"]=up.groupby("q").apply(summ)
    out["prof_up_zmean_by_q"]=up.groupby("q").z.mean()
    dn=P[P.z<0].copy(); dn["q"]=pd.qcut(dn.z,5,labels=False)
    out["prof_down_by_zquint"]=dn.groupby("q").apply(summ)
    out["prof_up_by_coin"]=up.groupby("coin").apply(summ)
    out["prof_up_by_window"]=up.groupby("w").apply(summ)
    out["prof_up_by_year"]=up.groupby("year").apply(summ)
    # horizons on grid
    for h in [2,3]:
        g=up[up.pos%h==0]
        out[f"prof_up_h{h}"]=summ(g,f"x{h}")
    # outside profile
    O=D[~D.prof]; ou=O[O.z>0].copy(); ou["q"]=pd.qcut(ou.z,5,labels=False)
    out["nonprof_up_by_zquint"]=ou.groupby("q").apply(summ)
    # all up days vs down days in profile, and flat/down day next
    out["prof_all_by_sign"]=P.assign(s=np.sign(P.z)).groupby("s").apply(summ)
    # slope tests
    sl=stats.linregress(up.z,up.x1); out["prof_up_slope"]=f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(up)}"
    sl=stats.linregress(P.z,P.x1); out["prof_all_slope"]=f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(P)}"
    return out

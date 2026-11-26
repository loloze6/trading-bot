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
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year":pd.to_datetime(b["timestamp"]).dt.year,"prof":b["regime"]=="unknown",
                "z":z,"x1":f1-drift,"x2":f2-2*drift,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","x1"])
    out={}
    def summ(g,col="x1"):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean%":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    def clslope(g,x,y):
        g=g.dropna(subset=[x,y])
        X=g[x].values; Y=g[y].values
        Xc=X-X.mean(); b=(Xc*(Y-Y.mean())).sum()/(Xc**2).sum()
        e=Y-Y.mean()-b*Xc
        s=pd.Series(Xc*e).groupby(g["day"].values).sum()
        se=np.sqrt((s**2).sum())/(Xc**2).sum()
        return f"slope {b:.5f} t_cl {b/se:.2f} n {len(g)} days {g['day'].nunique()}"
    P=D[D.prof]; dn=P[P.z<0].copy()
    out["prof_down_slope_cl"]=clslope(dn.assign(a=-dn.z),"a","x1")
    out["prof_up_slope_cl"]=clslope(P[P.z>0],"z","x1")
    out["prof_all_slope_cl"]=clslope(P,"z","x1")
    out["prof_down_by_coin"]=dn.groupby("coin").apply(summ)
    out["prof_down_by_year"]=dn.groupby("year").apply(summ)
    out["prof_down_by_window"]=dn.groupby("w").apply(summ)
    out["prof_down_h2"]=summ(dn[dn.pos%2==0],"x2")
    out["prof_all_days"]=summ(P)
    O=D[~D.prof]; od=O[O.z<0].copy(); od["q"]=pd.qcut(od.z,5,labels=False)
    out["nonprof_down_by_zquint"]=od.groupby("q").apply(summ)
    out["nonprof_down_slope_cl"]=clslope(od.assign(a=-od.z),"a","x1")
    return out

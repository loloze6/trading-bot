def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r1=b["close"].shift(-1)/b["close"]-1
            allr.append(r1.dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            rng=(b["high"]-b["low"])
            loc=(c-b["low"])/rng.replace(0,np.nan)
            mr=rng.rolling(20).mean()
            wid=rng/mr
            atr=(rng/c)
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fc":b["forecast"],"reg":b["regime"],"loc":loc,"wid":wid,
                "ex1":c.shift(-1)/c-1-mu,"ex2":(c.shift(-2)/c-1)-2*mu,"ex3":(c.shift(-3)/c-1)-3*mu,
                "dayret":c/c.shift(1)-1,"pos":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows)
    D["inprof"]=D["reg"]!="chop"
    def ct(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna()
        g=x.groupby("d")["v"].sum()
        n=len(x); m=x["v"].mean()
        se=np.sqrt((g**2).sum() - 0)/n if n>0 else np.nan
        # clustered: sum of (dev) per day
        dev=x["v"]-m; gd=dev.groupby(x["d"]).sum()
        se=np.sqrt((gd**2).sum())/n
        return pd.Series({"n":n,"days":x["d"].nunique(),"mean":m,"t":m/se if se>0 else np.nan})
    out={}
    A=D[D.fc>0]
    out["cases_h1h2h3"]=pd.DataFrame({h:ct(A[h],A["day"]) for h in ["ex1","ex2","ex3"]})
    out["by_coin"]=A.groupby("coin").apply(lambda g: ct(g["ex1"],g["day"]))
    out["by_year"]=A.groupby("year").apply(lambda g: ct(g["ex1"],g["day"]))
    A=A.copy()
    A["fq"]=pd.qcut(A["fc"].rank(method="first"),4,labels=False)
    out["by_fc_quart"]=A.groupby("fq").apply(lambda g: pd.concat([ct(g["ex1"],g["day"]),pd.Series({"fc":g.fc.mean(),"loc":g["loc"].mean()})]))
    A["wq"]=pd.qcut(A["wid"].rank(method="first"),3,labels=False)
    out["by_width_terc"]=A.groupby("wq").apply(lambda g: pd.concat([ct(g["ex1"],g["day"]),pd.Series({"wid":g.wid.mean()})]))
    A["down"]=A["dayret"]<0
    out["by_dayret_sign"]=A.groupby("down").apply(lambda g: ct(g["ex1"],g["day"]))
    P=D[D.inprof & (D.wid>=1)].copy()
    P["lb"]=pd.cut(P["loc"],[0,0.2,0.4,0.6,0.8,1.0001],include_lowest=True)
    out["profile_wide_by_loc_h1"]=P.groupby("lb").apply(lambda g: ct(g["ex1"],g["day"]))
    P2=D[D.inprof].copy()
    P2["lb"]=pd.cut(P2["loc"],[0,0.2,0.4,0.6,0.8,1.0001],include_lowest=True)
    out["profile_all_by_loc_h1"]=P2.groupby("lb").apply(lambda g: ct(g["ex1"],g["day"]))
    Q=D[(~D.inprof)&(D.wid>=1)&(D["loc"]<0.2)]
    out["outside_profile_wide_low_h1"]=ct(Q["ex1"],Q["day"])
    out["inprof_share"]=D["inprof"].mean()
    return out

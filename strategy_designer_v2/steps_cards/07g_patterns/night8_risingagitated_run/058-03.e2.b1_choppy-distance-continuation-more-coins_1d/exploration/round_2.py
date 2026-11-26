def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    def tt(x):
        x=pd.Series(x).dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    rows=[];drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            dist=c/c.rolling(20).mean()-1
            r1=c.pct_change()
            v30=r1.rolling(30).std()
            ret60=c/c.shift(60)-1
            fwd10=c.shift(-10)/c-1
            fwd1=c.shift(-1)/c-1
            fwd3=c.shift(-3)/c-1
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for i in range(n):
                drows.append(dict(coin=coin,w=w,i=i,r1=r1[i],v30=v30[i],ret60=ret60[i],fwd1=fwd1[i],fwd3=fwd3[i],
                    dist=dist[i],fwd10=fwd10[i],inprof=b["regime"][i]=="unknown",wd=ts[i].weekday(),
                    rng=rng[i],clpos=clpos[i],day=ts[i].normalize(),yr=ts[i].year))
    D=pd.DataFrame(drows)
    D["vrel"]=D["v30"]/D.groupby("coin")["v30"].transform("median")
    D["agit"]=D["vrel"]>1
    D["trend"]=np.where(D["ret60"]>0.1,"rise",np.where(D["ret60"]<-0.1,"fall","chop"))
    D.loc[D["ret60"].isna(),"trend"]=np.nan
    D["z"]=D["r1"]/D["v30"]
    # grid 10 for dist, raw fwd10 in profile
    G=D[D["i"]%10==0].dropna(subset=["dist","fwd10"]).copy()
    G["dq"]=G.groupby("coin")["dist"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["raw fwd10 by dist quintile, inprof"]=G[G.inprof].groupby("dq")["fwd10"].apply(tt).unstack()
    G["sx"]=np.sign(G["dist"])*(G["fwd10"]-G.groupby("coin")["fwd10"].transform("mean"))
    out["follow ex10 inprof by agit x side"]=G[G.inprof].groupby(["agit",G["dist"]>0])["sx"].apply(tt).unstack()
    # next 3 day return (grid 3) after large down z, by trend x agit
    H=D[D["i"]%3==0].dropna(subset=["z","fwd3","trend"]).copy()
    H["dr3"]=H["fwd3"]-H.groupby("coin")["fwd3"].transform("mean")
    H["zb"]=pd.cut(H["z"],[-99,-2,-1,0,1,2,99],labels=False)
    out["ex fwd3 by z bin, chop trend x agit"]=H[H.trend=="chop"].groupby(["agit","zb"])["dr3"].apply(tt).unstack()
    out["ex fwd3 by z bin, rise x agit"]=H[H.trend=="rise"].groupby(["agit","zb"])["dr3"].apply(tt).unstack()
    out["ex fwd3 by z bin, fall x agit"]=H[H.trend=="fall"].groupby(["agit","zb"])["dr3"].apply(tt).unstack()
    # big up day -> next days (short side idea), spearman z vs dr3 for z>0 by profile
    sp={}
    for (tr,ag),g in H[H.z>0].groupby(["trend","agit"]):
        if len(g)>30: r=stats.spearmanr(g["z"],g["dr3"]); sp[f"{tr}_{'ag' if ag else 'calm'}"]=pd.Series({"n":len(g),"rho":r[0],"p":r[1]})
    out["spearman up-z vs ex fwd3 by profile"]=pd.DataFrame(sp).T
    # weekday by trend
    out["coin ret by weekday x trend (mean)"]=D.dropna(subset=["trend","r1"]).pivot_table(index="wd",columns="trend",values="r1",aggfunc="mean")
    W=D.dropna(subset=["trend","r1"])
    out["fri+sat minus other t by trend"]=pd.DataFrame({tr:pd.Series(stats.ttest_ind(g[g.wd.isin([4,5])]["r1"],g[~g.wd.isin([4,5])]["r1"],equal_var=False)[:2],index=["t","p"]) for tr,g in W.groupby("trend")})
    # weekday by year robust
    out["fri+sat minus other by year"]=W.groupby("yr").apply(lambda g: g[g.wd.isin([4,5])]["r1"].mean()-g[~g.wd.isin([4,5])]["r1"].mean())
    # close position in range: low close next day
    C=D.dropna(subset=["clpos","fwd1","trend"]).copy()
    C["cq"]=pd.qcut(C["clpos"],5,labels=False)
    out["fwd1 by close-in-range quintile x trend"]=C.pivot_table(index="cq",columns="trend",values="fwd1",aggfunc="mean")
    return out

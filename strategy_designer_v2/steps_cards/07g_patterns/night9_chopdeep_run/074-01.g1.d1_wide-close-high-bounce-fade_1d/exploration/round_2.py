def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].astype(float); allr.append((c.shift(-1)/c-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c/c.shift(1)-1
            sd30=r.rolling(30).std()
            pct=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d=pd.DataFrame({
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r1":r,
                "width":(h-l)/(h-l).rolling(20).mean(),
                "loc":(c-l)/(h-l).replace(0,np.nan),
                "nxt":c.shift(-1)/c-1,
                "nxt2":c.shift(-2)/c.shift(-1)-1,
                "nxt3":c.shift(-3)/c.shift(-1)-1,
                "r60":c/c.shift(60)-1,
                "pct":pct,
                "inprof":(b["regime"]!="chop"),
            })
            d["ex"]=d["nxt"]-mu; d["ex2"]=d["nxt2"]-mu; d["ex3"]=d["nxt3"]-2*mu
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["r1","width","loc","nxt"])
    def st(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g),"days":0,"mean":np.nan,"t":np.nan})
        m=g[col].mean()
        dev=g.assign(dv=g[col]-m).groupby("day")["dv"].sum()
        D_=len(dev); se=np.sqrt((dev**2).sum()*D_/(D_-1))/len(g)
        return pd.Series({"n":len(g),"days":D_,"mean":m,"t":m/se})
    D["trend"]=np.where(D["r60"].isna(),"na",np.where(D["r60"]>0.1,"rising",np.where(D["r60"]<-0.1,"falling","choppy")))
    D["ag"]=np.where(D["pct"].isna(),"na",np.where(D["pct"]>0.5,"agit","calm"))
    D["prof"]=D["trend"]+"_"+D["ag"]
    D["wide"]=D.width>1; D["up"]=D.r1>0; D["hi"]=D["loc"]>0.5
    out={}
    out["wideup_hi_by_prof"]=D[D.up&D.hi&D.wide].groupby("prof").apply(st)
    out["widedown_lo_by_prof"]=D[~D.up&~D.hi&D.wide].groupby("prof").apply(st)
    out["wideup_lo_by_prof"]=D[D.up&~D.hi&D.wide].groupby("prof").apply(st)
    F=D[D.inprof&D.up&D.hi&D.wide].copy()
    F["fade"]=F["nxt"]<0
    out["inprof_wideuphi_day2_by_day1"]=F.groupby("fade").apply(lambda g:st(g,"ex2"))
    out["inprof_wideuphi_day2to3"]=st(F,"ex3").to_frame().T
    F["q"]=pd.qcut(F.width,3,labels=False)
    out["inprof_wideuphi_day2_by_width"]=F.groupby("q").apply(lambda g:st(g,"ex2"))
    # in profile, all days: day2 after a down next day
    G=D[D.inprof].copy()
    G["q"]=pd.qcut(G["loc"],5,labels=False)
    out["inprof_loc_quintile"]=G.groupby("q").apply(st)
    ca=D[D.prof=="choppy_agit"].copy()
    ca["q"]=pd.qcut(ca.r1,5,labels=False)
    out["choppy_agit_r1_quintile"]=ca.groupby("q").apply(st)
    out["prof_counts"]=D["prof"].value_counts()
    return out

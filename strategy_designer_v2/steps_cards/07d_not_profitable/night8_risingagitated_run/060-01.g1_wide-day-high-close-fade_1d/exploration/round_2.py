def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        allret=[]
        for w,b in wins.items():
            allret.append(pd.Series(b["close"].values).pct_change().dropna())
        drift=pd.concat(allret).mean()
        a2=[]
        for w,b in wins.items():
            c=pd.Series(b["close"].values); a2.append((c.shift(-2)/c-1).iloc[::2].dropna())
        drift2=pd.concat(a2).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            rng=(b["high"]-b["low"])
            cl=(c-b["low"])/rng.replace(0,np.nan)
            rr=rng/rng.rolling(20,min_periods=20).mean()
            lr=np.log(c).diff()
            r60=c/c.shift(60)-1
            v30=lr.rolling(30).std()
            vpct=v30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl,"rr":rr,
                "nxt":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"r1":c.pct_change(),
                "r60":r60,"vp":vpct,"inprof":b["regime"]!="chop",
                "pos":np.arange(len(b)),"alloc":b["postRebalance_current_allocation"],
                "ts":b["timestamp"].astype(str).str[:10]})
            d["su"]=-(d["nxt"]-drift); d["su2"]=-(d["n2"]-drift2)
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["nxt","rr","cl"])
    def stat(m,col="su"):
        x=D[m].dropna(subset=[col])
        if len(x)<3: return pd.Series({"n":len(x),"days":0,"mean":np.nan,"t_day":np.nan})
        g=x.groupby("ts")[col].sum(); n=len(g)
        return pd.Series({"n":len(x),"days":n,"mean":x[col].mean(),"t_day":g.mean()/(g.std(ddof=1)/np.sqrt(n))})
    sit=(D["cl"]>=0.6)&(D["rr"]>=1.0)
    fall=D["r60"]<-0.10; agit=D["vp"]>0.5; chop=D["r60"].abs()<=0.10; rise=D["r60"]>0.10
    o={}
    o["profiles"]=pd.DataFrame({
      "inprof(regime)":stat(sit&D["inprof"]),
      "falling agitated(recomp)":stat(sit&fall&agit),
      "falling any":stat(sit&fall),
      "falling calm":stat(sit&fall&~agit),
      "agitated any":stat(sit&agit),
      "choppy agitated":stat(sit&chop&agit),
      "rising agitated":stat(sit&rise&agit),
      "rising calm":stat(sit&rise&~agit),
      "choppy calm":stat(sit&chop&~agit)}).T.round(4)
    # 2-day horizon on even grid
    g2=D["pos"]%2==0
    o["h2"]=pd.DataFrame({"sit inprof h1":stat(sit&D["inprof"]),
       "sit inprof h2 grid":stat(sit&D["inprof"]&g2,"su2"),
       "sit falling h2 grid":stat(sit&fall&g2,"su2"),
       "inprof all h2 grid":stat(D["inprof"]&g2,"su2")}).T.round(4)
    # size of the up day: within situation in profile, by r1
    m=sit&D["inprof"]
    o["by_r1"]=D[m].groupby(pd.qcut(D.loc[m,"r1"],3))["su"].agg(["count","mean"]).round(4)
    # condition check: big up day without high close/wide range, in profile
    o["r1_alone"]=pd.DataFrame({"inprof r1 top tercile not sit":stat(D["inprof"]&(D["r1"]>D.loc[m,"r1"].quantile(0.67))&~sit),
                                "inprof sit by window count":pd.Series(dtype=float)}).T.round(4)
    o["sit_by_window"]=D[m].groupby("w")["su"].agg(["count","mean"]).round(4)
    o["sit_by_coin"]=D[m].groupby("coin")["su"].agg(["count","mean"]).round(4)
    o["sit_falling_by_window"]=D[sit&fall].groupby("w")["su"].agg(["count","mean"]).round(4)
    return o

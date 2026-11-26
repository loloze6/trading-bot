def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            s=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])/c/s
            loc=(b["high"]-c)/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.floor("D"),"yr":ts.dt.year,
                "inprof":(b["regime"]!="chop").astype(int),"rng":rng,"loc":loc,"rz":r/s,"s":s})
            for h in [1,2,3,5]:
                df["f%d"%h]=c.shift(-h)/c-1
            df["i"]=np.arange(len(df))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    # drift per coin per horizon on non-overlapping grid
    for h in [1,2,3,5]:
        g=d[d["i"]%h==0]
        dr=g.groupby("coin")["f%d"%h].mean()
        d["x%d"%h]=d["f%d"%h]-d["coin"].map(dr)
        d["u%d"%h]=d["x%d"%h]/(d["coin"].map(g.groupby("coin")["f%d"%h].std()))
    def tday(g,col):
        g=g.dropna(subset=[col])
        if len(g)<8: return pd.Series({"n":len(g),"mean%":np.nan,"t":np.nan,"days":g["day"].nunique()})
        dev=g[col]-g[col].mean(); sd=dev.groupby(g["day"]).sum()
        se=np.sqrt((sd**2).sum())/len(g)
        return pd.Series({"n":len(g),"mean%":100*g[col].mean(),"t":g[col].mean()/se,"days":g["day"].nunique()})
    out={}
    case=(d.inprof==1)&(d.rng>=2)&(d["loc"]>=0.667)
    hz=[]
    for h in [1,2,3,5]:
        g=d[case&(d["i"]%h==0)]
        s_=tday(g,"x%d"%h); s_["h"]=h
        s_["strength"]=g["u%d"%h].mean()
        gg=g.dropna(subset=["x%d"%h])
        s_["corr_rng*loc"]=np.corrcoef(gg["rng"]*gg["loc"],gg["x%d"%h])[0,1] if len(gg)>3 else np.nan
        hz.append(s_)
    out["case_by_horizon_grid"]=pd.DataFrame(hz)
    # graded: whole in-profile, score rng*loc, terciles, 3d grid
    g=d[(d.inprof==1)&(d["i"]%3==0)].copy()
    g["score"]=g["rng"]*g["loc"]
    g["sb"]=pd.qcut(g["score"],5,labels=False)
    out["inprof_score_quintile_3d"]=g.groupby("sb").apply(lambda x:tday(x,"x3"))
    o=d[(d.inprof==0)&(d["i"]%3==0)].copy(); o["score"]=o["rng"]*o["loc"]
    o["sb"]=pd.qcut(o["score"],5,labels=False)
    out["outprof_score_quintile_3d"]=o.groupby("sb").apply(lambda x:tday(x,"x3"))
    # dip by return z in profile, 3d grid
    g["zb"]=pd.cut(g["rz"],[-100,-2,-1,-0.5,0,1,100])
    out["inprof_rz_3d"]=g.groupby("zb",observed=True).apply(lambda x:tday(x,"x3"))
    # yearly consistency of case at 3d grid
    gc=d[case&(d["i"]%3==0)]
    out["case3d_by_year"]=gc.groupby("yr").apply(lambda x:tday(x,"x3"))
    out["case3d_by_coin"]=gc.groupby("coin").apply(lambda x:tday(x,"x3"))
    # low-close wide vs downday: does low close add beyond rz within in-profile wide days (3d)
    gw=g[g.rng>=2].copy()
    gw["neg"]=(gw.rz<0).astype(int)
    gw["lb"]=pd.cut(gw["loc"],[-0.01,0.333,0.667,1.01],labels=["hi","mid","lo"])
    out["inprof_wide_sign_loc_3d"]=gw.groupby(["neg","lb"],observed=True).apply(lambda x:tday(x,"x3"))
    return out

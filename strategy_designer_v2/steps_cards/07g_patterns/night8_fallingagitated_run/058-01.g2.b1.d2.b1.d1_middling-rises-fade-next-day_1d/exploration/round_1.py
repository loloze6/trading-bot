def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z1=r/sd
            r3=c/c.shift(3)-1
            z3=r3/(sd*np.sqrt(3))
            tr60=c/c.shift(60)-1
            f1=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z1":z1,"z3":z3,
                "f1":f1,"f3":f3,"inprof":(b["regime"]=="unknown").values,
                "tr60":tr60,"wd":ts.dt.weekday.values,"alloc":b["postRebalance_current_allocation"].astype(float),
                "day":ts.dt.floor("D").values,"rng":((b["high"]-b["low"])/c).values,
                "clpos":((c-b["low"])/(b["high"]-b["low"])).values})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift1=D["f1"].mean(); drift3=D.loc[D.pos%3==0,"f3"].mean()
    D["u1"]=D["f1"]-drift1; D["u3"]=D["f3"]-drift3
    def summ(g,col):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g),"mean":np.nan,"t_day":np.nan})
        s=g.groupby("day")[col].sum(); G=len(s)
        m=g[col].mean()
        se=np.sqrt((s-s.mean()*0+0).pow(2).sum()*0+((g.groupby("day")[col].apply(lambda x:(x-m).sum()))**2).sum()*G/(G-1))/len(g)
        return pd.Series({"n":len(g),"days":G,"mean":m,"t_day":m/se})
    out={}
    D["zb"]=pd.cut(D["z1"],[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["inprof_z1bin_next1"]=D[D.inprof].groupby("zb").apply(lambda g:summ(g,"u1"))
    out["outprof_z1bin_next1"]=D[~D.inprof].groupby("zb").apply(lambda g:summ(g,"u1"))
    G3=D[D.pos%3==0].copy()
    G3["z3b"]=pd.cut(G3["z3"],[-99,-1.5,-0.5,0,0.5,1.5,99])
    out["inprof_z3bin_next3"]=G3[G3.inprof].groupby("z3b").apply(lambda g:summ(g,"u3"))
    out["outprof_z3bin_next3"]=G3[~G3.inprof].groupby("z3b").apply(lambda g:summ(g,"u3"))
    D["trend"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    o=D[~D.inprof]
    out["outprof_trend_x_zsign_next1"]=o.groupby(["trend",np.sign(o["z1"])]).apply(lambda g:summ(g,"u1"))
    out["inprof_weekday_next1"]=D[D.inprof].groupby("wd").apply(lambda g:summ(g,"u1"))
    out["all_weekday_next1"]=D.groupby("wd").apply(lambda g:summ(g,"u1"))
    up=D[D.inprof&(D.z1>0)].copy()
    up["cb"]=pd.cut(up["clpos"],[0,0.33,0.66,1.0001],include_lowest=True)
    out["inprof_upday_closepos_next1"]=up.groupby("cb").apply(lambda g:summ(g,"u1"))
    Ds=D.copy(); Ds["rb"]=Ds.groupby(["coin","w"])["rng"].transform(lambda x:x/x.rolling(30,min_periods=20).median())
    Ds["rbb"]=pd.qcut(Ds["rb"],4)
    out["inprof_range_rel_next1"]=Ds[Ds.inprof].groupby("rbb").apply(lambda g:summ(g,"u1"))
    out["counts"]=pd.Series({"bars":len(D),"inprof":int(D.inprof.sum()),"drift1":drift1,"drift3":drift3})
    return out

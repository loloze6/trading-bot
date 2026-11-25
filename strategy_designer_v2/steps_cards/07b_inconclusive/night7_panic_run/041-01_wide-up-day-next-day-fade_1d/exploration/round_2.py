def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            std=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])/c
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"year":ts.dt.year,"day":ts.dt.floor("D"),
                "r":r,"z":rng/std,"zr":(r/std).abs(),"nxt":c.shift(-1)/c-1,"tr60":c/c.shift(60)-1,
                "nxt3":c.shift(-3)/c-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["nxt"].mean()
    D["dev"]=D["nxt"]-D["coin"].map(drift)
    D=D.dropna(subset=["dev","r","z"])
    def summ(g,sign):
        x=sign*g["dev"]; dd=x.groupby(g["day"]).sum()
        t=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>2 else np.nan
        return pd.Series({"n":len(g),"days":len(dd),"mean":x.mean(),"t":t})
    out={}
    dn=D[D.r<0].copy(); up=D[D.r>0].copy()
    dn["zq"]=pd.qcut(dn.z,5,labels=False); up["zq"]=pd.qcut(up.z,5,labels=False)
    dn["rq"]=pd.qcut(dn.zr,3,labels=False)
    out["dn_range_q_within_ret_tercile"]=dn.groupby(["rq",pd.qcut(dn.z,3,labels=False)]).apply(lambda x:summ(x,1))
    top=dn[dn.zq==4]
    out["dn_top_range_by_year"]=top.groupby("year").apply(lambda x:summ(x,1))
    out["dn_top_range_by_coin"]=top.groupby("coin").apply(lambda x:summ(x,1))
    out["dn_top_range_minus_bottom_t"]=pd.Series({"diff":top.dev.mean()-dn[dn.zq==0].dev.mean()})
    # graded slope: regress dev on z, per side
    for nm,g,s in [("up",up,-1),("dn",dn,1)]:
        y=s*g.dev; x=g.z
        b=np.cov(x,y)[0,1]/x.var()
        out[nm+"_slope_on_z"]=pd.Series({"slope":b,"corr":np.corrcoef(x,y)[0,1],"n":len(g)})
    up["tr"]=pd.cut(up.tr60,[-9,-.1,.1,99],labels=["fall","chop","rise"])
    nr=up[up.tr.isin(["fall","chop"])].copy(); nr["zq"]=pd.qcut(nr.z,3,labels=False)
    out["up_notrise_by_range_tercile"]=nr.groupby("zq").apply(lambda x:summ(x,-1))
    return out

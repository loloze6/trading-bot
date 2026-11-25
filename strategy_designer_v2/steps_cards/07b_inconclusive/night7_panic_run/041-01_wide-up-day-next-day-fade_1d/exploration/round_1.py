def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            std=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])/c
            d=pd.DataFrame({"coin":coin,"win":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"z":rng/std,"zr":r/std,"nxt":c.shift(-1)/c-1,
                "fc":b["forecast"],"clpos":(c-b["low"])/(b["high"]-b["low"]),
                "tr60":c/c.shift(60)-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["nxt"].mean()
    D["dev"]=D["nxt"]-D["coin"].map(drift)
    D=D.dropna(subset=["dev","r","z"])
    def summ(g,sign):
        x=sign*g["dev"]
        dd=x.groupby(g["day"]).sum()
        t=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>2 else np.nan
        return pd.Series({"n":len(g),"days":len(dd),"mean":x.mean(),"t":t})
    up=D[D.r>0].copy(); dn=D[D.r<0].copy()
    out={}
    out["up_all"]=summ(up,-1); out["dn_all(long)"]=summ(dn,1)
    out["up_fc"]=summ(up[up.fc<0],-1)
    for nm,g,s in [("up",up,-1),("dn",dn,1)]:
        g=g.copy()
        g["zq"]=pd.qcut(g.z,5,labels=False)
        out[nm+"_by_range_quint"]=g.groupby("zq").apply(lambda x:summ(x,s))
        g["rq"]=pd.qcut(g.zr.abs(),5,labels=False)
        out[nm+"_by_ret_quint"]=g.groupby("rq").apply(lambda x:summ(x,s))
        g["cq"]=pd.cut(g.clpos,[-.01,.33,.67,1.01],labels=False)
        out[nm+"_by_closepos"]=g.groupby("cq").apply(lambda x:summ(x,s))
        out[nm+"_by_coin"]=g.groupby("coin").apply(lambda x:summ(x,s))
        out[nm+"_by_year"]=g.groupby("year").apply(lambda x:summ(x,s))
        g["tr"]=pd.cut(g.tr60,[-9,-.1,.1,99],labels=["fall","chop","rise"])
        out[nm+"_by_trend"]=g.dropna(subset=["tr"]).groupby("tr").apply(lambda x:summ(x,s))
    up2=up[up.fc<0].copy(); up2["fq"]=pd.qcut(up2.fc.abs(),3,labels=False)
    out["up_by_fc_third"]=up2.groupby("fq").apply(lambda x:summ(x,-1))
    out["corr_fc_z"]=float(np.corrcoef(up2.fc.abs(),up2.z)[0,1])
    return out

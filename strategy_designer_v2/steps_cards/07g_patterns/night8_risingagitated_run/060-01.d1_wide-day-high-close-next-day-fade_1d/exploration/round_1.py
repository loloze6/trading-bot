def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"];o=b["open"]
            r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["clv"]=((c-l)/(h-l)).where(h>l)
            d["wide"]=((h-l)/c)/r.rolling(20).std()
            d["tr60"]=c.pct_change(60)*100
            d["tr20"]=c.pct_change(20)*100
            d["r1"]=r
            d["vol20"]=r.rolling(20).std()
            d["nxt"]=c.shift(-1)/c-1
            d["nxt3"]=c.shift(-3)/c-1
            d["regime"]=b["regime"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["wd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["nxt"].transform("mean")
    D["ex"]=D["nxt"]-mu
    D["exz"]=D["ex"]/D["vol20"]
    def agg(g,col="ex"):
        x=g[col].dropna()
        n=len(x)
        return pd.Series({"n":n,"mean%":x.mean()*100 if col=="ex" else x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["trend"]=pd.cut(D["tr60"],[-1e9,-10,10,1e9],labels=["fall","chop","rise"])
    D["clvq"]=pd.qcut(D["clv"],5,labels=False)
    D["wideb"]=pd.cut(D["wide"],[0,1,1.5,2,3,1e9])
    out["clvq_by_trend_exz"]=D.groupby(["trend","clvq"]).apply(agg,col="exz").unstack(0)
    out["wide_x_clvhalf_fall"]=D[D.trend=="fall"].assign(hi=D.clv>0.5).groupby(["wideb","hi"]).apply(agg).reset_index()
    out["wide_x_clvhalf_all"]=D.assign(hi=D.clv>0.5).groupby(["wideb","hi"]).apply(agg).reset_index()
    D["r1q"]=pd.qcut(D["r1"]/D["vol20"],5,labels=False)
    out["r1z_q_by_trend"]=D.groupby(["trend","r1q"]).apply(agg,col="exz").unstack(0)
    out["weekday"]=D.groupby("wd").apply(agg)
    out["vol_tercile"]=D.groupby(pd.qcut(D["vol20"].rank(pct=True),3,labels=False)).apply(agg)
    act=D[D.alloc.abs()>1e-6]
    out["active_by_year"]=act.groupby("year").apply(agg)
    out["active_by_clv_tercile"]=act.groupby(pd.qcut(act.clv,3,labels=False)).apply(agg)
    return out

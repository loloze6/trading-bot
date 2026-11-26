def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"]
            r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["clv"]=((c-l)/(h-l)).where(h>l)
            d["vol20"]=r.rolling(20).std()
            d["wide"]=((h-l)/c)/d["vol20"]
            d["tr60"]=c.pct_change(60)*100
            d["nxt"]=c.shift(-1)/c-1
            d["nxt2"]=c.shift(-2)/c-1
            d["regime"]=b["regime"].values
            d["wd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            d["day"]=d["ts"].dt.floor("D")
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    D["ex2"]=D["nxt2"]-D.groupby("coin")["nxt2"].transform("mean")
    def cl(g,col="ex"):
        g=g.dropna(subset=[col])
        n=len(g)
        if n<5: return pd.Series({"n":n,"days":np.nan,"mean%":np.nan,"t_day":np.nan})
        m=g[col].mean()
        s=(g[col]-m).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/n
        return pd.Series({"n":n,"days":len(s),"mean%":m*100,"t_day":m/se})
    D["trend"]=pd.cut(D["tr60"],[-1e9,-10,10,1e9],labels=["fall","chop","rise"])
    W=D[D.wide>=1.5].copy()
    W["clv3"]=pd.cut(W.clv,[-0.01,1/3,2/3,1.01],labels=["low","mid","high"])
    out={}
    out["wide15_trend_x_clv3"]=W.groupby(["trend","clv3"]).apply(cl).reset_index()
    out["wide15_all_clv3"]=W.groupby("clv3").apply(cl)
    out["wide15_all_clv3_2day"]=W.groupby("clv3").apply(cl,col="ex2")
    hi=W[W.clv3=="high"]; lo=W[W.clv3=="low"]
    out["wide15_high_by_window"]=hi.groupby("w").apply(cl)
    out["wide15_high_fall_by_year"]=hi[hi.trend=="fall"].groupby("year").apply(cl)
    out["wide15_high_by_coin"]=hi.groupby("coin").apply(cl)
    out["wide15_high_regime_notchop"]=hi.groupby(hi.regime!="chop").apply(cl)
    # graded: clv deciles slope within wide days, fall trend
    F=W[W.trend.isin(["fall","chop"])].dropna(subset=["clv","ex"])
    out["fallchop_wide_clv_slope"]=pd.Series({"corr":F.clv.corr(F.ex),"n":len(F)})
    hf=F[F.clv>0.5]
    out["fallchop_wide_hi_clv_corr"]=pd.Series({"corr":hf.clv.corr(hf.ex),"n":len(hf)})
    out["weekday_by_year_wed"]=D[D.wd==2].groupby("year").apply(cl)
    out["weekday_cl"]=D.groupby("wd").apply(cl)
    return out

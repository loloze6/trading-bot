def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            hh=h.rolling(20).max(); ll=l.rolling(20).min()
            rp=(2*(c-ll)/(hh-ll)-1)
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"rp":rp,
                             "r60":c/c.shift(60)-1,"v30":r1.rolling(30).std(),
                             "f5":c.shift(-5)/c-1,"f2":c.shift(-2)/c-1,"r1":r1,"r20":c/c.shift(20)-1,
                             "pos":np.arange(len(b))})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["day"]=A.ts.dt.floor("D"); A["year"]=A.ts.dt.year
    A["vrel"]=A.v30/A.groupby("coin").v30.transform("median")
    A["trend"]=pd.cut(A.r60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    A["agit"]=np.where(A.vrel>1,"agit","calm")
    def slope(x,col,y="ex5"):
        x=x.dropna(subset=[col,y])
        if len(x)<20: return pd.Series({"n":len(x),"slope":np.nan,"t":np.nan})
        X=np.c_[np.ones(len(x)),x[col].values]; Y=x[y].values
        bta=np.linalg.lstsq(X,Y,rcond=None)[0]; e=Y-X@bta
        XtXi=np.linalg.inv(X.T@X); meat=np.zeros((2,2))
        for _,ix in x.groupby("day").indices.items():
            s=(X[ix]*e[ix,None]).sum(0); meat+=np.outer(s,s)
        V=XtXi@meat@XtXi
        return pd.Series({"n":len(x),"slope%":100*bta[1],"t":bta[1]/np.sqrt(V[1,1])})
    out={}
    res=[]
    for off in range(5):
        g=A[(A.pos%5)==off].copy()
        g["ex5"]=g.f5-g.groupby("coin").f5.transform("mean")
        r=g.groupby(["trend","agit"],observed=True).apply(lambda x:slope(x,"rp"))
        r["off"]=off; res.append(r.reset_index())
    R=pd.concat(res)
    out["rp_slope_by_cell_offsets"]=R.groupby(["trend","agit"]).agg(n=("n","mean"),slope=("slope%","mean"),tmean=("t","mean"),tmin=("t","min"),tmax=("t","max")).round(2)
    g=A[(A.pos%5)==0].copy()
    g["ex5"]=g.f5-g.groupby("coin").f5.transform("mean")
    cc=g[(g.trend=="chop")&(g.agit=="calm")]
    out["chopcalm_slope_by_year"]=cc.groupby("year").apply(lambda x:slope(x,"rp")).round(2)
    fc=g[(g.trend=="fall")&(g.agit=="calm")]
    out["fallcalm_slope_by_year"]=fc.groupby("year").apply(lambda x:slope(x,"rp")).round(2)
    ca=g[(g.agit=="agit")]
    out["agit_slope_by_trend_r20"]=ca.groupby("trend",observed=True).apply(lambda x:slope(x,"r20")).round(2)
    out["calm_slope_by_trend_r20"]=g[g.agit=="calm"].groupby("trend",observed=True).apply(lambda x:slope(x,"r20")).round(2)
    # median-based robust: share of positive ex5 by rp quintile in chop calm (sign test)
    cc2=cc.dropna(subset=["ex5","rp"]).copy()
    cc2["q"]=pd.cut(cc2.rp,[-1.01,-0.6,-0.2,0.2,0.6,1.01])
    out["chopcalm_median_share"]=cc2.groupby("q",observed=True).ex5.agg(["count","median",lambda s:(s>0).mean()]).round(4)
    return out

def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["fwd"]=c.shift(-1)/c-1
            d["fwd2_3"]=c.shift(-3)/c.shift(-1)-1
            s20=r.rolling(20).std()
            d["rng"]=(b["high"]-b["low"])/c/s20
            hl=(b["high"]-b["low"]).replace(0,np.nan)
            d["low_near"]=(b["high"]-c)/hl
            d["z0"]=r/s20
            d["r60"]=c/c.shift(60)-1
            d["vol_rel"]=s20/r.rolling(60,min_periods=40).std()
            d["fc"]=b["forecast"]
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D["ex23"]=D["fwd2_3"]-D.groupby("coin")["fwd2_3"].transform("mean")
    D["day"]=D["ts"].dt.floor("D"); D["yr"]=D["ts"].dt.year
    def tday(sub,col="ex"):
        sub=sub.dropna(subset=[col])
        g=sub.groupby("day")[col].sum(); n=len(g)
        return pd.Series({"mean_bp":sub[col].mean()*1e4,"n":len(sub),"days":n,"t":g.mean()/(g.std()/np.sqrt(n)) if n>2 else np.nan})
    q=lambda col,k=5: D.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),k,labels=False))
    D["fq"]=q("fc"); D["zq"]=q("z0"); D["lq"]=q("low_near",3); D["rq"]=q("rng",3)
    out={}
    # horizon: days 2-3 after, non-overlapping grid of 3 on fwd2_3 approx
    g3=D[D["pos"]%3==0]
    out["fq_days2to3"]=g3.groupby("fq").apply(lambda s:tday(s,"ex23"))
    # z0 quintile x low_near tercile
    out["zq_x_lq_mean_bp"]=(D.dropna(subset=["ex","zq","lq"]).groupby(["zq","lq"])["ex"].mean().unstack()*1e4).round(1)
    out["zq_x_lq_t"]=D.dropna(subset=["ex","zq","lq"]).groupby(["zq","lq"]).apply(lambda s:tday(s)["t"]).unstack().round(2)
    out["zq_x_lq_n"]=D.dropna(subset=["ex","zq","lq"]).groupby(["zq","lq"]).size().unstack()
    # trend profile split of fc top vs bottom
    D["trend"]=np.where(D["r60"]>0.10,"rising",np.where(D["r60"]<-0.10,"falling",np.where(D["r60"].notna(),"choppy",None)))
    T=D.dropna(subset=["trend","ex","fq"])
    out["trend_fq_mean_bp"]=(T.groupby(["trend","fq"])["ex"].mean().unstack()*1e4).round(1)
    out["trend_fq_t"]=T.groupby(["trend","fq"]).apply(lambda s:tday(s)["t"]).unstack().round(2)
    D["agit"]=np.where(D["vol_rel"]>1,"agit",np.where(D["vol_rel"].notna(),"calm",None))
    A=D.dropna(subset=["agit","ex","fq"])
    out["agit_fq_mean_bp"]=(A.groupby(["agit","fq"])["ex"].mean().unstack()*1e4).round(1)
    out["agit_fq_t"]=A.groupby(["agit","fq"]).apply(lambda s:tday(s)["t"]).unstack().round(2)
    # by year top fifth minus bottom
    out["yr_top_fc"]=D[D["fq"]==4].groupby("yr").apply(tday)
    out["yr_bottom_z0"]=D[D["zq"]==0].groupby("yr").apply(tday)
    # joint regression ex ~ rng*low_near + z0 (standardised), day-clustered t
    J=D.dropna(subset=["ex","rng","low_near","z0"]).copy()
    J["prod"]=J["rng"]*J["low_near"]
    X=np.column_stack([np.ones(len(J)),(J["prod"]-J["prod"].mean())/J["prod"].std(),(J["z0"]-J["z0"].mean())/J["z0"].std()])
    y=J["ex"].values
    beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
    XtXi=np.linalg.inv(X.T@X)
    days=J["day"].values; S=np.zeros((3,3))
    for dd,idx in pd.Series(np.arange(len(J))).groupby(days):
        u=X[idx.values].T@e[idx.values]; S+=np.outer(u,u)
    se=np.sqrt(np.diag(XtXi@S@XtXi))
    out["joint_reg_bp_per_sd"]=pd.DataFrame({"beta_bp":beta*1e4,"t":beta/se},index=["const","rng_x_lownear","z0"])
    return out

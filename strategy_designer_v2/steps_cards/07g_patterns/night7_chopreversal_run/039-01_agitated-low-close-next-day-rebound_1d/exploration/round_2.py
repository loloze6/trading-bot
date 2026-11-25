def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            rng=(b.high-b.low)
            d["cl"]=((b.high-b.close)/rng).where(rng>0)
            d["r0"]=b.close/b.close.shift(1)-1
            d["r1"]=b.close.shift(-1)/b.close-1
            d["rngp"]=rng/b.close
            d["rngz"]=d.rngp/d.rngp.rolling(20,min_periods=10).mean().shift(1)
            d["agit"]=(b.regime!="chop").astype(int)
            d["pos"]=b.postRebalance_current_allocation
            d["coin"]=c; d["w"]=w; d["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            d["yr"]=pd.to_datetime(b.timestamp).dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["x1"]=D.r1-D.groupby("coin").r1.transform("mean")
    D["gain"]=D.pos*D.r1
    def clus(df,xcols,y="x1"):
        df=df.dropna(subset=xcols+[y])
        X=np.column_stack([np.ones(len(df))]+[df[c].values for c in xcols]); Y=df[y].values
        XtX=np.linalg.inv(X.T@X); b=XtX@X.T@Y; e=Y-X@b
        S=pd.DataFrame(X*e[:,None]).groupby(df["day"].values).sum().values
        G=S.shape[0]; V=XtX@(S.T@S)@XtX*G/(G-1)
        return pd.Series(np.r_[b,b/np.sqrt(np.diag(V)),len(df),G],index=["b0"]+["b_"+c for c in xcols]+["t0"]+["t_"+c for c in xcols]+["n","days"])
    D["clc"]=D.cl-0.5
    D["lrz"]=np.log(D.rngz)
    D["clxr"]=D.clc*D.lrz
    D["r0s"]=D.r0/D.rngp
    out={}
    out["reg_by_agit"]=pd.DataFrame({a:clus(D[D.agit==a],["clc","lrz","clxr"]) for a in [0,1]}).round(4)
    out["reg_cl_vs_r0_agit"]=pd.DataFrame({"cl_r0":clus(D[D.agit==1],["clc","r0"]),"r0only":clus(D[D.agit==1],["r0"])}).round(4)
    D["clw"]=D.clc*D.rngp
    out["clw_by_agit"]=pd.DataFrame({a:clus(D[D.agit==a],["clw"]) for a in [0,1]}).round(4)
    A=D[D.agit==1].copy()
    out["agit_wide_cl_by_year"]=A[A.rngz>A.rngz.quantile(2/3)].groupby("yr").apply(lambda g:pd.Series({"n":g[["cl","x1"]].dropna().shape[0],"corr":g.cl.corr(g.x1)})).round(3)
    out["agit_cl_by_year"]=A.groupby("yr").apply(lambda g:pd.Series({"n":g[["cl","x1"]].dropna().shape[0],"corr":g.cl.corr(g.x1)})).round(3)
    A["rzq"]=pd.qcut(A.rngz,3,labels=False)
    out["book_gain_by_rangewidth_agit"]=A.groupby("rzq").apply(lambda g:pd.Series({"n":g.gain.notna().sum(),"gain_bp":1e4*g.gain.mean(),"abs_pos":g.pos.abs().mean()})).round(3)
    return out

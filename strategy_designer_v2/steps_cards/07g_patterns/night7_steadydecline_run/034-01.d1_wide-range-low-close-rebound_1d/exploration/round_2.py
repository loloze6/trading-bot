def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            rng=(h-l); rr=rng/c
            r=c.pct_change()
            vol=r.shift(1).rolling(30,min_periods=15).std()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "clv":(c-l)/rng.replace(0,np.nan),"rw":rr/rr.shift(1).rolling(60,min_periods=20).mean(),
                "ret0":r,"z0":r/vol,"r1":c.shift(-1)/c-1,
                "agit":(b["regime"]=="mean_reversion"),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "pv":b["postRebalance_total_value"].astype(float)})
            d["bookr1"]=d["pv"].shift(-1)/d["pv"]-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["x1"]=D["r1"]-D["coin"].map(D.groupby("coin")["r1"].mean())
    D["day"]=D["ts"].dt.floor("D"); D["yr"]=D["ts"].dt.year
    def summ(x,col="x1"):
        x=x.dropna(subset=[col])
        if len(x)<15: return pd.Series({"n":len(x),"mean":np.nan,"t_day":np.nan})
        g=x.groupby("day")[col].mean()
        return pd.Series({"n":len(x),"days":len(g),"mean":x[col].mean(),"t_day":g.mean()/(g.std()/np.sqrt(len(g)))})
    out={}
    A=D[D.agit].copy()
    A["zq"]=pd.qcut(A["z0"],3,labels=False); A["cq"]=pd.qcut(A["clv"],3,labels=False)
    out["agit_z0terc_x_clvterc"]=A.groupby(["zq","cq"]).apply(summ).round(4)
    C=D[~D.agit].copy()
    C["zq"]=pd.qcut(C["z0"],3,labels=False); C["cq"]=pd.qcut(C["clv"],3,labels=False)
    out["calm_z0terc_x_clvterc"]=C.groupby(["zq","cq"]).apply(summ).round(4)
    # joint regression in agitated: x1 on clv, z0, rw (day-clustered)
    def reg(df,cols):
        x=df.dropna(subset=cols+["x1"])
        X=np.column_stack([np.ones(len(x))]+[(x[c]-x[c].mean())/x[c].std() for c in cols]); y=x["x1"].values
        bt=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@bt
        XtXi=np.linalg.inv(X.T@X); M=np.zeros((X.shape[1],)*2)
        for _,idx in x.groupby("day").indices.items():
            s=X[idx].T@e[idx]; M+=np.outer(s,s)
        V=XtXi@M@XtXi; return pd.DataFrame({"coef":bt,"t":bt/np.sqrt(np.diag(V))},index=["c"]+cols).round(5)
    out["reg_agit"]=reg(A,["clv","z0","rw"])
    out["reg_calm"]=reg(C,["clv","z0","rw"])
    A["lowc"]=A["clv"]<0.33
    out["agit_lowclv_by_year"]=A[A.lowc].groupby("yr").apply(summ).round(4)
    out["agit_highclv_by_year"]=A[A.clv>0.67].groupby("yr").apply(summ).round(4)
    out["agit_lowclv_by_coin"]=A[A.lowc].groupby("coin").apply(summ).round(4)
    # book's largest gain/loss bars: what preceded
    B=D.dropna(subset=["bookr1"]); B=B[B.alloc.abs()>0]
    q=B["bookr1"].quantile([0.05,0.95])
    out["book_extreme_context"]=pd.DataFrame({
        "worst5":B[B.bookr1<=q[0.05]][["clv","z0","rw","alloc"]].mean(),
        "best5":B[B.bookr1>=q[0.95]][["clv","z0","rw","alloc"]].mean(),
        "all_held":B[["clv","z0","rw","alloc"]].mean()}).round(3)
    # agitated up-days mid: ret0 moderate up followed by weakness, graded by z0
    A["zq5"]=pd.qcut(A["z0"],5,labels=False)
    out["agit_z0_quint"]=A.groupby("zq5").apply(summ).round(4)
    out["calm_z0_quint"]=C.assign(zq5=pd.qcut(C["z0"],5,labels=False)).groupby("zq5").apply(summ).round(4)
    return out

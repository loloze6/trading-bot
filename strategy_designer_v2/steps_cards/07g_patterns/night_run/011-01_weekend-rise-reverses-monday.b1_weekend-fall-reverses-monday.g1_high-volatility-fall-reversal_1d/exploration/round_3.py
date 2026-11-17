def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            d=b.copy()
            d["ts"]=pd.to_datetime(d["timestamp"])
            d["r"]=d["close"].pct_change()
            d["fwd"]=d["close"].shift(-1)/d["close"]-1
            d["vol20"]=d["r"].rolling(20).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["vrel"]=d["vol20"]/d["vol20"].rolling(40,min_periods=20).mean()
            d["volu"]=d["volume"]/d["volume"].rolling(20).mean().shift(1)
            d["wd"]=d["ts"].dt.dayofweek
            d["yr"]=d["ts"].dt.year
            d["coin"]=c; d["win"]=w
            rows.append(d[["coin","win","yr","wd","r","fwd","z","vrel","volu"]])
    A=pd.concat(rows,ignore_index=True)
    A["ex"]=A["fwd"]-A.groupby("coin")["fwd"].transform("mean")
    B=A.dropna(subset=["z","ex","vrel","volu"]).copy()
    B["zc"]=B["z"].clip(-5,5)
    out={}
    def slope(g,x="zc"):
        if len(g)<30: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        s=stats.linregress(g[x],g["ex"]); return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    B["grp"]=np.select([B["wd"].isin([5,6]),B["wd"]==0],["weekend","monday"],"tue_fri")
    out["slope_by_grp_coin"]=B.groupby(["grp","coin"]).apply(slope).unstack(0)
    out["slope_by_grp_year"]=B.groupby(["grp","yr"]).apply(slope).unstack(0)
    # weekend vs tue-thu slope difference: interaction regression
    C=B[B["wd"].isin([1,2,3,5,6])].copy()
    C["we"]=C["wd"].isin([5,6]).astype(float)
    X=np.column_stack([np.ones(len(C)),C["zc"],C["we"],C["zc"]*C["we"]])
    beta,res,_,_=np.linalg.lstsq(X,C["ex"].values,rcond=None)
    e=C["ex"].values-X@beta; s2=(e@e)/(len(C)-4)
    cov=s2*np.linalg.inv(X.T@X)
    out["weekend_minus_midweek_slope"]=pd.Series({"n":len(C),"diff":beta[3],"t":beta[3]/np.sqrt(cov[3,3])})
    # weekend slope graded by weekend volume
    W=B[B["wd"].isin([5,6])].copy()
    W["uq"]=pd.qcut(W["volu"],3,labels=["lowvol","mid","highvol"])
    out["weekend_slope_by_volume"]=W.groupby("uq").apply(slope)
    # down-day volume controlling for z
    D=B[B["r"]<0].copy()
    X=np.column_stack([np.ones(len(D)),D["zc"],np.log(D["volu"].clip(lower=0.05))])
    beta,_,_,_=np.linalg.lstsq(X,D["ex"].values,rcond=None)
    e=D["ex"].values-X@beta; s2=(e@e)/(len(D)-3); cov=s2*np.linalg.inv(X.T@X)
    out["down_reg_z_logvolu"]=pd.Series({"n":len(D),"b_z":beta[1],"t_z":beta[1]/np.sqrt(cov[1,1]),"b_logvolu":beta[2],"t_logvolu":beta[2]/np.sqrt(cov[2,2])})
    # low vrel down days continuation: graded by z?
    lo=B[(B["vrel"]<=B["vrel"].quantile(0.2))]
    out["lowvrel_slope_all"]=slope(lo)
    out["lowvrel_by_year_down"]=lo[lo["r"]<0].groupby("yr")["ex"].agg(["count","mean"])
    return out

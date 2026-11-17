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
            d["yr"]=d["ts"].dt.year
            d["coin"]=c; d["win"]=w
            rows.append(d[["coin","win","yr","r","fwd","z","vrel","volu"]])
    A=pd.concat(rows,ignore_index=True)
    A["ex"]=A["fwd"]-A.groupby("coin")["fwd"].transform("mean")
    B=A.dropna(subset=["z","ex","vrel","volu"]).copy()
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    vcut=B["vrel"].quantile(2/3)
    H=B[B["vrel"]>=vcut].copy()
    U=H[H["r"]>0].copy()
    U["zq"]=pd.qcut(U["z"],4,labels=False)
    out["highv_up_ex_by_z_quartile"]=U.groupby("zq").apply(summ)
    s=stats.linregress(U["z"].clip(upper=5),U["ex"])
    out["highv_up_slope"]=pd.Series({"n":len(U),"slope":s.slope,"t":s.slope/s.stderr,"rho":stats.spearmanr(U["z"],U["ex"])[0]})
    out["highv_up_by_coin"]=U.groupby("coin").apply(summ)
    out["highv_up_by_year"]=U.groupby("yr").apply(summ)
    # graded vrel for up days, all regimes
    Up=B[B["r"]>0].copy()
    Up["vq"]=pd.qcut(Up["vrel"],5,labels=False)
    out["up_ex_by_vrel_quintile"]=Up.groupby("vq").apply(summ)
    Dn=B[B["r"]<0].copy()
    Dn["vq"]=pd.qcut(Dn["vrel"],5,labels=False)
    out["down_ex_by_vrel_quintile"]=Dn.groupby("vq").apply(summ)
    # volume on down days, graded, and inside high vol
    Dn["uq"]=pd.qcut(Dn["volu"],5,labels=False)
    out["down_ex_by_volume_quintile"]=Dn.groupby("uq").apply(summ)
    HD=H[H["r"]<0].copy()
    HD["uq"]=pd.qcut(HD["volu"],3,labels=False)
    out["highv_down_ex_by_volume"]=HD.groupby("uq").apply(summ)
    # interaction: signed z * volu
    Dn["zv"]=-Dn["z"].clip(lower=-5)*Dn["volu"].clip(upper=5)
    s=stats.linregress(Dn["zv"],Dn["ex"])
    out["down_fall_x_volume_slope"]=pd.Series({"n":len(Dn),"slope":s.slope,"t":s.slope/s.stderr,"rho":stats.spearmanr(Dn["zv"],Dn["ex"])[0]})
    out["down_volume_by_year"]=Dn.groupby(["yr"]).apply(lambda g: pd.Series({"rho":stats.spearmanr(g["volu"],g["ex"])[0],"n":len(g)}))
    out["down_volume_by_coin"]=Dn.groupby(["coin"]).apply(lambda g: pd.Series({"rho":stats.spearmanr(g["volu"],g["ex"])[0],"n":len(g)}))
    # signed reversal in high vol: regress ex on -r (both sides)
    s=stats.linregress(-H["z"].clip(-5,5),H["ex"])
    out["highv_both_sides_slope"]=pd.Series({"n":len(H),"slope":s.slope,"t":s.slope/s.stderr})
    return out

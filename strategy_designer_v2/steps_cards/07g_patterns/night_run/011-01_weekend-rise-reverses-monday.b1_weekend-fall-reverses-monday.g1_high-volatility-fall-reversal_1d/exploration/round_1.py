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
            d["fwd2"]=d["close"].shift(-2)/d["close"]-1
            d["vol20"]=d["r"].rolling(20).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["vrel"]=d["vol20"]/d["vol20"].rolling(40,min_periods=20).mean()
            d["volu"]=d["volume"]/d["volume"].rolling(20).mean().shift(1)
            d["r2"]=d["close"].pct_change(2)
            d["wd"]=d["ts"].dt.dayofweek
            d["coin"]=c; d["win"]=w
            rows.append(d[["coin","win","wd","r","r2","fwd","fwd2","z","vrel","volu","forecast","regime","postRebalance_current_allocation"]])
    A=pd.concat(rows,ignore_index=True)
    A["ex"]=A["fwd"]-A.groupby("coin")["fwd"].transform("mean")
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    B=A.dropna(subset=["z","ex"])
    B["zq"]=pd.qcut(B["z"],7,labels=False)
    out["ex_by_z_septile"]=B.groupby("zq").apply(summ)
    B["vq"]=pd.qcut(B["vrel"],3,labels=["lowv","midv","highv"])
    B["dn"]=np.where(B["r"]<0,"down","up")
    out["ex_by_vrel_dir"]=B.groupby(["vq","dn"]).apply(summ)
    out["ex_by_weekday_of_signal"]=B.groupby("wd").apply(summ)
    # slope of ex on z by weekday
    sl=[]
    for wd,g in B.groupby("wd"):
        s=stats.linregress(g["z"].clip(-5,5),g["ex"]); sl.append([wd,len(g),s.slope,s.slope/s.stderr])
    out["slope_ex_on_z_by_wd"]=pd.DataFrame(sl,columns=["wd","n","slope","t"])
    # weekend: Sunday bar (wd 6) 2-day return -> Monday
    S=B[B["wd"]==6].dropna(subset=["r2"])
    s=stats.linregress(S["r2"],S["ex"])
    out["sunday_2d_ret_vs_monday_ex"]=pd.Series({"n":len(S),"slope":s.slope,"t":s.slope/s.stderr,"rho":stats.spearmanr(S["r2"],S["ex"])[0]})
    W=B[B["wd"].isin([1,2,3,4])].dropna(subset=["r2"])
    s=stats.linregress(W["r2"],W["ex"])
    out["weekday_2d_ret_vs_next_ex"]=pd.Series({"n":len(W),"slope":s.slope,"t":s.slope/s.stderr})
    # volume on down days
    D=B[B["r"]<0].dropna(subset=["volu"])
    D["uq"]=pd.qcut(D["volu"],3,labels=["lowvol","mid","highvol"])
    out["down_ex_by_volume"]=D.groupby("uq").apply(summ)
    U=B[B["r"]>0].dropna(subset=["volu"])
    U["uq"]=pd.qcut(U["volu"],3,labels=["lowvol","mid","highvol"])
    out["up_ex_by_volume"]=U.groupby("uq").apply(summ)
    F=B[B["forecast"]>0].copy()
    F["fq"]=pd.qcut(F["forecast"],4,labels=False)
    out["ex_by_forecast_q"]=F.groupby("fq").apply(summ)
    out["ex_by_coin_down_highv"]=B[(B["r"]<0)&(B["vq"]=="highv")].groupby("coin").apply(summ)
    # book
    dd=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            x=d.copy(); x["coin"]=c; x["wd"]=pd.to_datetime(x["day"]).dt.dayofweek; dd.append(x)
    Dd=pd.concat(dd)
    bk=Dd.groupby(["wd"])["book_return"].agg(["count","mean","std"])
    bk["t"]=bk["mean"]/(bk["std"]/np.sqrt(bk["count"]))
    out["book_ret_by_weekday"]=bk
    return out

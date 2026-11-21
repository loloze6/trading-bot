def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out={}
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float); op=b["open"].astype(float)
            r1=c.pct_change()
            rng=(hi-lo)/c
            df=pd.DataFrame({"coin":coin,"w":w,
                "f5":c.shift(-5)/c-1,"f10":c.shift(-10)/c-1,"f2":c.shift(-2)/c-1,
                "rng":rng,"rngrel":rng/rng.rolling(30,min_periods=15).mean(),
                "r1":r1,"body":(c-op)/op,
                "vol20":r1.rolling(20).std(),"fc":b["forecast"].astype(float),
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek})
            for H,col in [(5,"g5"),(10,"g10"),(2,"g2")]:
                df[col]=False
                df.loc[df.index[::H],col]=True
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    for H in ["f5","f10","f2"]:
        g=A[A["g"+H[1:]]]
        st=g.groupby("coin")[H].agg(["mean","std"])
        A[H+"_z"]=(A[H]-A["coin"].map(st["mean"]))/A["coin"].map(st["std"])
        A[H+"_ex"]=A[H]-A["coin"].map(st["mean"])
    A["rngrel_r"]=A.groupby("coin")["rngrel"].rank(pct=True)
    A["rng_r"]=A.groupby("coin")["rng"].rank(pct=True)
    A["vol_r"]=A.groupby("coin")["vol20"].rank(pct=True)
    A["fc_r"]=A.groupby("coin")["fc"].rank(pct=True)
    A["up"]=np.sign(A["body"])
    res={}
    for H in ["f2","f5","f10"]:
        g=A[A["g"+H[1:]]].dropna(subset=["rngrel_r",H+"_z","vol_r","fc_r"])
        X=np.column_stack([np.ones(len(g)),g["rngrel_r"],g["vol_r"],g["fc_r"]])
        y=g[H+"_z"].values
        beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
        e=y-X@beta; s2=e@e/(len(y)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        res[H]={"b_rngrel":beta[1],"t_rngrel":beta[1]/se[1],"b_vol":beta[2],"t_vol":beta[2]/se[2],"b_fc":beta[3],"t_fc":beta[3]/se[3],"n":len(g)}
    out["multireg_z"]=pd.DataFrame(res).T
    g=A[A["g5"]].dropna(subset=["rngrel_r","f5_ex"]).copy()
    g["q"]=pd.qcut(g["rngrel_r"],5,labels=False)
    def summ(d,col):
        a=d.groupby(["q","up"])[col].agg(["size","mean","median","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["size"])); return a.drop(columns="std")
    out["rngrel_q_by_daydir_5d"]=summ(g,"f5_ex")
    g["sq"]=g["f5_ex"].clip(g["f5_ex"].quantile(0.01),g["f5_ex"].quantile(0.99))
    a=g.groupby("q")["sq"].agg(["size","mean","median"]);out["rngrel_q_winsor_5d"]=a
    # per coin slope sign
    pc={}
    for coin,d in g.groupby("coin"):
        if len(d)>30:
            r=stats.linregress(d["rngrel_r"],d["f5_z"]); pc[coin]=(r.slope,r.slope/r.stderr,len(d))
    pc=pd.DataFrame(pc,index=["slope","t","n"]).T
    out["rngrel_per_coin"]=pc
    out["rngrel_coins_positive"]=f"{(pc.slope>0).sum()} of {len(pc)}"
    # per window
    pw={}
    for w,d in g.groupby("w"):
        if len(d)>30:
            r=stats.linregress(d["rngrel_r"],d["f5_z"]); pw[w]=(r.slope,r.slope/r.stderr,len(d))
    pw=pd.DataFrame(pw,index=["slope","t","n"]).T
    out["rngrel_windows_positive"]=f"{(pw.slope>0).sum()} of {len(pw)}"
    # weekday robustness
    wdd=g.groupby("wd").agg(n=("sq","size"),mean_w=("sq","mean"),median=("f5_ex","median"),z=("f5_z","mean"))
    out["weekday_winsor"]=wdd
    pww={}
    for w,d in g.groupby("w"):
        m=d.groupby("wd")["f5_z"].mean(); pww[w]=m
    pww=pd.DataFrame(pww).T
    out["weekday_windows_positive_share"]=(pww>0).mean()
    # 1-day weekday effect on daily returns (all bars)
    A["r1n"]=A.groupby(["coin","w"])["r1"].shift(-1)
    st=A.groupby("coin")["r1n"].agg(["mean","std"])
    A["r1z"]=(A["r1n"]-A["coin"].map(st["mean"]))/A["coin"].map(st["std"])
    out["next_day_by_close_weekday"]=A.groupby("wd")["r1z"].agg(["size","mean"])
    return out

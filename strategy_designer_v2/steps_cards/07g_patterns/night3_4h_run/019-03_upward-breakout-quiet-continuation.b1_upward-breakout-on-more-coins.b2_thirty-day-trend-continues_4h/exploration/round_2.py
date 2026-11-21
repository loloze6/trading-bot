def explore(data):
    import numpy as np, pandas as pd
    H=18
    rows=[]; hb=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            rng=(hi-lo)/c; r1=c.pct_change()
            ts=pd.to_datetime(df["timestamp"])
            vol=r1.rolling(30).std()
            feat=pd.DataFrame({"coin":coin,"win":w,"yr":ts.dt.year,
                "fc":df["forecast"].astype(float),"fwd":c.shift(-H)/c-1,
                "r6z":(c/c.shift(6)-1)/(vol*np.sqrt(6)),
                "r6":c/c.shift(6)-1,
                "comp":rng.rolling(30).mean()/rng.rolling(180).mean(),
                "vr":vol/r1.rolling(180).std(),
                "lastrng":rng/rng.rolling(30).mean()}).iloc[::H]
            rows.append(feat)
            hb.append(pd.DataFrame({"coin":coin,"yr":ts.dt.year,"hour":ts.dt.hour,"nxt":c.shift(-1)/c-1}))
    g=pd.concat(rows,ignore_index=True).dropna(subset=["fwd"])
    st=g.groupby("coin")["fwd"].agg(["mean","std"])
    g["ex"]=g["fwd"]-g["coin"].map(st["mean"]); g["s"]=g["ex"]/g["coin"].map(st["std"])
    out={}
    def tt(x): 
        x=x.dropna(); return pd.Series({"n":len(x),"m":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # 1 comp effect within forecast state
    d=g.dropna(subset=["comp"]).copy()
    d["cq"]=pd.qcut(d["comp"].rank(method="first"),5,labels=False)
    d["on"]=(d.fc>0).astype(int)
    out["comp_by_on"]=d.groupby(["on","cq"])["s"].apply(tt).unstack().round(4)
    # 2 multiple regression
    d=g.dropna(subset=["comp","r6z","lastrng","vr"]).copy()
    X=np.column_stack([np.ones(len(d)),d.fc,np.log(d.comp),d.r6z.clip(-4,4),np.log(d.lastrng.clip(0.05,None)),np.log(d.vr)])
    y=d.s.values; b,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b
    cov=np.linalg.inv(X.T@X)*(e@e)/(len(y)-X.shape[1])
    out["ols"]=pd.DataFrame({"b":b,"t":b/np.sqrt(np.diag(cov))},index=["c","fc","logcomp","r6z","loglastrng","logvr"]).round(4)
    # 3 reversal after large one-day falls, graded by vol-scaled size
    d=g.dropna(subset=["r6z"]).copy()
    d["q"]=pd.qcut(d["r6z"].rank(method="first"),10,labels=False)
    a=d.groupby("q").agg(lo=("r6z","min"),hi=("r6z","max"),ex=("ex","mean")); a=a.join(d.groupby("q")["s"].apply(tt).unstack())
    out["r6z_dec"]=a.round(4)
    bot=d[d.q<=1]
    out["r6z_bottom_by_yr"]=bot.groupby("yr")["s"].apply(tt).unstack().round(3)
    out["r6z_bottom_by_on"]=bot.groupby(bot.fc>0)["s"].apply(tt).unstack().round(3)
    # 4 direction after expanded ranges
    d=g.dropna(subset=["comp","r6z"]).copy()
    d["cq"]=pd.qcut(d["comp"].rank(method="first"),5,labels=False)
    top=d[d.cq==4].copy(); top["dirs"]=np.sign(top.r6)*top.s
    out["exp_rev_by_yr"]=top.groupby("yr")["dirs"].apply(tt).unstack().round(3)
    top["mq"]=pd.qcut(top.r6z.abs().rank(method="first"),3,labels=False)
    out["exp_rev_by_size"]=top.groupby("mq")["dirs"].apply(tt).unstack().round(3)
    out["exp_rev_up_vs_down"]=top.groupby(np.sign(top.r6))["s"].apply(tt).unstack().round(3)
    # 5 hour 16 by year and coin
    h=pd.concat(hb,ignore_index=True).dropna(subset=["nxt"])
    h16=h[h.hour==16]
    out["h16_by_yr"]=h16.groupby("yr")["nxt"].apply(lambda x:tt(x*1e4)).unstack().round(2)
    pc=h16.groupby("coin")["nxt"].mean()
    out["h16_coins_pos"]=f"{(pc>0).sum()} of {len(pc)}"
    return out

def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r1=c.pct_change()
            sma=c.rolling(20,min_periods=20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"ts":pd.to_datetime(b["timestamp"]),
               "dist":c/sma-1,"ret1":r1,"ret5":c/c.shift(5)-1,"tr30":c/c.shift(30)-1,
               "vol10":r1.rolling(10,min_periods=10).std(),
               "fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,"fwd5":c.shift(-5)/c-1,"fwd10":c.shift(-10)/c-1,
               "clpos":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
               "regime":b["regime"],"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True); D["day"]=D["ts"].dt.floor("D")
    D["tg"]=np.where(D.tr30>0.10,"rising",np.where(D.tr30<-0.10,"falling","choppy"))
    D["ag"]=np.where(D.vol10>D.groupby("coin")["vol10"].transform("median"),"agit","calm")
    def slope(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<30: return pd.Series({"n":len(df),"slope":np.nan,"t":np.nan})
        X=df[x]-df[x].mean(); Y=df[y]-df[y].mean()
        b=(X*Y).sum()/(X*X).sum(); e=Y-b*X
        sc=(X*e).groupby(df["day"]).sum(); se=np.sqrt((sc**2).sum())/(X*X).sum()
        return pd.Series({"n":len(df),"days":df.day.nunique(),"slope":b,"t":b/se})
    def dt(df,col):
        df=df.dropna(subset=[col]); mu=df[col].mean()
        dev=(df[col]-mu).groupby(df["day"]).sum(); se=np.sqrt((dev**2).sum())/len(df)
        return pd.Series({"n":len(df),"days":df.day.nunique(),"mean%":100*mu,"t_day":mu/se})
    out={}
    res={}
    for h in [1,2,5,10]:
        g=D[D.pos%h==0].copy(); m=g.groupby("coin")[f"fwd{h}"].mean(); g["ex"]=g[f"fwd{h}"]-g["coin"].map(m)
        gg=g[g.dist>0]
        for (tg,ag),s in gg.groupby(["tg","ag"]):
            r=slope(s,"dist","ex"); res[(h,tg,ag)]=r
    out["dist_pos_slope_by_h_profile"]=pd.DataFrame(res).T
    # falling agitated: up day then giveback (short side empty)
    g=D[D.pos%2==0].copy(); m=g.groupby("coin")["fwd2"].mean(); g["ex2"]=g["fwd2"]-g["coin"].map(m)
    g["rq"]=g.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["ex2_by_ret1_quint_profile"]=g.groupby(["tg","ag","rq"]).apply(lambda d: dt(d,"ex2"))[["n","mean%","t_day"]].unstack("rq")["t_day"]
    out["ex2_by_ret1_quint_profile_mean"]=g.groupby(["tg","ag","rq"]).apply(lambda d: dt(d,"ex2"))["mean%"].unstack("rq")
    out["slope_ret1_ex2_by_profile"]=g.groupby(["tg","ag"]).apply(lambda d: slope(d,"ret1","ex2"))
    g["cq"]=pd.cut(g.clpos,[-0.01,0.2,0.4,0.6,0.8,1.01],labels=False)
    out["ex2_by_clpos_profile_t"]=g.groupby(["tg","ag","cq"]).apply(lambda d: dt(d,"ex2"))["t_day"].unstack("cq")
    # book daily
    days=pd.concat([x.assign(coin=c) for c,ws in data["days"].items() for x in ws.values()],ignore_index=True)
    bk=days.groupby("day")["book_return"].mean().dropna()
    q=bk.quantile([0.02,0.98])
    big=days[days.day.isin(bk[bk>=q[0.98]].index)]; small=days[days.day.isin(bk[bk<=q[0.02]].index)]
    out["book_tails"]=pd.Series({"n_days":len(bk),"top2%_mean":bk[bk>=q[0.98]].mean(),"bot2%_mean":bk[bk<=q[0.02]].mean(),
        "share_gain_top2%":bk[bk>=q[0.98]].sum()/bk.sum(),"share_loss_bot2%":bk[bk<=q[0.02]].sum()/bk.sum()})
    return out

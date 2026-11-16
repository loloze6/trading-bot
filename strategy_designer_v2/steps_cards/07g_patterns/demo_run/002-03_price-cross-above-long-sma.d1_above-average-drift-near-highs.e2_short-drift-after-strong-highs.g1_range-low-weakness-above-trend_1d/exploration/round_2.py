def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; drows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            p20=c/c.shift(20)-1
            ma200=c.rolling(200,min_periods=200).mean()
            f5=c.shift(-5)/c-1
            vol=c.pct_change().rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            idx=np.arange(0,len(b),5)
            rows.append(pd.DataFrame({"coin":coin,"w":w,"p20":p20.iloc[idx].values,"f5":f5.iloc[idx].values,
                "vol":vol.iloc[idx].values,"reg":b["regime"].iloc[idx].values,"fc":b["forecast"].iloc[idx].values,
                "pos":b["postRebalance_current_allocation"].iloc[idx].values,"year":ts.dt.year.iloc[idx].values}))
        for w,d in data["days"][coin].items():
            d=d.copy(); d["coin"]=coin; d["w"]=w
            dd=pd.to_datetime(d["day"]); d["wd"]=dd.dt.weekday; d["year"]=dd.dt.year
            d["prev"]=d["coin_return"].shift(1)
            drows.append(d)
    G=pd.concat(rows).dropna(subset=["f5"])
    G["ex"]=G["f5"]-G.groupby("coin")["f5"].transform("mean")
    G["vn"]=G["p20"]/(G["vol"]*np.sqrt(20))
    out={}
    T=G[G.reg=="trending"].dropna(subset=["p20","vn"])
    def spear(df,x):
        r,p=stats.spearmanr(df[x],df["ex"]); return r,len(df),p
    res=[]
    for coin,s in T.groupby("coin"):
        r,n,p=spear(s,"vn"); res.append((coin,"trend vn",round(r,3),n,round(p,4)))
    U=G[G.reg!="trending"].dropna(subset=["vn"])
    for coin,s in U.groupby("coin"):
        r,n,p=spear(s,"vn"); res.append((coin,"unknown vn",round(r,3),n,round(p,4)))
    r,n,p=spear(T,"vn"); res.append(("ALL","trend vn",round(r,3),n,round(p,5)))
    r,n,p=spear(U,"vn"); res.append(("ALL","unknown vn",round(r,3),n,round(p,5)))
    out["spearman vol-normed 20d ret vs ex5"]=pd.DataFrame(res,columns=["coin","set","rho","n","p"])
    T["half"]=np.where(T["year"]<=2021,"2018-21","2022-25")
    T["vq"]=T.groupby("coin")["vn"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    a=T.groupby(["half","vq"])["ex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["trend: vn quintile by half"]=a.drop(columns="std").round(4)
    # book: realised short P&L per grid by forecast bucket
    A=G[G.reg=="trending"].copy()
    A["fb"]=pd.cut(A["fc"],[-21,-15,-10,-5,-0.001,0.001])
    A["posret"]=A["pos"]*A["f5"]
    out["trend: pos*f5 and ex by fc bucket"]=A.groupby("fb")[["posret","ex","f5","pos"]].agg(["mean"]).round(4).join(A.groupby("fb")["ex"].count().rename("n"))
    D=pd.concat(drows).dropna(subset=["coin_return"])
    D["cex"]=D["coin_return"]-D.groupby("coin")["coin_return"].transform("mean")
    sat=D[D.wd==5]; oth=D[D.wd!=5]
    out["sat minus others welch"]=str(stats.ttest_ind(sat["cex"],oth["cex"],equal_var=False))
    a=sat.groupby("coin")["cex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["sat by coin"]=a.round(5)
    a=sat.groupby("year")["cex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["sat by year"]=a.round(5)
    # Saturday excess graded by Friday's return?
    sat2=sat.dropna(subset=["prev"]).copy()
    sat2["pq"]=sat2.groupby("coin")["prev"].transform(lambda s: pd.qcut(s,3,labels=False))
    a=sat2.groupby("pq")["cex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["sat by fri return tercile"]=a.round(5)
    # daily reversal after large moves
    D2=D.dropna(subset=["prev"]).copy()
    D2["pq"]=D2.groupby("coin")["prev"].transform(lambda s: pd.qcut(s,5,labels=False))
    a=D2.groupby("pq")["cex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["next-day excess by prev-day quintile"]=a.round(5)
    return out

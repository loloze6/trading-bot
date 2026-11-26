def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wd in data["bars"].items():
        for w,df in wd.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            n=len(c)
            pmax=c.shift(1).rolling(60).max(); pmin=c.shift(1).rolling(60).min()
            pmax20=c.shift(1).rolling(20).max(); pmin20=c.shift(1).rolling(20).min()
            r1=c.pct_change()
            feat=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(n),
                "fwd":c.shift(-H)/c-1,
                "fwd10":c.shift(-10)/c-1,
                "rp60":(c-pmin)/(pmax-pmin),
                "rp20":(c-pmin20)/(pmax20-pmin20),
                "dist_hi":c/pmax-1,
                "vol20":r1.rolling(20).std(),
                "day":pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "year":pd.to_datetime(df["timestamp"]).dt.year,
                "alloc":df["postRebalance_current_allocation"].astype(float)})
            rows.append(feat)
    A=pd.concat(rows,ignore_index=True)
    G=A[A["pos"]%H==0].dropna(subset=["fwd"]).copy()
    drift=G.groupby("coin")["fwd"].mean()
    G["ux"]=G["fwd"]-G["coin"].map(drift)
    G["uxs"]=G["ux"]/G["coin"].map(G.groupby("coin")["fwd"].std())
    out={}
    def qtab(d,col,q=5):
        d=d.dropna(subset=[col,"ux"]).copy()
        d["q"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        g=d.groupby("q")
        res=pd.DataFrame({"mean_col":g[col].mean(),"mean_ux":g["ux"].mean(),"str":g["uxs"].mean(),
                          "t":g["ux"].mean()/(g["ux"].std()/np.sqrt(g["ux"].count())),"n":g["ux"].count()})
        return res
    out["rp60_q"]=qtab(G,"rp60")
    out["rp20_q"]=qtab(G,"rp20")
    d=G.dropna(subset=["rp60","ux"]).copy()
    d["sc"]=d["rp60"]-0.5
    # day clustered t of slope-ish: product signal
    d["prod"]=d["sc"]*d["uxs"]
    pdays=d.groupby("day")["prod"].sum()
    out["rp60_prod_dayt"]=pd.Series({"mean_per_day":pdays.mean(),"t":pdays.mean()/(pdays.std()/np.sqrt(len(pdays))),"days":len(pdays),
        "spearman":stats.spearmanr(d["rp60"],d["ux"])[0],"spearman_p":stats.spearmanr(d["rp60"],d["ux"])[1]})
    # by window: spearman
    out["rp60_by_win"]=d.groupby("win").apply(lambda x: pd.Series({"rho":stats.spearmanr(x["rp60"],x["ux"])[0],"n":len(x),
        "top_minus_bot":x[x.rp60>0.8]["ux"].mean()-x[x.rp60<0.2]["ux"].mean()}))
    out["rp60_by_coin"]=d.groupby("coin").apply(lambda x: pd.Series({"rho":stats.spearmanr(x["rp60"],x["ux"])[0],"n":len(x)}))
    out["rp60_by_year"]=d.groupby("year").apply(lambda x: pd.Series({"rho":stats.spearmanr(x["rp60"],x["ux"])[0],"n":len(x)}))
    # interaction with vol: low vs high vol halves
    d["vh"]=d.groupby("coin")["vol20"].transform(lambda s: s>s.median())
    out["rp60_by_volhalf"]=d.groupby("vh").apply(lambda x: pd.Series({"rho":stats.spearmanr(x["rp60"],x["ux"])[0],"n":len(x)}))
    # 10-day horizon on a 10 grid
    G10=A[A["pos"]%10==0].dropna(subset=["fwd10","rp60"]).copy()
    G10["ux"]=G10["fwd10"]-G10["coin"].map(G10.groupby("coin")["fwd10"].mean())
    out["rp60_q_10d"]=qtab(G10.assign(uxs=0),"rp60")
    # book: in-position vs not, relative to rp60
    out["share_inpos_by_rp60q"]=d.assign(q=pd.qcut(d["rp60"].rank(method="first"),5,labels=False)).groupby("q")["alloc"].apply(lambda s:(s.abs()>0).mean())
    return out

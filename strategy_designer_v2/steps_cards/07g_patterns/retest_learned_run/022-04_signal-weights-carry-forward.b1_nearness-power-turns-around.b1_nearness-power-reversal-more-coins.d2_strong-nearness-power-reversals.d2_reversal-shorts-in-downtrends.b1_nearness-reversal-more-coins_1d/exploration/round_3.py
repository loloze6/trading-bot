def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change()
            d=pd.DataFrame(index=b.index); d["coin"]=coin; d["win"]=w
            d["fwd"]=c.shift(-H)/c-1
            d["r20"]=c/c.shift(20)-1
            v20=r1.rolling(20,min_periods=15).std(); v60=r1.rolling(60,min_periods=40).std()
            d["volratio"]=v20/v60
            d["r5z"]=(c/c.shift(5)-1)/(v20*np.sqrt(5))
            d["rng"]=(b["high"].astype(float)-b["low"].astype(float))/c/v20
            vol=b["volume"].astype(float).replace(0,np.nan)
            d["volu"]=np.log(vol/vol.rolling(20,min_periods=15).mean())
            d["r1"]=r1
            ts=pd.to_datetime(b["timestamp"]); d["yr"]=ts.dt.year.values; d["wd"]=ts.dt.dayofweek.values
            d["grid"]=(np.arange(len(b))%H==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.grid & D.fwd.notna()].copy()
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    G["exs"]=G["ex"]/G.groupby("coin")["fwd"].transform("std")
    out={}
    def per(g,col,key):
        res={}
        for k,x in g[g[col].notna()].groupby(key):
            if len(x)<40: continue
            s=stats.spearmanr(x[col],x["exs"]).correlation
            res[k]=s
        s=pd.Series(res)
        return s
    specs=[("rng",G),("volu",G),("r5z",G[G.r20<0]),("volratio",G[G.r20<0])]
    for col,g in specs:
        sy=per(g,col,"yr"); sc=per(g,col,"coin")
        gg=g[g[col].notna()]
        # signed-raw rng: rng times sign of day return
        out[col+" summary"]=pd.Series({"rho_all":stats.spearmanr(gg[col],gg.exs).correlation,"n":len(gg),
            "years_pos_share":(sy>0).mean(),"n_years":len(sy),"coins_pos_share":(sc>0).mean(),"n_coins":len(sc)}).round(3)
        out[col+" rho by year"]=sy.round(3)
    # rng split by direction of the day
    g=G[G.rng.notna()&G.r1.notna()].copy()
    g["up"]=g.r1>0
    g["b"]=g.groupby("coin")["rng"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    a=g.groupby(["up","b"])["exs"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    a["ex_pct"]=g.groupby(["up","b"])["ex"].mean()*100
    out["rng by day direction"]=a.round(3)
    # volu tail split by vol direction
    g=G[G.volu.notna()].copy()
    for col in ["rng","volu"]:
        g2=G[G[col].notna()]
        out[col+" rho controlling r5z sign"]=pd.Series({"r5z>0":stats.spearmanr(g2[g2.r5z>0][col],g2[g2.r5z>0].exs).correlation,
                                                     "r5z<=0":stats.spearmanr(g2[g2.r5z<=0][col],g2[g2.r5z<=0].exs).correlation}).round(3)
    a=G.groupby(["wd"])["exs"].agg(["mean","count"])
    out["weekday by year: Tue minus Sun"]=(G[G.wd==1].groupby("yr")["exs"].mean()-G[G.wd==6].groupby("yr")["exs"].mean()).round(3)
    return out

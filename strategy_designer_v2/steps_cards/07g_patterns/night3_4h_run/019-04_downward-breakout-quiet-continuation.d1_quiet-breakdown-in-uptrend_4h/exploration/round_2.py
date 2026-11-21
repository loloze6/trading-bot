def explore(data):
    import numpy as np, pandas as pd
    H=18
    per=[]
    for coin, wins in data["bars"].items():
        grid=[]; dfs=[]
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            s=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            n=len(s)
            f=s.shift(-H)/s-1
            f6=s.shift(-6)/s-1
            r1=s/s.shift(1)-1
            r6=s/s.shift(6)-1
            vol=r1.rolling(180,min_periods=90).std()
            r6z=r6/(vol*np.sqrt(6))
            r180=s/s.shift(180)-1
            minlo=lo.shift(1).rolling(12).min(); maxhi=hi.shift(1).rolling(12).max()
            comp=(maxhi-minlo)/(hi-lo).rolling(180).mean()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"f":f,"f6":f6,"r6":r6,"r6z":r6z,"r180":r180,"comp":comp,"dn":s<minlo,
                             "pos":np.arange(n),"coin":coin,"w":w,"yr":ts.dt.year,"wd":ts.dt.weekday})
            dfs.append(df); grid.append(f.iloc[::H].dropna())
        g=pd.concat(grid); drift=g.mean(); sd=g.std()
        for df in dfs:
            df["u"]=df["f"]-drift; df["z"]=df["u"]/sd
            per.append(df)
    A=pd.concat(per,ignore_index=True)
    G=A[A["pos"]%H==0].dropna(subset=["u","r6z","r180"]).copy()
    def summ(x,col="u"):
        v=x[col].dropna()
        return pd.Series({"n":len(v),"mean":v.mean(),"t":v.mean()/(v.std()/np.sqrt(len(v))),"strength":x["z"].mean()})
    out={}
    G["d"]=G.groupby("coin")["r6z"].transform(lambda x: pd.qcut(x,10,labels=False))
    out["grid_by_1day_zret_decile"]=G.groupby("d").apply(summ)
    G["tr"]=np.where(G["r180"]>0,"r180+","r180-")
    G["q"]=G.groupby("coin")["r6z"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["grid_trend_x_zret_quint"]=G.groupby(["tr","q"]).apply(summ)
    low=G[G["q"]==0]
    out["lowquint_by_coin"]=low.groupby("coin").apply(summ)
    out["lowquint_by_year"]=low.groupby("yr").apply(summ)
    wins_t=low.groupby("w")["u"].mean()
    out["lowquint_windows_positive_share"]=float((wins_t>0).mean())
    out["lowquint_n_windows"]=int(len(wins_t))
    # spearman of r6z vs u per coin
    out["spearman_r6z_u_by_coin"]=G.groupby("coin").apply(lambda x: pd.Series({"rho":x["r6z"].corr(x["u"],method="spearman"),"n":len(x)}))
    # 1-day horizon after falls (grid 6)
    G6=A[A["pos"]%6==0].dropna(subset=["f6","r6z"]).copy()
    G6["u6"]=G6["f6"]-G6.groupby("coin")["f6"].transform("mean")
    G6["z"]=G6["u6"]/G6.groupby("coin")["f6"].transform("std")
    G6["q"]=G6.groupby("coin")["r6z"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["grid6_next1day_by_zret_quint"]=G6.groupby("q").apply(lambda x: summ(x,"u6"))
    # down-break wide stretch in uptrend vs controlled by 1-day ret
    D=A[A["dn"] & A["u"].notna() & A["comp"].notna() & A["r6z"].notna()].copy()
    D["cell"]=D["pos"]//H
    D=D.groupby(["coin","w","cell"]).head(1)
    D["ct"]=D.groupby("coin")["comp"].transform(lambda x: pd.qcut(x,3,labels=False))
    D["fq"]=D.groupby("coin")["r6z"].transform(lambda x: pd.qcut(x,2,labels=["deepfall","mildfall"]))
    out["downbreak_r180pos_comp_x_fall"]=D[D["r180"]>0].groupby(["ct","fq"]).apply(summ)
    return out

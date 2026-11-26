def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change()
            df=pd.DataFrame(index=b.index)
            df["coin"]=coin; df["w"]=w
            df["r1"]=r1
            df["vol20"]=r1.rolling(20).std().shift(1)
            df["z"]=r1/df["vol20"]
            df["ret28"]=c/c.shift(28)-1
            df["f1"]=c.shift(-1)/c-1
            df["f3"]=c.shift(-3)/c-1
            df["g3"]=(np.arange(len(b))%3==0)
            ts=pd.to_datetime(b["timestamp"])
            df["yr"]=ts.dt.year.values; df["wd"]=ts.dt.weekday.values; df["day"]=ts.dt.floor("D").values
            df["alloc"]=b["postRebalance_current_allocation"].astype(float).values
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    mu1=A.groupby("coin")["f1"].mean()
    A["ex1"]=A["f1"]-A.coin.map(mu1)
    G3=A[A.g3].copy(); mu3=G3.groupby("coin")["f3"].mean(); G3["ex3"]=G3["f3"]-G3.coin.map(mu3)
    def daysumm(g,col):
        g=g.dropna(subset=[col]); n=len(g)
        if n<3: return pd.Series({"n":n,"days":np.nan,"mean":np.nan,"t_day":np.nan})
        m=g[col].mean(); s=g.groupby("day")[col].sum(); k=g.groupby("day")[col].count()
        se=np.sqrt(((s-k*m)**2).sum())/n
        return pd.Series({"n":n,"days":len(s),"mean":m,"t_day":m/se})
    out={}
    bins=[-99,-3,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,99]
    A["zb"]=pd.cut(A.z,bins)
    out["next1_by_z_dayclustered"]=A.groupby("zb").apply(lambda g: daysumm(g,"ex1"))
    G3["zb"]=pd.cut(G3.z,bins)
    out["next3_grid_by_z"]=G3.groupby("zb").apply(lambda g: daysumm(g,"ex3"))
    dn=A[A.z<=-1]
    out["corr_z_ex1_down"]=float(dn[["z","ex1"]].corr().iloc[0,1])
    out["down_z_le_-1_by_year"]=dn.groupby("yr").apply(lambda g: daysumm(g,"ex1"))
    out["down_z_le_-1_by_coin"]=dn.groupby("coin").apply(lambda g: daysumm(g,"ex1"))
    out["down_z_le_-1_by_trend"]=dn.groupby(dn.ret28>0).apply(lambda g: daysumm(g,"ex1"))
    out["down_z_le_-1_book_in_position_share"]=float((dn.alloc.abs()>0).mean())
    out["weekday_ex1_by_year_fri_sat"]=A[A.wd.isin([3,4,5])].groupby(["yr","wd"]).apply(lambda g: daysumm(g,"ex1"))
    return out

def explore(data):
    import numpy as np, pandas as pd
    H=36
    rows=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rs+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(rs) if rs else np.nan; usual[coin]=np.std(rs,ddof=1) if len(rs)>1 else np.nan
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            hh=b["high"].rolling(12).max().shift(1)
            rng=(b["high"]-b["low"]).rolling(180,min_periods=45).mean()
            raw=((b["close"]-hh)/rng).values
            r7=(b["close"]/b["close"].shift(42)-1).values
            lv=(b["high"].rolling(12).max().shift(1)-b["low"].rolling(12).min().shift(1))/rng
            lv=lv.values
            base=0.0; bet_cells=set()
            n=len(c)
            for t in range(n):
                if f[t]<=0: base=0.0; continue
                if f[t]<base: base=f[t]
                if f[t]-base>=2:
                    base=f[t]
                    cell=t//H
                    if cell in bet_cells: continue
                    bet_cells.add(cell)
                    d={"coin":coin,"w":w,"year":pd.Timestamp(b["timestamp"].iloc[t]).year,"f":f[t],"raw":raw[t],"r7":r7[t],"narrow":lv[t]}
                    for h in [6,12,18,36,72]:
                        d["u%d"%h]=(c[t+h]/c[t]-1 - drift[coin]*h/H) if t+h<n else np.nan
                    d["s36"]=d["u36"]/usual[coin] if not np.isnan(d["u36"]) else np.nan
                    rows.append(d)
    df=pd.DataFrame(rows); df=df[df.u36.notna()]
    def st(g,col="u36"):
        x=g[col].dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["n_total"]=len(df)
    out["forecast_dist"]=df["f"].describe()
    out["share_f_at_20"]=float((df.f>=19.99).mean())
    df["rawq"]=pd.qcut(df.raw.rank(method="first"),5,labels=False)
    out["by_raw_quintile"]=df.groupby("rawq").apply(st).join(df.groupby("rawq").raw.mean())
    df["r7q"]=pd.qcut(df.r7.rank(method="first"),5,labels=False)
    out["by_r7_quintile"]=df.groupby("r7q").apply(st).join(df.groupby("r7q").r7.mean())
    df["nq"]=pd.qcut(df.narrow.rank(method="first"),5,labels=False)
    out["by_narrowness_q"]=df.groupby("nq").apply(st).join(df.groupby("nq").narrow.mean())
    out["by_coin"]=df.groupby("coin").apply(st)
    out["by_year"]=df.groupby("year").apply(st)
    out["by_horizon"]=pd.DataFrame({h:st(df,"u%d"%h) for h in [6,12,18,36,72]}).T
    out["corr_raw_u36_spearman"]=float(df[["raw","u36"]].corr(method="spearman").iloc[0,1])
    out["corr_f_u36_spearman"]=float(df[["f","u36"]].corr(method="spearman").iloc[0,1])
    return out

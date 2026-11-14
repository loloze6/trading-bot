def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.reset_index(drop=True).copy()
            c=d["close"].astype(float)
            r=np.log(c).diff()
            d["r1"]=r; d["f1"]=r.shift(-1)
            d["f10"]=np.log(c.shift(-10)/c)
            d["vol20"]=r.rolling(20).std()
            d["z"]=r/d["vol20"].shift(1)
            d["ret10p"]=np.log(c/c.shift(10))
            col="debug_info.components.below_sma200.last_history_value"
            d["dist"]=d[col] if col in d else np.nan
            d["coin"]=coin; d["w"]=w; d["i"]=np.arange(len(d))
            ts=pd.to_datetime(d["timestamp"])
            d["wd"]=ts.dt.weekday; d["yr"]=ts.dt.year
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["xf1"]=A["f1"]-A.groupby("coin")["f1"].transform("mean")
    A["m10"]=A.groupby("coin")["f10"].transform("mean"); A["x10"]=A["f10"]-A["m10"]
    def summ(g,col):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"hit":(x>0).mean()})
    out={}
    # weekday of the bar's own return (r1 at bar dated wd), already labelled as next-day of wd-1; recheck with r1 directly
    A["xr1"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    A["wdn"]=(A["wd"]+1)%7
    out["fri_next_by_coin"]=A[A["wd"]==4].groupby("coin").apply(lambda g:summ(g,"xf1"))
    out["fri_next_by_year"]=A[A["wd"]==4].groupby("yr").apply(lambda g:summ(g,"xf1"))
    out["wed_next_by_coin"]=A[A["wd"]==2].groupby("coin").apply(lambda g:summ(g,"xf1"))
    out["wed_next_by_year"]=A[A["wd"]==2].groupby("yr").apply(lambda g:summ(g,"xf1"))
    D=A[A["z"]<=-1]
    out["down_next_by_coin"]=D.groupby("coin").apply(lambda g:summ(g,"xf1"))
    out["down_next_by_year"]=D.groupby("yr").apply(lambda g:summ(g,"xf1"))
    D=D.copy(); D["below"]=np.where(D["dist"]<0,"below","above")
    out["down_next_by_sma_side"]=D.groupby("below").apply(lambda g:summ(g,"xf1"))
    U=A[A["z"]>=1].copy(); U["below"]=np.where(U["dist"]<0,"below","above")
    out["up_next_by_sma_side"]=U.groupby("below").apply(lambda g:summ(g,"xf1"))
    G=A[(A["i"]%10==0)&A["f10"].notna()].copy()
    G["mb"]=G.groupby("coin")["ret10p"].transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["top_past10_by_coin"]=G[G["mb"]==4].groupby("coin").apply(lambda g:summ(g,"x10"))
    out["top_past10_by_year"]=G[G["mb"]==4].groupby("yr").apply(lambda g:summ(g,"x10"))
    return out

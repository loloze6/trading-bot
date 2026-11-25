def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            rng=(b.high-b.low)
            d["cl"]=((b.high-b.close)/rng).where(rng>0)
            d["r0"]=b.close/b.close.shift(1)-1
            d["r1"]=b.close.shift(-1)/b.close-1
            d["r3"]=b.close.shift(-3)/b.close-1
            d["rngp"]=rng/b.close
            d["rngz"]=d.rngp/d.rngp.rolling(20,min_periods=10).mean().shift(1)
            d["r5p"]=b.close/b.close.shift(5)-1
            d["agit"]=(b.regime!="chop").astype(int)
            d["pos"]=b.postRebalance_current_allocation
            d["wd"]=pd.to_datetime(b.timestamp).dt.weekday
            d["pos_in_w"]=np.arange(len(b))
            d["coin"]=c; d["w"]=w; d["ts"]=pd.to_datetime(b.timestamp).dt.floor("D")
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin").r1.transform("mean")
    D["x1"]=D.r1-mu
    D["x3"]=D.r3-D.groupby("coin").r3.transform("mean")
    def summ(g,col="x1"):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    D["clq"]=pd.qcut(D.cl,5,labels=False)
    out["cl_quint_by_agit"]=D.groupby(["agit","clq"]).apply(summ).round(3)
    D["r0q"]=pd.qcut(D.r0,5,labels=False)
    out["r0_quint_by_agit"]=D.groupby(["agit","r0q"]).apply(summ).round(3)
    A=D[D.agit==1]
    out["agit_cl_x_r0sign"]=A.groupby([np.sign(A.r0),pd.qcut(A.cl,3,labels=False)]).apply(summ).round(3)
    A2=A.copy(); A2["rzq"]=pd.qcut(A2.rngz,3,labels=False)
    out["agit_cl_x_rangewidth"]=A2.groupby(["rzq",pd.qcut(A2.cl,3,labels=False)]).apply(summ).round(3)
    G=D[D.pos_in_w%3==0]
    out["cl_quint_3d_by_agit"]=G.groupby(["agit","clq"]).apply(lambda g:summ(g,"x3")).round(3)
    D["r5q"]=pd.qcut(D.r5p,5,labels=False)
    out["r5_quint_next1_by_agit"]=D.groupby(["agit","r5q"]).apply(summ).round(3)
    out["weekday_all"]=D.groupby("wd").apply(summ).round(3)
    out["cl_by_coin_agit_corr"]=A.groupby("coin").apply(lambda g:pd.Series({"n":g[["cl","x1"]].dropna().shape[0],"corr":g.cl.corr(g.x1)})).round(3)
    out["rngz_tercile_next_absret"]=D.groupby(pd.qcut(D.rngz,3,labels=False)).apply(lambda g:pd.Series({"n":g.r1.notna().sum(),"abs%":100*g.r1.abs().mean(),"mean%":100*g.x1.mean()})).round(3)
    return out

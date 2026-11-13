def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(60,min_periods=20).std(); mu=r.rolling(60,min_periods=20).mean()
            ts=pd.to_datetime(b["timestamp"])
            hl=(b["high"]-b["low"]).replace(0,np.nan)
            df=pd.DataFrame({"coin":coin,"w":w,"r":r,"z":(r-mu)/sd,"n1":r.shift(-1),
                "reg":b["regime"].values,"yr":ts.dt.year.values,"wd":ts.dt.dayofweek.values,
                "cl":((c-b["low"])/hl).values,"rng":(hl/c).values,
                "vrel":(b["volume"]/b["volume"].rolling(20,min_periods=10).mean()).values,
                "pos":b["postRebalance_current_allocation"].astype(float).values})
            df["rngz"]=df["rng"]/df["rng"].rolling(60,min_periods=20).mean()
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["z","n1","cl"])
    d["n1x"]=d["n1"]-d.groupby("coin")["n1"].transform("mean")
    def agg(g):
        x=g["n1x"]
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,"up":(g["n1"]>0).mean()})
    out={}
    d["clb"]=pd.cut(d["cl"],[-0.01,0.1,0.3,0.7,0.9,1.01])
    out["all_by_cl"]=d.groupby("clb").apply(agg)
    d["sign"]=np.where(d["r"]<0,"down","up")
    out["cl_by_sign"]=d.groupby(["sign","clb"]).apply(agg)
    lowc=d[d.cl<=0.1]
    out["lowclose_by_year"]=lowc.groupby("yr").apply(agg)
    out["lowclose_by_coin"]=lowc.groupby("coin").apply(agg)
    out["lowclose_by_reg"]=lowc.groupby("reg").apply(agg)
    out["lowclose_by_rngz"]=lowc.groupby(pd.qcut(lowc["rngz"],3)).apply(agg)
    out["lowclose_smalldrop"]=lowc.groupby(pd.cut(lowc["z"],[-99,-1.5,-0.5,99])).apply(agg)
    hic=d[d.cl>=0.9]
    out["hiclose_by_year"]=hic.groupby("yr").apply(agg)
    # wide-range day by sign
    d["rq"]=d.groupby("coin")["rngz"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["rangeq_by_sign"]=d.groupby(["rq","sign"]).apply(agg)
    # weekday stability
    d["half"]=np.where(d["yr"]<=2021,"early","late")
    out["wd_by_half"]=d.groupby(["wd","half"]).apply(agg)["mean"].unstack()
    out["wd_by_half_t"]=d.groupby(["wd","half"]).apply(agg)["t"].unstack()
    # book: where pnl comes from
    dy=pd.concat([t.assign(coin=c) for c,ws in data["days"].items() for t in ws.values()])
    out["book_ret_desc"]=dy["book_return"].describe()
    return out

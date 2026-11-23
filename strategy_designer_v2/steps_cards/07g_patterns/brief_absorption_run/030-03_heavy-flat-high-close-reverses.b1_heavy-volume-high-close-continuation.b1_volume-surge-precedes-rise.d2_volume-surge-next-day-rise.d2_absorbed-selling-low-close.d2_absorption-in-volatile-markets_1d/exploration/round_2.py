def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["dist_high"]=(b["high"]-c)/rng
            d["volr"]=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            v20=r.rolling(20).std()
            d["vr"]=v20/v20.rolling(60).mean()
            d["r1"]=r
            d["r5p"]=c/c.shift(5)-1
            d["rngrel"]=(rng/c)/((rng/c).shift(1).rolling(20).mean())
            d["f1"]=c.shift(-1)/c-1
            d["f3"]=c.shift(-3)/c-1
            d["pos3"]=(np.arange(len(b))%3==0)
            d["active"]=(b["regime"]=="mean_reversion").values
            d["fc"]=b["forecast"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values
            d["yr"]=ts.dt.year.values
            d["absr"]=(c/b["open"]-1).abs()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["f1"].transform("mean")
    D["x1"]=D["f1"]-mu
    mu3=D[D.pos3].groupby("coin")["f3"].mean()
    D["x3"]=D["f3"]-D["coin"].map(mu3)
    out={}
    def tab(g,col="x1",sub=None):
        S=D if sub is None else sub
        a=S.dropna(subset=[col]).groupby(g)[col].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a.drop(columns="std")
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err: "+str(e)[:80]
    D["clq"]=pd.qcut(D["dist_high"],5,labels=False,duplicates="drop")
    D["vq"]=pd.qcut(D["volr"],3,labels=False)
    D["vrq"]=pd.qcut(D["vr"],3,labels=False)
    D["r1q"]=pd.qcut(D["r1"],5,labels=False)
    D["absq"]=pd.qcut(D["absr"],3,labels=False)
    D["r5q"]=pd.qcut(D["r5p"],5,labels=False)
    D["rgq"]=pd.qcut(D["rngrel"],3,labels=False)
    safe("clq x active",lambda: tab(["active","clq"]))
    safe("clq x volr terc t",lambda: tab(["vq","clq"])["t"].unstack(0))
    safe("clq x vr terc t",lambda: tab(["vrq","clq"])["t"].unstack(0))
    safe("clq x vr terc mean",lambda: tab(["vrq","clq"])["mean"].unstack(0))
    safe("clq x range-rel terc t",lambda: tab(["rgq","clq"])["t"].unstack(0))
    safe("3d grid clq x active",lambda: tab(["active","clq"],"x3",D[D.pos3]))
    safe("r1q x vr terc t",lambda: tab(["vrq","r1q"])["t"].unstack(0))
    safe("r1q x vr terc mean",lambda: tab(["vrq","r1q"])["mean"].unstack(0))
    safe("clq x body terc t",lambda: tab(["absq","clq"])["t"].unstack(0))
    safe("r5q x vr terc t",lambda: tab(["vrq","r5q"])["t"].unstack(0))
    safe("r5q x vr terc mean",lambda: tab(["vrq","r5q"])["mean"].unstack(0))
    safe("weekday all",lambda: tab("wd"))
    safe("weekday long",lambda: tab("wd",sub=D[D.alloc>0]))
    safe("year long",lambda: tab("yr",sub=D[D.alloc>0]))
    safe("year all",lambda: tab("yr"))
    def coin_t():
        res={}
        for cn,g in D.groupby("coin"):
            g=g.dropna(subset=["dist_high","x1"])
            lr=stats.linregress(g["dist_high"],g["x1"]); res[cn]=lr.slope/lr.stderr
        return pd.Series(res)
    safe("coin dist_high slope t all bars",coin_t)
    def fcq():
        S=D[D.fc>0].copy(); S["fq"]=pd.qcut(S["fc"],5,labels=False,duplicates="drop")
        return tab("fq",sub=S)
    safe("forecast quint long bars",fcq)
    safe("active but flat vs long",lambda: tab(D["alloc"]>0,sub=D[D.active]))
    # book days: largest gains/losses
    def bk():
        dd=[]
        for coin,wins in data["days"].items():
            for w,x in wins.items():
                x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
        X=pd.concat(dd); X["day"]=pd.to_datetime(X["day"])
        B=X.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna().reset_index()
        B=B.sort_values(["win","day"])
        B["br_next"]=B.groupby("win")["br"].shift(-1)
        B["cr_prev"]=B.groupby("win")["cr"].shift(1)
        B["bq"]=pd.qcut(B["br"],10,labels=False,duplicates="drop")
        g=B.groupby("bq").agg(br=("br","mean"),cr=("cr","mean"),next_br=("br_next","mean"),prev_cr=("cr_prev","mean"),n=("br","count"))
        return g
    safe("book decile days",bk)
    return out

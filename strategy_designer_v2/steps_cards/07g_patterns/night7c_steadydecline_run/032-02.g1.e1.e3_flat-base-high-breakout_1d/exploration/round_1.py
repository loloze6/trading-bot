def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            f=pd.DataFrame({"coin":coin,"win":w})
            f["fwd"]=c.shift(-H)/c-1
            f["r28"]=c/c.shift(28)-1
            f["r5p"]=c/c.shift(5)-1
            f["r1p"]=r1
            f["dist"]=c/c.rolling(28).max()-1
            f["distlow"]=c/c.rolling(28).min()-1
            f["vol20"]=r1.rolling(20).std()
            f["volrel"]=f["vol20"]/r1.rolling(60,min_periods=40).std()
            rng=(b["high"]-b["low"])/c
            f["rngrel"]=rng/rng.rolling(28).mean()
            v=b["volume"].astype(float)
            f["vrel"]=v/v.rolling(28).mean()
            f["fc"]=b["forecast"].astype(float)
            f["alloc"]=b["postRebalance_current_allocation"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            f["wd"]=ts.dt.weekday
            f["yr"]=ts.dt.year
            f["pos"]=np.arange(len(b))
            rows.append(f)
    A=pd.concat(rows,ignore_index=True)
    G=A[(A["pos"]%H==0)&A["fwd"].notna()].copy()
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    out={}
    def tab(col,q=5):
        d=G.dropna(subset=[col,"ex"]).copy()
        d["b"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        t=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean_ex=("ex","mean"),
                             t=("ex",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
        sl=stats.spearmanr(d[col],d["ex"])
        t.loc["spearman"]=[np.nan,np.nan,len(d),sl.correlation,sl.pvalue]
        return t
    for col in ["r28","r5p","r1p","dist","distlow","vol20","volrel","rngrel","vrel"]:
        out["fwd5ex by "+col]=tab(col)
    # at-high cases vs r28
    hi=G[G["dist"]>=-1e-12].copy()
    out["athigh n,mean,t"]=pd.Series({"n":len(hi),"mean":hi["ex"].mean(),"t":hi["ex"].mean()/(hi["ex"].std()/np.sqrt(len(hi)))})
    # near high within 5% vs vol
    nh=G[G["dist"]>-0.05].dropna(subset=["volrel"]).copy()
    nh["b"]=pd.qcut(nh["volrel"].rank(method="first"),3,labels=False)
    out["nearhigh by volrel"]=nh.groupby("b")["ex"].agg(["size","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # calm decline: r28 low & volrel low
    d=G.dropna(subset=["r28","volrel"]).copy()
    d["rq"]=pd.qcut(d["r28"].rank(method="first"),3,labels=["dn","mid","up"])
    d["vq"]=pd.qcut(d["volrel"].rank(method="first"),3,labels=["calm","mid","wild"])
    out["r28 x volrel mean_ex"]=d.pivot_table(index="rq",columns="vq",values="ex",aggfunc="mean")
    out["r28 x volrel n"]=d.pivot_table(index="rq",columns="vq",values="ex",aggfunc="size")
    out["by coin"]=G.groupby("coin")["ex"].agg(["size","mean"])
    out["by weekday (all bars 1d next ret)"]=A.assign(n1=A.groupby(["coin","win"])["r1p"].shift(-1)).groupby("wd")["n1"].agg(["size","mean",lambda x:x.mean()/(x.std()/np.sqrt(x.count()))])
    # book daily
    D=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy();x["coin"]=coin;x["win"]=w;D.append(x)
    D=pd.concat(D)
    D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    bk["wd"]=bk.index.get_level_values("day").weekday
    out["book by weekday"]=bk.groupby("wd")["br"].agg(["size","mean"])
    out["book by window"]=bk.groupby(level="win").agg(br=("br","mean"),cr=("cr","mean"),n=("br","size"))
    # trades
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): x=t.copy();x["coin"]=coin;T.append(x)
    T=pd.concat(T)
    T["net"]=T["net_profit_loss_percent"].astype(float)
    T["q"]=pd.qcut(T["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades by entry fc q"]=T.groupby("q").agg(n=("net","size"),fc=("entry_forecast","mean"),net=("net","mean"),win=("net",lambda x:(x>0).mean()))
    out["trades duration days"]=pd.Series({"mean":T["duration_minutes"].mean()/1440,"median":T["duration_minutes"].median()/1440,"n":len(T)})
    return out

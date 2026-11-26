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
            f=pd.DataFrame(index=b.index)
            f["coin"]=coin; f["win"]=w
            f["fwd"]=c.shift(-H)/c-1
            f["fwd1"]=c.shift(-1)/c-1
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
            ts=pd.to_datetime(b["timestamp"])
            f["wd"]=ts.dt.weekday.values
            f["yr"]=ts.dt.year.values
            f["pos"]=np.arange(len(b))
            rows.append(f)
    A=pd.concat(rows,ignore_index=True)
    G=A[(A["pos"]%H==0)&A["fwd"].notna()].copy()
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    out={}
    def tt(x):
        x=x.dropna()
        return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    def tab(col,q=5,d=None):
        d=(G if d is None else d).dropna(subset=[col,"ex"]).copy()
        d["b"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        t=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean_ex=("ex","mean"),t=("ex",tt))
        sl=stats.spearmanr(d[col],d["ex"])
        t.loc["spearman"]=[np.nan,np.nan,len(d),sl.correlation,sl.pvalue]
        return t
    for col in ["r28","r5p","r1p","dist","distlow","volrel","rngrel","vrel"]:
        try: out["ex5 by "+col]=tab(col)
        except Exception as e: out["err "+col]=str(e)
    try:
        hi=G[G["dist"]>=-1e-12]
        out["athigh"]=pd.Series({"n":len(hi),"mean":hi["ex"].mean(),"t":tt(hi["ex"])})
        nh=G[G["dist"]>-0.03]
        out["nearhigh(3%) ex5 by r28"]=tab("r28",3,nh)
        out["nearhigh(3%) ex5 by volrel"]=tab("volrel",3,nh)
        out["nearhigh(3%) ex5 by vrel"]=tab("vrel",3,nh)
    except Exception as e: out["err hi"]=str(e)
    try:
        d=G.dropna(subset=["r28","volrel"]).copy()
        d["rq"]=pd.qcut(d["r28"].rank(method="first"),3,labels=["dn","mid","up"])
        d["vq"]=pd.qcut(d["volrel"].rank(method="first"),3,labels=["calm","mid","wild"])
        out["r28 x volrel mean_ex"]=d.pivot_table(index="rq",columns="vq",values="ex",aggfunc="mean")
        out["r28 x volrel t"]=d.pivot_table(index="rq",columns="vq",values="ex",aggfunc=tt)
        out["r28 x volrel n"]=d.pivot_table(index="rq",columns="vq",values="ex",aggfunc="size")
    except Exception as e: out["err grid"]=str(e)
    try:
        out["ex5 by year"]=G.groupby("yr")["ex"].agg(["size","mean",tt])
        out["by coin"]=G.groupby("coin")["ex"].agg(["size","mean",tt])
        out["next1d by weekday"]=A.groupby("wd")["fwd1"].agg(["size","mean",tt])
    except Exception as e: out["err misc"]=str(e)
    try:
        D=[]
        for coin,wins in data["days"].items():
            for w,dd in wins.items():
                x=dd.copy();x["coin"]=coin;x["win"]=w;D.append(x)
        D=pd.concat(D,ignore_index=True)
        D["day"]=pd.to_datetime(D["day"])
        bk=D.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna().reset_index()
        bk["wd"]=bk["day"].dt.weekday
        out["book by weekday"]=bk.groupby("wd")["br"].agg(["size","mean",tt])
        out["book by window"]=bk.groupby("win").agg(br=("br","mean"),cr=("cr","mean"),n=("br","size"))
        bk["cq"]=pd.qcut(bk["cr"].rank(method="first"),5,labels=False)
        out["book by coins-day quintile"]=bk.groupby("cq").agg(cr=("cr","mean"),br=("br","mean"),n=("br","size"))
    except Exception as e: out["err book"]=str(e)
    try:
        T=[]
        for coin,wins in data["trades"].items():
            for w,t in wins.items():
                if len(t): x=t.copy();x["coin"]=coin;T.append(x)
        T=pd.concat(T,ignore_index=True)
        T["net"]=T["net_profit_loss_percent"].astype(float)
        T["efc"]=T["entry_forecast"].astype(float)
        T["q"]=pd.qcut(T["efc"].rank(method="first"),4,labels=False)
        out["trades by entry fc q"]=T.groupby("q").agg(n=("net","size"),fc=("efc","mean"),net=("net","mean"),win=("net",lambda x:(x>0).mean()))
        out["trades dur days"]=pd.Series({"mean":T["duration_minutes"].mean()/1440,"median":T["duration_minutes"].median()/1440,"n":len(T),"net_mean":T["net"].mean(),"net_t":tt(T["net"])})
    except Exception as e: out["err trades"]=str(e)
    return out

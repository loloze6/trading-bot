def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book daily returns
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B = B.dropna()
    v = (1+B["book_return"]).cumprod(); dd_ = v/v.cummax()-1
    B["dd"] = dd_.values
    vh = (1+B["coin_return"]).cumprod(); B["ddh"] = (vh/vh.cummax()-1).values
    out["deepest fall book / hold"] = pd.Series({"book": B["dd"].min(), "hold": B["ddh"].min(),
        "book_sharpe": B.book_return.mean()/B.book_return.std()*np.sqrt(365),
        "hold_sharpe": B.coin_return.mean()/B.coin_return.std()*np.sqrt(365)})
    pw = B.groupby("wn").agg(book=("book_return", lambda x:(1+x).prod()-1),
                              hold=("coin_return", lambda x:(1+x).prod()-1),
                              mindd=("dd","min"), n=("book_return","size"))
    out["per window"] = pw
    # bar-level features
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            b["r1"] = b["close"].shift(-1)/b["close"]-1
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            b["ret5"] = b["close"]/b["close"].shift(5)-1
            lr = np.log(b["close"]).diff()
            b["vol20"] = lr.rolling(20).std()
            b["above50"] = (b["close"] > b["close"].rolling(50, min_periods=20).mean()).astype(float)
            b.loc[b["close"].rolling(50, min_periods=20).mean().isna(),"above50"]=np.nan
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"]=c; b["w"]=w
            rows.append(b[["r1","ret20","ret5","vol20","above50","alloc","forecast","coin","w"]])
    X = pd.concat(rows)
    mu = X.groupby("coin")["r1"].transform("mean")
    X["ex"] = X["r1"]-mu
    out["alloc stats"] = pd.Series({"share alloc>0": (X.alloc>0.001).mean(),
        "share fc>0": (X.forecast>0).mean(), "mean alloc fc==0": X.loc[X.forecast<=0,"alloc"].mean(),
        "mean alloc fc>0": X.loc[X.forecast>0,"alloc"].mean(), "mean alloc": X.alloc.mean(),
        "corr alloc fc": X[["alloc","forecast"]].corr().iloc[0,1]})
    X["q"] = pd.qcut(X["forecast"].rank(method="first"), 5, labels=False)
    g = X.dropna(subset=["r1"]).groupby("q").agg(n=("r1","size"), r1=("r1","mean"), ex=("ex","mean"),
            alloc=("alloc","mean"), fc=("forecast","mean"))
    out["by forecast fifth"] = g
    # state splits
    X["trend"] = np.where(X.ret20>0,"up20","dn20")
    X.loc[X.ret20.isna(),"trend"]=np.nan
    X["volt"] = X.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    def tab(col):
        r=[]
        for k, s in X.dropna(subset=["r1",col]).groupby(col):
            for hi in [False, True]:
                ss = s[(s.q>=3)==hi]
                t = ss.r1.mean()/ss.r1.std()*np.sqrt(len(ss))
                r.append({"state":k,"topfifths":hi,"n":len(ss),"r1":ss.r1.mean(),"ex":ss.ex.mean(),
                          "alloc":ss.alloc.mean(),"t":t,"pnl_alloc":(ss.alloc*ss.r1).mean()})
        return pd.DataFrame(r)
    out["by trend20"] = tab("trend")
    out["by above50"] = tab("above50")
    out["by vol tercile"] = tab("volt")
    # deepest fall period: alloc and coin
    i = B["dd"].idxmin()
    # find peak
    sub = B.loc[:i]
    pk = sub["dd"][sub["dd"]==0].index.max()
    fall = B.loc[pk:i]
    out["deepest fall"] = pd.Series({"windows": f"w{fall.wn.min()}-w{fall.wn.max()}", "days": len(fall),
        "book": (1+fall.book_return).prod()-1, "hold": (1+fall.coin_return).prod()-1})
    # pnl contributions: alloc*r1 by trend and fc>0
    X["pnl"] = X.alloc*X.r1
    out["pnl by trend x fc>0"] = X.dropna(subset=["r1","trend"]).groupby(["trend", X.forecast>0]).agg(
        n=("pnl","size"), pnl=("pnl","mean"), alloc=("alloc","mean"), r1=("r1","mean"))
    return out

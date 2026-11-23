def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy().reset_index(drop=True)
            dd["coin"] = c; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows, ignore_index=True)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"]).dropna().reset_index(drop=True)
    v = (1+B["book_return"]).cumprod(); B["dd"] = (v/v.cummax()-1).values
    vh = (1+B["coin_return"]).cumprod(); B["ddh"] = (vh/vh.cummax()-1).values
    yrs = len(B)/365
    out["book summary"] = pd.Series({"book_dd": B.dd.min(), "hold_dd": B.ddh.min(),
        "book_yr": v.iloc[-1]**(1/yrs)-1, "hold_yr": vh.iloc[-1]**(1/yrs)-1,
        "book_sharpe": B.book_return.mean()/B.book_return.std()*np.sqrt(365),
        "hold_sharpe": B.coin_return.mean()/B.coin_return.std()*np.sqrt(365),
        "corr book hold": B[["book_return","coin_return"]].corr().iloc[0,1]})
    out["per window"] = B.groupby("wn").agg(book=("book_return", lambda x:(1+x).prod()-1),
        hold=("coin_return", lambda x:(1+x).prod()-1), mindd=("dd","min")).round(3)
    i = int(B["dd"].idxmin()); sub = B.loc[:i]
    pk = int(sub.index[sub["dd"]==0].max()); fall = B.loc[pk:i]
    out["deepest fall"] = pd.Series({"windows": f"w{fall.wn.min()}-w{fall.wn.max()}", "days": len(fall),
        "book": (1+fall.book_return).prod()-1, "hold": (1+fall.coin_return).prod()-1})
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            b["r1"] = b["close"].shift(-1)/b["close"]-1
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            ma50 = b["close"].rolling(50, min_periods=20).mean()
            b["above50"] = np.where(ma50.isna(), np.nan, (b["close"]>ma50).astype(float))
            b["vol20"] = np.log(b["close"]).diff().rolling(20).std()
            rng = (b.high-b.low).replace(0,np.nan)
            b["clv"] = (b.high-b.close)/rng
            b["vr"] = b.volume/b.volume.shift(1).rolling(20).mean()
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"]=c; b["wn"]=int(w[1:])
            rows.append(b[["r1","ret20","above50","vol20","clv","vr","alloc","forecast","coin","wn"]])
    X = pd.concat(rows, ignore_index=True)
    X["ex"] = X["r1"] - X.groupby("coin")["r1"].transform("mean")
    X["pnl"] = X.alloc*X.r1
    out["alloc stats"] = pd.Series({"share alloc>0.001": (X.alloc>0.001).mean(),
        "share fc>0": (X.forecast>0).mean(), "mean alloc fc<=0": X.loc[X.forecast<=0,"alloc"].mean(),
        "mean alloc fc>0": X.loc[X.forecast>0,"alloc"].mean(),
        "pnl share from fc<=0 bars": X.loc[X.forecast<=0,"pnl"].sum()/X.pnl.sum()})
    X["q"] = pd.qcut(X["forecast"].rank(method="first"), 5, labels=False)
    out["by forecast fifth"] = X.dropna(subset=["r1"]).groupby("q").agg(n=("r1","size"), r1=("r1","mean"),
        ex=("ex","mean"), alloc=("alloc","mean"), fc=("forecast","mean"), pnl=("pnl","mean"))
    X["trend"] = np.where(X.ret20.isna(), np.nan, np.where(X.ret20>0,1.0,0.0))
    X["volt"] = X.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    X["sig"] = (X.q>=3).astype(int)
    def tab(col):
        r=[]
        for (k,hi), ss in X.dropna(subset=["r1",col]).groupby([col,"sig"]):
            r.append({"state":k,"sig":hi,"n":len(ss),"r1":ss.r1.mean(),"ex":ss.ex.mean(),
                      "t":ss.r1.mean()/ss.r1.std()*np.sqrt(len(ss)),"alloc":ss.alloc.mean(),"pnl":ss.pnl.mean()})
        return pd.DataFrame(r).round(5)
    out["by trend20 x sig"] = tab("trend")
    out["by above50 x sig"] = tab("above50")
    out["by vol tercile x sig"] = tab("volt")
    # graded within signal: vr and clv buckets
    X["vrb"] = pd.cut(X.vr,[0,1,1.5,2.5,100]); X["clvb"]=pd.cut(X.clv,[-.01,.33,.66,1.01])
    out["r1 by vr x clv"] = X.dropna(subset=["r1"]).groupby(["vrb","clvb"],observed=True).agg(
        n=("r1","size"), ex=("ex","mean"), alloc=("alloc","mean")).round(5)
    # fall period: what held
    fw = set(range(fall.wn.min(), fall.wn.max()+1))
    F = X[X.wn.isin(fw)]
    out["fall period vs rest"] = pd.DataFrame({"fall": [F.alloc.mean(), (F.forecast>0).mean(), F.pnl.mean(), F.r1.mean(), F.trend.mean()],
        "rest": [X[~X.wn.isin(fw)].alloc.mean(), (X[~X.wn.isin(fw)].forecast>0).mean(), X[~X.wn.isin(fw)].pnl.mean(), X[~X.wn.isin(fw)].r1.mean(), X[~X.wn.isin(fw)].trend.mean()]},
        index=["alloc","share fc>0","pnl","r1","share up20"])
    # multi-day horizon of signal (non-overlapping 3-day)
    r=[]
    for h in [1,3,5]:
        vals=[]
        for c in coins:
            for w,b in bars[c].items():
                b=b.reset_index(drop=True)
                fr = b.close.shift(-h)/b.close-1
                idx = np.arange(0,len(b),h)
                vals.append(pd.DataFrame({"fr":fr.iloc[idx].values,"fc":b.forecast.iloc[idx].values,"coin":c}))
        V=pd.concat(vals,ignore_index=True).dropna()
        V["ex"]=V.fr-V.groupby("coin").fr.transform("mean")
        hi=V[V.fc>V.fc.quantile(0.6)]; lo=V[V.fc<=V.fc.quantile(0.6)]
        r.append({"h":h,"n_hi":len(hi),"ex_hi":hi.ex.mean(),"t_hi":hi.ex.mean()/hi.ex.std()*np.sqrt(len(hi)),
                  "ex_lo":lo.ex.mean(),"sd":V.fr.std()})
    out["horizons"]=pd.DataFrame(r)
    return out

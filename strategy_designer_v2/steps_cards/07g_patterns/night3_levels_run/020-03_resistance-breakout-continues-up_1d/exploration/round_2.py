import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std().shift(1)
            z = r1 / vol
            past20 = c / c.shift(20) - 1
            hi = c.rolling(90, min_periods=30).max()
            dd90 = c / hi - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            for t in range(1, n - 1):
                daily.append(dict(coin=coin, w=w, yr=yr[t], r1=r1[t], z=z[t], past20=past20[t], dd90=dd90[t],
                                  nxt=c[t+1]/c[t]-1, wdn=wd[t+1], fc=float(b["forecast"][t])))
            for t in range(1, n - 3, 3):
                pass
    d = pd.DataFrame(daily)
    d["drift"] = d.groupby("coin")["nxt"].transform("mean")
    d["sd"] = d.groupby("coin")["nxt"].transform("std")
    d["ex"] = d["nxt"] - d["drift"]; d["st"] = d["ex"] / d["sd"]
    out = {}
    def tt(s):
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean()/(s.std()/np.sqrt(len(s)))))
    x = d.dropna(subset=["z"]).copy()
    x["q"] = x.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    r = x.groupby("q").agg(n=("ex","size"), mean=("ex","mean"), sd=("ex","std"), strength=("st","mean"), zmean=("z","mean"))
    r["t"] = r["mean"]/(r["sd"]/np.sqrt(r["n"])); out["next day ex by vol-scaled ret decile"] = r.drop(columns="sd")
    low = x[x["q"] <= 1]
    out["bottom 2 deciles by coin"] = low.groupby("coin")["ex"].apply(tt).unstack()
    out["bottom 2 deciles by year"] = low.groupby("yr")["ex"].apply(tt).unstack()
    low["wgrp"] = low["w"].str[1:].astype(int).apply(lambda k: "w1-8" if k <= 8 else ("w9-16" if k <= 16 else "w17-24"))
    out["bottom 2 deciles by window group"] = low.groupby("wgrp")["ex"].apply(tt).unstack()
    # graded within falls: spearman of z vs ex among z<0
    neg = x[x["z"] < 0]
    out["spearman z vs ex, falls only"] = pd.Series(dict(rho=stats.spearmanr(neg["z"], neg["ex"])[0], n=len(neg),
        p=stats.spearmanr(neg["z"], neg["ex"])[1]))
    # regime: falls in uptrend vs downtrend (past20 sign)
    low["up20"] = (low["past20"] > 0).astype(int)
    out["bottom 2 deciles by past20 sign"] = low.groupby("up20")["ex"].apply(tt).unstack()
    low["deep"] = pd.qcut(low["dd90"].rank(method="first"), 3, labels=False)
    out["bottom 2 deciles by drawdown tercile"] = low.groupby("deep")["ex"].apply(tt).unstack()
    # weekday by coin (Saturday)
    out["saturday ex by coin"] = d[d["wdn"] == 5].groupby("coin")["ex"].apply(tt).unstack()
    out["saturday ex by year"] = d[d["wdn"] == 5].groupby("yr")["ex"].apply(tt).unstack()
    # book's largest losses/gains: coin return day after
    bk = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            y = dy[["book_return", "coin_return"]].copy().reset_index(drop=True)
            y["next_coin"] = y["coin_return"].shift(-1); y["coin"] = coin; bk.append(y)
    bk = pd.concat(bk).dropna()
    bk["q"] = bk.groupby("coin")["book_return"].transform(lambda s: pd.qcut(s.rank(method="first"), 20, labels=False))
    out["next coin ret by book-return 5% bins (ends)"] = bk[bk["q"].isin([0, 1, 18, 19])].groupby("q")["next_coin"].apply(tt).unstack()
    return out

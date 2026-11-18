import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    dd = []
    for coin, wins in days.items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday; D["yr"] = D["day"].dt.year
    D["wkend"] = D["wd"].isin([4, 5]).astype(int)
    def tt(a, b):
        r = stats.ttest_ind(a, b, equal_var=False); return r.statistic
    res = {}
    for coin, g in D.groupby("coin"):
        res[coin] = {"sat_mean": g[g.wd==5].coin_return.mean(), "other_mean": g[g.wd!=5].coin_return.mean(),
                     "t_sat_minus_other": tt(g[g.wd==5].coin_return, g[g.wd!=5].coin_return), "n_sat": (g.wd==5).sum()}
    out["saturday vs other by coin"] = pd.DataFrame(res).T
    res = {}
    for y, g in D.groupby("yr"):
        res[y] = {"sat_mean": g[g.wd==5].coin_return.mean(), "other_mean": g[g.wd!=5].coin_return.mean(),
                  "t": tt(g[g.wd==5].coin_return, g[g.wd!=5].coin_return), "n_sat": (g.wd==5).sum()}
    out["saturday vs other by year"] = pd.DataFrame(res).T
    res = {}
    for w, g in D.groupby("w"):
        res[w] = g[g.wd==5].coin_return.mean() - g[g.wd!=5].coin_return.mean()
    s = pd.Series(res)
    out["sat minus other by window: share>0, t"] = pd.Series({"share_pos": (s>0).mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))), "n": len(s)})
    # Fri+Sat vs others, per coin
    res = {}
    for coin, g in D.groupby("coin"):
        res[coin] = {"frisat_minus_other": g[g.wkend==1].coin_return.mean()-g[g.wkend==0].coin_return.mean(),
                     "t": tt(g[g.wkend==1].coin_return, g[g.wkend==0].coin_return)}
    out["fri+sat vs other by coin"] = pd.DataFrame(res).T
    # book by weekday
    g = D.groupby("wd")["book_return"].agg(["mean", "count", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["book by weekday"] = g
    # timestamp hour check
    b0 = bars["BTCUSD"]["w1"]
    out["bar start hour"] = str(pd.to_datetime(b0["timestamp"]).dt.hour.value_counts().to_dict())
    # ret5 momentum, pooled, non-overlapping 7d, by coin and by vol level
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            s = b["close"].reset_index(drop=True); n = len(s)
            r1 = s.pct_change(); vol20 = r1.rolling(20).std()
            ret5 = s/s.shift(5)-1; ret5z = ret5/(vol20*np.sqrt(5))
            for t in range(0, n-7, 7):
                rows.append(dict(coin=coin, w=w, fwd=s[t+7]/s[t]-1, ret5=ret5[t], ret5z=ret5z[t], vol20=vol20[t],
                                 yr=pd.Timestamp(b["timestamp"].iloc[t]).year))
    d = pd.DataFrame(rows).dropna()
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    r = stats.linregress(d["ret5z"], d["ex"]); out["ret5z pooled slope"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(d)})
    r = stats.linregress(d["ret5"], d["ex"]); out["ret5 pooled slope"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(d)})
    res = {}
    for y, g in d.groupby("yr"):
        r = stats.linregress(g["ret5z"], g["ex"]); res[y] = {"slope": r.slope, "t": r.slope/r.stderr, "n": len(g)}
    out["ret5z slope by year"] = pd.DataFrame(res).T
    d["vq"] = d.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    res = {}
    for q, g in d.groupby("vq"):
        r = stats.linregress(g["ret5z"], g["ex"]); res[q] = {"slope": r.slope, "t": r.slope/r.stderr, "n": len(g)}
    out["ret5z slope by vol tercile"] = pd.DataFrame(res).T
    return out

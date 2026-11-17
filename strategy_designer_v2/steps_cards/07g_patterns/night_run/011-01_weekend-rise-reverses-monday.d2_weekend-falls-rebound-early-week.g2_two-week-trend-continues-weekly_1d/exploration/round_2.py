import numpy as np, pandas as pd
from scipy import stats

def tt(x):
    x = pd.Series(x).dropna()
    return x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    dr = []
    for coin in days:
        for w, dd in days[coin].items():
            dd = dd.copy().reset_index(drop=True)
            dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            dd["next"] = dd["coin_return"].shift(-1)
            dd["vol"] = dd["coin_return"].rolling(20).std()
            dd["z"] = dd["coin_return"]/dd["vol"].shift(1)
            dd["coin"] = coin; dd["w"] = w
            dr.append(dd)
    D = pd.concat(dr, ignore_index=True)
    neg = D[D["z"] < 0].dropna(subset=["z", "next"]).copy()
    pos = D[D["z"] > 0].dropna(subset=["z", "next"]).copy()
    res = {}
    for nm, g in [("down days", neg), ("up days", pos)]:
        r = stats.linregress(g["z"], g["next"])
        res[nm] = [len(g), r.slope, r.slope/r.stderr]
    out["next-day slope on z, split by sign"] = pd.DataFrame(res, index=["n", "slope", "t"])
    neg["zq"] = pd.qcut(neg["z"], 5, labels=False)
    out["down days: next day by z quintile"] = neg.groupby("zq").agg(n=("next", "size"), z=("z", "mean"), nxt=("next", "mean"), t=("next", tt))
    big = D[D["z"] < -1].dropna(subset=["next"])
    out["after z<-1: next day by coin"] = big.groupby("coin")["next"].agg(["size", "mean", tt])
    out["after z<-1: next day by year"] = big.groupby("year")["next"].agg(["size", "mean", tt])
    out["after z<-1: next day by weekday of drop"] = big.groupby("wd")["next"].agg(["size", "mean", tt])
    out["saturday coin return by coin"] = D[D.wd == 5].groupby("coin")["coin_return"].agg(["size", "mean", tt])
    out["saturday coin return by year"] = D[D.wd == 5].groupby("year")["coin_return"].agg(["size", "mean", tt])
    # relative volume interaction by year, 7-bar grid
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].values; n = len(b)
            vrel = (b["volume"]/b["volume"].rolling(30).mean()).values
            v14 = (b["volume"].rolling(14).mean()/b["volume"].rolling(60, min_periods=30).mean()).values
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n-7, 7):
                rows.append(dict(coin=coin, year=ts[t].year, f=b["forecast"].iloc[t], fwd7=c[t+7]/c[t]-1, vrel=vrel[t], v14=v14[t]))
    d = pd.DataFrame(rows)
    d["ex7"] = d["fwd7"] - d.groupby("coin")["fwd7"].transform("mean")
    d["prod"] = d["f"]*d["ex7"]
    d["vrq"] = d.groupby("coin")["vrel"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    d["v14q"] = d.groupby("coin")["v14"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["f*ex7 by within-coin 1d rel vol tercile"] = d.groupby("vrq")["prod"].agg(["size", "mean", tt])
    out["f*ex7 by within-coin 14d rel vol tercile"] = d.groupby("v14q")["prod"].agg(["size", "mean", tt])
    hi = d[d.vrq == 2]; lo = d[d.vrq == 0]
    out["high minus low rel vol: welch t"] = float(stats.ttest_ind(hi["prod"].dropna(), lo["prod"].dropna(), equal_var=False).statistic)
    out["high rel vol f*ex7 by coin"] = hi.groupby("coin")["prod"].agg(["size", "mean", tt])
    out["high rel vol f*ex7 by year"] = hi.groupby("year")["prod"].agg(["size", "mean", tt])
    return out

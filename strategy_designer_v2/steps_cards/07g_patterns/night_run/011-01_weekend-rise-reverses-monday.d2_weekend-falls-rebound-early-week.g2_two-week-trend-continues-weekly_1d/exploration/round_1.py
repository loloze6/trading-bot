import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std()
            r14 = pd.Series(c).pct_change(14)
            r3 = pd.Series(c).pct_change(3)
            r1d = r1
            vrel = b["volume"] / b["volume"].rolling(30).mean()
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n - 7, 7):
                rows.append(dict(coin=coin, w=w, wn=int(w[1:]), year=ts[t].year, wd=ts[t].dayofweek,
                                 f=b["forecast"].iloc[t], fwd7=c[t+7]/c[t]-1, fwd1=c[t+1]/c[t]-1,
                                 r1=r1d.iloc[t], r3=r3.iloc[t], r14=r14.iloc[t], vol=vol20.iloc[t],
                                 vrel=vrel.iloc[t], s=r14.iloc[t]/(vol20.iloc[t]*np.sqrt(14)) if vol20.iloc[t] else np.nan))
    d = pd.DataFrame(rows)
    d["ex7"] = d["fwd7"] - d.groupby("coin")["fwd7"].transform("mean")
    d["fq"] = pd.qcut(d["f"], 5, labels=False, duplicates="drop")
    out["fwd7 by forecast quintile"] = d.groupby("fq").agg(n=("ex7","size"), f=("f","mean"), ex7=("ex7","mean"),
        t=("ex7", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    d["vq"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    d["prod"] = d["f"]*d["ex7"]
    out["f*ex7 by vol tercile"] = d.groupby("vq")["prod"].agg(["size","mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["f*ex7 by coin"] = d.groupby("coin")["prod"].agg(["size","mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["f*ex7 by year"] = d.groupby("year")["prod"].agg(["size","mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # volume-relative interaction
    d["vrq"] = pd.qcut(d["vrel"], 3, labels=False, duplicates="drop")
    out["f*ex7 by rel volume tercile"] = d.groupby("vrq")["prod"].agg(["size","mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # daily-level: weekday and after-large-move, non-overlapping 1d is every bar
    dr = []
    for coin in days:
        for w, dd in days[coin].items():
            dd = dd.copy()
            dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
            dd["next"] = dd["coin_return"].shift(-1)
            dd["vol"] = dd["coin_return"].rolling(20).std()
            dd["z"] = dd["coin_return"]/dd["vol"].shift(1)
            dd["next3"] = dd["close"].shift(-3)/dd["close"]-1
            dd["coin"] = coin; dd["w"] = w
            dr.append(dd)
    D = pd.concat(dr)
    D["book_mkt"] = D["book_return"]
    out["coin & book by weekday"] = D.groupby("wd").agg(n=("coin_return","count"), coin=("coin_return","mean"),
        tcoin=("coin_return", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))),
        book=("book_return","mean"), tbook=("book_return", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))))
    D["zq"] = pd.qcut(D["z"], 5, labels=False, duplicates="drop")
    out["next day by today z quintile"] = D.groupby("zq").agg(n=("next","count"), z=("z","mean"), nxt=("next","mean"),
        t=("next", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))))
    # weekend z vs weekday z: next-day slope
    D["isw"] = D["wd"].isin([5,6])
    sl = {}
    for k, g in D.dropna(subset=["z","next"]).groupby("isw"):
        res = stats.linregress(g["z"], g["next"]); sl[str(k)] = [len(g), res.slope, res.slope/res.stderr]
    out["next-day slope on z, weekend(True)"] = pd.DataFrame(sl, index=["n","slope","t"])
    # book daily: by year, drawdown
    bk = D.groupby(["w","day"])["book_return"].mean().dropna()
    bkdf = bk.reset_index(); bkdf["year"] = pd.to_datetime(bkdf["day"]).dt.year
    out["book by year"] = bkdf.groupby("year")["book_return"].agg(["count","mean","std", lambda x: x.mean()/x.std()*np.sqrt(365)])
    return out

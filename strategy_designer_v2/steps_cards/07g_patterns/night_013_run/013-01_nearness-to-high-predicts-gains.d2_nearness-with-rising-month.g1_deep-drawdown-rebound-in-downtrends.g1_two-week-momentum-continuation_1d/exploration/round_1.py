import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            r1 = pd.Series(cl).pct_change().values
            vol20 = pd.Series(r1).rolling(20).std().values
            ret14 = pd.Series(cl).pct_change(14).values
            hi30 = pd.Series(b["high"].values).rolling(30).max().values
            near = cl / hi30 - 1
            v = b["volume"].values
            vrel = v / pd.Series(v).rolling(20).mean().values
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=c, win=w, f=b["forecast"].iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 r1=r1[i], vol=vol20[i], ret14=ret14[i], near=near[i], vrel=vrel[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 fwd=cl[i+7]/cl[i]-1))
    s = pd.DataFrame(rows)
    s["dm"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
    out = {}
    def grp(col, q=5):
        d = s.dropna(subset=[col, "dm"]).copy()
        d["g"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("g")["dm"]
        return pd.DataFrame({"lo": d.groupby("g")[col].min(), "n": g.size(), "mean": g.mean(),
                             "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    out["by forecast quintile"] = grp("f")
    out["by ret14 decile"] = grp("ret14", 10)
    out["by nearness to 30d high quintile"] = grp("near")
    out["by 1d return quintile"] = grp("r1")
    out["by vol quintile"] = grp("vol")
    out["by volume ratio quintile"] = grp("vrel")
    # slope per coin and per year
    def slope(d):
        d = d.dropna(subset=["f", "dm"])
        if len(d) < 20: return pd.Series({"n": len(d), "t": np.nan})
        r = stats.linregress(d["f"], d["dm"])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr})
    out["slope by coin"] = s.groupby("coin").apply(slope)
    out["slope by year"] = s.groupby("yr").apply(slope)
    # slope within vol tercile
    s["vt"] = pd.qcut(s["vol"], 3, labels=False)
    out["slope by vol tercile"] = s.groupby("vt").apply(slope)
    # book: daily long/short split
    dl = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            a = b["postRebalance_current_allocation"].values[:-1]
            r = b["close"].pct_change().shift(-1).values[:-1]
            wd = pd.to_datetime(b["timestamp"]).dt.dayofweek.values[:-1]
            dl.append(pd.DataFrame(dict(coin=c, a=a, r=r, g=a*r, wd=wd)))
    dl = pd.concat(dl)
    dl["side"] = np.where(dl["a"] > 0, "long", np.where(dl["a"] < 0, "short", "flat"))
    gg = dl.groupby("side")["g"]
    out["bar gain by side"] = pd.DataFrame({"n": gg.size(), "mean": gg.mean(), "t": gg.mean()/(gg.std()/np.sqrt(gg.size())), "meanabs_alloc": dl.groupby("side")["a"].apply(lambda x: x.abs().mean())})
    out["bar gain long by coin"] = dl[dl.side=="long"].groupby("coin")["g"].mean()
    out["bar gain short by coin"] = dl[dl.side=="short"].groupby("coin")["g"].mean()
    rw = dl.groupby("wd")["r"]
    out["coin next-day return by weekday"] = pd.DataFrame({"n": rw.size(), "mean": rw.mean(), "t": rw.mean()/(rw.std()/np.sqrt(rw.size()))})
    # book daily
    bd = []
    for c in days:
        for w, d in days[c].items():
            bd.append(d.assign(coin=c, win=w))
    bd = pd.concat(bd)
    br = bd.groupby(["win", "day"])["book_return"].mean().dropna()
    cr = bd.groupby(["win", "day"])["coin_return"].mean().dropna()
    out["book by window"] = pd.DataFrame({"book": br.groupby(level=0).mean(), "hold": cr.groupby(level=0).mean()})
    return out

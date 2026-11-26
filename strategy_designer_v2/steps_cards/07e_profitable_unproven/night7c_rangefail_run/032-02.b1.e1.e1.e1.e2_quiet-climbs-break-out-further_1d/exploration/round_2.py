import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    res = []
    for h in [10, 20, 40]:
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                a = cl[h::h]; allr += list(a / cl[:len(a) * h:h][:len(a)] - 1)
            mh = np.mean(allr)
            for w, b in bars[c].items():
                cl = b["close"].reset_index(drop=True)
                n = len(cl)
                pm = cl.shift(1).rolling(60).max()
                pmin = cl.shift(1).rolling(60).min()
                vol = np.log(cl).diff().rolling(20).std()
                R = cl.shift(1) / cl.shift(61) - 1
                R20 = cl / cl.shift(20) - 1
                brk = cl > pm
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                for s in range(0, n, h):
                    if s + h >= n: continue
                    idx = [i for i in range(s, min(s + h, n)) if brk.iloc[i]]
                    if idx:
                        i = idx[0]
                        if i + h >= n: continue
                        res.append(dict(h=h, coin=c, w=w, yr=yr[i], ts=str(b["timestamp"].iloc[i])[:10], brk=1,
                            dist=cl.iloc[i] / pm.iloc[i] - 1, distv=(np.log(cl.iloc[i] / pm.iloc[i])) / vol.iloc[i],
                            rng=pm.iloc[i] / pmin.iloc[i] - 1, R=R.iloc[i], R20=R20.iloc[i],
                            ex=cl.iloc[i + h] / cl.iloc[i] - 1 - mh))
                    elif not np.isnan(pm.iloc[s]):
                        res.append(dict(h=h, coin=c, w=w, yr=yr[s], ts=str(b["timestamp"].iloc[s])[:10], brk=0,
                            dist=cl.iloc[s] / pm.iloc[s] - 1, distv=np.nan, rng=pm.iloc[s] / pmin.iloc[s] - 1, R=R.iloc[s], R20=R20.iloc[s],
                            ex=cl.iloc[s + h] / cl.iloc[s] - 1 - mh))
    C = pd.DataFrame(res)
    def summ(g):
        dd = g.groupby("ts")["ex"].sum()
        return pd.Series({"n": len(g), "days": len(dd), "mean_ex": g.ex.mean(), "t_day": dd.mean() / dd.std() * np.sqrt(len(dd)) if len(dd) > 2 else np.nan})
    out["brk_vs_not"] = C.groupby(["h", "brk"]).apply(summ)
    B = C[C.brk == 1].copy()
    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        X = g[x] - g[x].mean(); y = g.ex - g.ex.mean()
        b = (X * y).sum() / (X ** 2).sum()
        e = y - b * X
        sc = (X * e).groupby(g.ts).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(g), "slope": b, "t_cl": b / se, "spearman": stats.spearmanr(g[x], g.ex)[0]})
    rows = []
    for h, g in B.groupby("h"):
        for x in ["dist", "distv", "rng", "R", "R20"]:
            s = slope(g, x); s["h"] = h; s["x"] = x; rows.append(s)
    out["slopes_breakouts"] = pd.DataFrame(rows)
    NB = C[C.brk == 0]
    rows = []
    for h, g in NB.groupby("h"):
        for x in ["dist", "rng", "R"]:
            s = slope(g, x); s["h"] = h; s["x"] = x; rows.append(s)
    out["slopes_nonbreak"] = pd.DataFrame(rows)
    out["brk_h20_by_year"] = B[B.h == 20].groupby("yr").apply(summ)
    B20 = B[B.h == 20].copy()
    B20["rq"] = pd.qcut(B20.rng, 3, labels=["tight", "mid", "wide"])
    B20["vq"] = pd.qcut(B20.distv, 3, labels=["small", "mid", "big"])
    out["h20_by_range_width"] = B20.groupby("rq").apply(summ)
    out["h20_by_dist_in_vol"] = B20.groupby("vq").apply(summ)
    # book trades by entry year
    tr = pd.concat([t for c in data["trades"] for t in data["trades"][c].values()])
    tr["yr"] = pd.to_datetime(tr["entry_time"]).dt.year
    out["trades_by_year"] = tr.groupby("yr")["net_profit_loss_percent"].agg(["count", "sum", "mean"])
    return out

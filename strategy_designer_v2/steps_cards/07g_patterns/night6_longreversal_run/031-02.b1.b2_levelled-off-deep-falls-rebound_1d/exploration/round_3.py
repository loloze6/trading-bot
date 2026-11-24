import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    def grid(h, L, volwin=60):
        recs = []
        for c in bars:
            fr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl)-h, h):
                    fr.append(cl[i+h]/cl[i]-1)
            fr = np.array(fr); drift = fr.mean(); sd = fr.std()
            for w, b in bars[c].items():
                cl = b["close"].values; ts = pd.to_datetime(b["timestamp"]).values
                lr = np.log(cl[1:]/cl[:-1])
                for i in range(0, len(cl)-h, h):
                    if i < max(L, volwin): continue
                    v = np.std(lr[i-volwin:i])
                    pz = np.log(cl[i]/cl[i-L])/(v*np.sqrt(L*1.0))
                    p7 = np.log(cl[i]/cl[i-7])/(v*np.sqrt(7.0))
                    recs.append((c, w, ts[i], pz, p7, cl[i+h]/cl[i]-1-drift, (cl[i+h]/cl[i]-1-drift)/sd, pd.Timestamp(ts[i]).year))
        return pd.DataFrame(recs, columns=["coin","win","ts","pz","p7","ex","z","yr"])
    def slope_cl(g, x, y):
        X = g[x]-g[x].mean(); b = (X*g[y]).sum()/(X**2).sum()
        e = g[y]-g[y].mean()-b*X
        s = (X*e).groupby(g.ts).sum()
        se = np.sqrt((s**2).sum())/(X**2).sum()
        return b, b/se, g.ts.nunique(), len(g)
    for h, L in [(7,30),(7,60),(7,90),(14,60),(30,90),(30,60)]:
        g = grid(h, L)
        b, t, nd, n = slope_cl(g, "pz", "ex")
        bc = g.groupby("coin").apply(lambda d: np.polyfit(d.pz, d.ex, 1)[0] if len(d) > 5 else np.nan)
        out[f"slope_past{L}_next{h}"] = pd.Series({"slope": b, "t_day_cl": t, "days": nd, "n": n,
            "coins_pos": (bc>0).sum(), "coins": bc.notna().sum(),
            "strength_hi_q": g[g.pz>=g.pz.quantile(.8)].z.mean(), "strength_lo_q": g[g.pz<=g.pz.quantile(.2)].z.mean()})
    # deep falls graded: within lowest-quintile 90d scaled return, does depth or 30d level matter for next 30 days
    g = grid(30, 90)
    deep = g[g.pz <= g.groupby("coin").pz.transform(lambda s: s.quantile(.2))].copy()
    deep["q"] = pd.qcut(deep.pz, 3, labels=False)
    out["deep90_next30"] = deep.groupby("q").agg(n=("ex","size"), pz=("pz","mean"), ex=("ex","mean"), z=("z","mean"))
    # momentum 30->7 controlled for last 7 days
    g = grid(7, 30)
    g["q7"] = pd.qcut(g.p7, 3, labels=False)
    g["q30"] = pd.qcut(g.pz, 3, labels=False)
    out["mom30_by_last7"] = g.pivot_table(index="q30", columns="q7", values="ex", aggfunc="mean")
    return out

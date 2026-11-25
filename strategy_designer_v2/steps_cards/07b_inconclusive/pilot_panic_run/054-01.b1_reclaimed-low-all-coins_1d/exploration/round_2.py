import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    H = (5,10,15,20)
    coinmean = {}
    for coin, wins in bars.items():
        cm = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c)-h, h):
                    rs.append(c[i+h]/c[i]-1)
            cm[h] = np.mean(rs) if rs else np.nan
        coinmean[coin] = cm
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            lo = df["low"]; cl = df["close"]; hi = df["high"]
            prior = lo.shift(1).rolling(30, min_periods=30).min()
            depth = (prior - lo) / prior
            pierce = (lo < prior) & (cl >= prior)
            reg = df["regime"].astype(str)
            n = len(df)
            seen = set()
            for i in np.where(pierce.values)[0]:
                inprof = reg.iloc[i] == "mean_reversion"
                key = (i//5, inprof)
                if key in seen: continue
                seen.add(key)
                r = {"coin": coin, "inprof": inprof, "depth": depth.iloc[i],
                     "closepos": (cl.iloc[i]-lo.iloc[i])/(hi.iloc[i]-lo.iloc[i]) if hi.iloc[i]>lo.iloc[i] else np.nan,
                     "reclaim": cl.iloc[i]/prior.iloc[i]-1,
                     "range": hi.iloc[i]/lo.iloc[i]-1,
                     "tr60": (cl.iloc[i]/cl.iloc[i-60]-1) if i>=60 else np.nan,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date())}
                for h in H:
                    r[f"x{h}"] = (cl.iloc[i+h]/cl.iloc[i]-1 - coinmean[coin][h]) if i+h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="x5"):
        g = g.dropna(subset=[col]); s = g[col]
        if len(s) < 3: return pd.Series({"n": len(s), "mean": s.mean()})
        gg = g.groupby("day")[col].apply(lambda v: (v - s.mean()).sum())
        G = len(gg); se = np.sqrt(G/(G-1)*(gg**2).sum())/len(s) if G>1 else np.nan
        return pd.Series({"n": len(s), "days": G, "mean": s.mean(), "t": s.mean()/se, "hit": (s>0).mean()})
    out = {}
    p = d[d.inprof].copy()
    out["inprof_by_h"] = pd.DataFrame({h: summ(p, f"x{h}") for h in H}).T
    q = d[~d.inprof].copy()
    q["trend"] = pd.cut(q["tr60"], [-10, -0.10, 0.10, 100], labels=["falling","choppy","rising"])
    out["outprof_by_trend_x5"] = q.groupby("trend").apply(summ)
    out["outprof_by_trend_x10"] = q.groupby("trend").apply(lambda g: summ(g, "x10"))
    out["inprof_corrs_x5"] = p[["depth","closepos","reclaim","range","x5"]].corr()["x5"]
    out["inprof_corrs_x10"] = p[["depth","closepos","reclaim","range","x10"]].corr()["x10"]
    p["rq"] = pd.qcut(p["reclaim"], 2, labels=["smallreclaim","bigreclaim"])
    out["inprof_by_reclaim"] = p.groupby("rq").apply(summ)
    p["dq"] = pd.qcut(p["depth"], 2, labels=["shallow","deep"])
    out["inprof_by_depth_x10"] = p.groupby("dq").apply(lambda g: summ(g, "x10"))
    return out

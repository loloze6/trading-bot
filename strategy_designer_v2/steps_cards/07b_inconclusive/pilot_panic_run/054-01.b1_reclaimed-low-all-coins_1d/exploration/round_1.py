import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allret = {h: [] for h in (1,3,5,10)}
    coinmean = {}
    for coin, wins in bars.items():
        cm = {}
        for h in (1,3,5,10):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c)-h, h):
                    rs.append(c[i+h]/c[i]-1)
            cm[h] = np.mean(rs) if rs else np.nan
        coinmean[coin] = cm
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            lo = df["low"]; cl = df["close"]; hi = df["high"]; op = df["open"]
            prior = lo.shift(1).rolling(30, min_periods=30).min()
            depth = (prior - lo) / prior
            pierce = (lo < prior) & (cl >= prior)
            reg = df["regime"].astype(str)
            n = len(df)
            seen = set()
            for i in np.where(pierce.values)[0]:
                cell = i // 5
                inprof = reg.iloc[i] == "mean_reversion"
                key = (cell, inprof)
                if key in seen: continue
                seen.add(key)
                r = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "inprof": inprof, "depth": depth.iloc[i],
                     "closepos": (cl.iloc[i]-lo.iloc[i])/(hi.iloc[i]-lo.iloc[i]) if hi.iloc[i]>lo.iloc[i] else np.nan,
                     "upday": cl.iloc[i] > op.iloc[i],
                     "reclaim": cl.iloc[i]/prior.iloc[i]-1,
                     "ret30": cl.iloc[i]/cl.iloc[max(0,i-30)]-1 if i>=30 else np.nan,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date())}
                for h in (1,3,5,10):
                    r[f"x{h}"] = (cl.iloc[i+h]/cl.iloc[i]-1 - coinmean[coin][h]) if i+h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="x5"):
        s = g[col].dropna()
        if len(s) < 3: return pd.Series({"n": len(s), "mean": s.mean(), "t": np.nan})
        gg = g.dropna(subset=[col]).groupby("day")[col].apply(lambda v: (v - s.mean()).sum())
        G = len(gg); se = np.sqrt(G/(G-1)*(gg**2).sum())/len(s) if G>1 else np.nan
        return pd.Series({"n": len(s), "days": G, "mean": s.mean(), "t": s.mean()/se if se else np.nan,
                          "hit": (s>0).mean()})
    out = {}
    out["by_profile_x5"] = d.groupby("inprof").apply(summ)
    p = d[d.inprof]
    out["inprof_by_h"] = pd.DataFrame({h: summ(p, f"x{h}") for h in (1,3,5,10)}).T
    out["outprof_by_h"] = pd.DataFrame({h: summ(d[~d.inprof], f"x{h}") for h in (1,3,5,10)}).T
    out["inprof_by_coin"] = p.groupby("coin").apply(summ)
    out["inprof_by_year"] = p.groupby("year").apply(summ)
    out["inprof_by_win"] = p.groupby("win").apply(summ)
    p = p.copy()
    p["dq"] = pd.qcut(p["depth"], 3, labels=["shallow","mid","deep"])
    out["inprof_by_depth"] = p.groupby("dq").apply(summ)
    p["cq"] = pd.qcut(p["closepos"], 3, labels=["lowclose","midclose","highclose"])
    out["inprof_by_closepos"] = p.groupby("cq").apply(summ)
    p["rq"] = pd.qcut(p["ret30"], 3, labels=["worst30","mid30","best30"])
    out["inprof_by_ret30"] = p.groupby("rq").apply(summ)
    out["inprof_by_upday"] = p.groupby("upday").apply(summ)
    out["corr_depth_x5"] = float(p[["depth","x5"]].dropna().corr().iloc[0,1])
    d2 = d.copy(); d2["dq"] = pd.qcut(d2["depth"],3,labels=["shallow","mid","deep"])
    out["all_by_depth"] = d2.groupby("dq").apply(summ)
    return out

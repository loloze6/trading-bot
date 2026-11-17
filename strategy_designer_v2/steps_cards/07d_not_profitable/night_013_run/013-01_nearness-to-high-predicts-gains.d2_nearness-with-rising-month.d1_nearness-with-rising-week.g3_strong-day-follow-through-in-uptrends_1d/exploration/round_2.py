def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []; fw = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            z = r/vol
            z7 = z.rolling(7, min_periods=5).mean()
            ret30 = cl/cl.shift(30)-1
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = cl.shift(-1)/cl-1
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            fsign = np.sign(b["forecast"])
            flip = (fsign != fsign.shift(1)) & (fsign != 0)
            rows.append(pd.DataFrame({"coin":c,"pos":pos,"g":pos*r1,"fee":fee,"reg":b["regime"],"fc":b["forecast"],"flip":flip}))
            idx = np.arange(0, len(b)-7, 7)
            fw.append(pd.DataFrame({"coin":c,"reg":b["regime"].values[idx],"fc":b["forecast"].values[idx],
                                    "z7":z7.values[idx],"r30":ret30.values[idx],"z":z.values[idx],
                                    "fr":cl.values[idx+7]/cl.values[idx]-1}))
    S = pd.concat(rows)
    T = S[S.reg=="trending"].copy()
    T["fcq"] = pd.qcut(T.fc.rank(method="first"),5,labels=False)
    out["trending per bar by fc quintile"] = T.groupby("fcq").agg(n=("g","size"),fc=("fc","mean"),pos=("pos","mean"),gain=("g","mean"),fee=("fee","mean"))
    out["sign flips per trending bar"] = float(T.flip.mean())
    out["fc lag1 autocorr trending"] = float(np.corrcoef(T.fc.values[1:], T.fc.values[:-1])[0,1])
    F = pd.concat(fw).dropna(subset=["fr"])
    F = F[F.reg=="trending"].copy()
    F["ex"] = F.fr - F.groupby("coin").fr.transform("mean")
    res = {}
    for col in ["fc","z","z7","r30"]:
        g = F.dropna(subset=[col])
        sl = stats.linregress(g[col], g.ex)
        res[col] = {"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr}
    out["h7 slope by predictor (trending grid)"] = pd.DataFrame(res).T
    g = F.dropna(subset=["z7"]).copy()
    g["q"] = pd.qcut(g.z7.rank(method="first"),5,labels=False)
    out["h7 by z7 quintile"] = g.groupby("q").agg(n=("fr","size"),z7=("z7","mean"),fr=("fr","mean"),ex=("ex","mean"))
    g = F.dropna(subset=["r30"]).copy()
    g["q"] = pd.qcut(g.r30.rank(method="first"),5,labels=False)
    out["h7 by r30 quintile"] = g.groupby("q").agg(n=("fr","size"),r30=("r30","mean"),fr=("fr","mean"),ex=("ex","mean"))
    out["share h7 fr>0 trending"] = float((F.fr>0).mean())
    return out

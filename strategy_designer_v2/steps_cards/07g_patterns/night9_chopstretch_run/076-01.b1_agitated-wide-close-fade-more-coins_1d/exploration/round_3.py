def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c - 1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l); mr = rng.rolling(20, min_periods=20).mean(); rm = rng / mr
            clv = ((c - l) / rng.replace(0, np.nan))
            r1 = c.shift(-1)/c - 1; r2 = c.shift(-2)/c - 1
            tr = c/c.shift(60) - 1
            d = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "rm": rm, "clv": clv, "u1": r1 - mu, "u2": r2 - 2*mu, "g2": (np.arange(len(b)) % 2 == 0),
                              "agit": (b["regime"] != "chop"), "trend": tr})
            rows.append(d)
    df = pd.concat(rows, ignore_index=True).dropna(subset=["rm","clv","trend"])
    def stat(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        s = g.groupby("day")[col].apply(lambda x: (x - g[col].mean()).sum())
        dd = len(s); se = np.sqrt((s**2).sum() * dd/(dd-1)) / len(g)
        return pd.Series({"n": len(g), "days": dd, "mean%": 100*g[col].mean(), "t_day": g[col].mean()/se})
    df["tb"] = pd.cut(df["trend"], [-9, -0.1, 0.1, 99], labels=["falling","choppy","rising"])
    out = {}
    cc = df[(~df.agit) & (df.tb == "choppy")].dropna(subset=["u1"]).copy()
    cc["push"] = cc.rm * cc.clv
    out["choppy calm: spearman u1 vs rm*clv, vs rm, vs clv"] = pd.Series({
        "rho push": stats.spearmanr(cc.push, cc.u1)[0], "p push": stats.spearmanr(cc.push, cc.u1)[1],
        "rho rm (clv>0.67)": stats.spearmanr(cc[cc.clv>0.67].rm, cc[cc.clv>0.67].u1)[0],
        "p rm (clv>0.67)": stats.spearmanr(cc[cc.clv>0.67].rm, cc[cc.clv>0.67].u1)[1], "n": len(cc)})
    cc["pq"] = pd.qcut(cc.push, 5, labels=False)
    out["choppy calm u1 by rm*clv quintile"] = cc.groupby("pq").apply(stat)
    hc = cc[cc.clv > 0.67].copy()
    hc["rmb"] = pd.cut(hc.rm, [0, 0.8, 1.2, 1.5, 99], labels=["<0.8","0.8-1.2","1.2-1.5",">1.5"])
    out["choppy calm high close by width"] = hc.groupby("rmb", observed=True).apply(stat)
    out["choppy calm wide high close by coin"] = cc[(cc.rm>=1.5)&(cc.clv>0.67)].groupby("coin")["u1"].agg(["count","mean"])
    g2 = cc[cc.g2]
    out["choppy calm u2 grid by push quintile"] = g2.assign(pq=pd.qcut(g2.push,5,labels=False)).groupby("pq").apply(lambda g: stat(g,"u2"))
    fa = df[(df.agit)&(df.tb=="falling")&(df.rm>=1.5)&(df.clv>0.67)].dropna(subset=["u1"])
    out["falling agitated wide high close by window"] = fa.groupby("win")["u1"].agg(["count","mean"])
    return out

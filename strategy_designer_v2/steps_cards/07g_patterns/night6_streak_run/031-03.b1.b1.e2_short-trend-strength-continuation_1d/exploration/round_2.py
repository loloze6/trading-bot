import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close"]].copy().reset_index(drop=True)
            c = d["close"]
            d["r1"] = c.pct_change()
            d["vol"] = d["r1"].rolling(60, min_periods=20).std()
            for p in [3,10,30,60]:
                d["sc%d"%p] = (c / c.shift(p) - 1) / (d["vol"] * np.sqrt(p))
            d["z1"] = d["r1"] / d["vol"]
            d["ddz"] = (c / c.rolling(60, min_periods=20).max() - 1) / d["vol"]
            d["fwd5"] = c.shift(-5) / c - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(d))
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    g = A[(A["pos"] % 5 == 0) & A["fwd5"].notna()].copy()
    drift = g.groupby("coin")["fwd5"].mean()
    usual = g.groupby("coin")["fwd5"].std()
    g["ex5"] = g["fwd5"] - g["coin"].map(drift)
    g["s5"] = g["ex5"] / g["coin"].map(usual)
    drift1 = A.groupby("coin")["fwd1"].mean()
    A["ex1"] = A["fwd1"] - A["coin"].map(drift1)

    def cmean(df, col):
        x = df.dropna(subset=[col])
        n = len(x); m = x[col].mean()
        e = (x[col] - m).groupby(x["day"]).sum()
        G = len(e)
        se = np.sqrt((e**2).sum() / n**2 * G / max(G-1,1))
        return pd.Series({"mean%": m*100, "t_day": m/se if se>0 else np.nan, "n": n, "days": G})

    def cslope(df, xcol, ycol):
        x = df.dropna(subset=[xcol, ycol])
        X = np.column_stack([np.ones(len(x)), x[xcol].values]); y = x[ycol].values
        b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        S = pd.DataFrame(X * e[:,None]).groupby(x["day"].values).sum().values
        G = S.shape[0]; n = len(x)
        V = XtXi @ (S.T @ S) @ XtXi * G/(G-1) * (n-1)/(n-2)
        return pd.Series({"slope": b[1], "t_day": b[1]/np.sqrt(V[1,1]), "n": n, "days": G})

    out = {}
    # per-coin sextiles of sc10 and sc30, day-clustered
    for f in ["sc10","sc30","ddz","sc60"]:
        gg = g.dropna(subset=[f]).copy()
        gg["b"] = gg.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 6, labels=False))
        out["ex5 by within-coin "+f+" sextile, day-clustered"] = gg.groupby("b").apply(lambda x: cmean(x, "ex5")).round(3)
    # graded slopes in each half
    res = {}
    for f in ["sc10","sc30","sc60","ddz","sc3"]:
        res[f+" all"] = cslope(g, f, "s5")
        res[f+" >0"] = cslope(g[g[f]>0], f, "s5")
        res[f+" <0"] = cslope(g[g[f]<0], f, "s5")
    out["slope of 5d strength on situation, day-clustered"] = pd.DataFrame(res).T.round(4)
    # per-coin sign of slope sc30 and sc10<0
    pc = {}
    for coin, x in g.groupby("coin"):
        x = x.dropna(subset=["sc30","sc10"])
        pc[coin] = {"corr sc30": x["sc30"].corr(x["s5"]),
                    "corr sc10|<0": x[x["sc10"]<0]["sc10"].corr(x[x["sc10"]<0]["s5"]),
                    "corr ddz": x["ddz"].corr(x["s5"]), "n": len(x)}
    pcd = pd.DataFrame(pc).T
    out["per-coin corr"] = pcd.round(3)
    out["coins positive"] = (pcd[["corr sc30","corr sc10|<0","corr ddz"]] > 0).sum()
    # daily reversal after daily shock, day-clustered
    aa = A.dropna(subset=["z1","ex1"]).copy()
    out["1d reversal slope ex1 on z1"] = cslope(aa, "z1", "ex1").round(5)
    aa["zb"] = pd.cut(aa["z1"], [-99,-1.5,-0.5,0.5,1.5,99])
    out["ex1 by z1, day-clustered"] = aa.groupby("zb").apply(lambda x: cmean(x, "ex1")).round(3)
    out["ex1 by weekday of next day, day-clustered"] = A.dropna(subset=["ex1"]).assign(wd2=(A["wd"]+1)%7).groupby("wd2").apply(lambda x: cmean(x, "ex1")).round(3)
    # 2-way: sc30 top tercile vs sc10 bottom
    gg = g.dropna(subset=["sc30","sc10"]).copy()
    gg["t30"] = gg.groupby("coin")["sc30"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    gg["t10"] = gg.groupby("coin")["sc10"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["ex5 by sc30 tercile x sc10 tercile"] = gg.groupby(["t30","t10"]).apply(lambda x: cmean(x,"ex5")).round(3)
    return out

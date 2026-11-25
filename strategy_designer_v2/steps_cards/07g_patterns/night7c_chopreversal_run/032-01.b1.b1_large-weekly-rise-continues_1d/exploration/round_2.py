import numpy as np, pandas as pd
from scipy import stats

def clu(g, col):
    m = g[col].mean(); k = len(g)
    dev = g.groupby("day")[col].apply(lambda x: (x - m).sum())
    D = len(dev)
    se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / k
    return pd.Series({"n": k, "days": D, "mean": m, "t_clu": m / se if se > 0 else np.nan})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n),
                               "z1": r1 / sd30.shift(1), "r1": r1, "sd30": sd30,
                               "fwd1": c.shift(-1) / c - 1, "fwd3": c.shift(-3) / c - 1,
                               "z7": (c / c.shift(7) - 1) / (sd30 * np.sqrt(7)),
                               "day": ts.dt.floor("D"), "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["z1", "fwd1"])
    dr1 = A.groupby("coin")["fwd1"].mean()
    A["u1"] = A["fwd1"] - A["coin"].map(dr1)
    out = {}
    A["z1bin"] = pd.cut(A["z1"], [-np.inf, -3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3, np.inf])
    out["u1 by z1 bin (clustered)"] = A.groupby("z1bin", observed=True).apply(lambda g: clu(g, "u1"))
    neg = A[A["z1"] < -1]
    out["u1 after z1<-1 by window"] = neg.groupby("win").apply(lambda g: clu(g, "u1"))
    out["u1 after z1<-1 by coin"] = neg.groupby("coin").apply(lambda g: clu(g, "u1"))
    r = stats.linregress(neg["z1"], neg["u1"])
    out["slope u1 on z1 among z1<-1"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(neg)})
    A["volt"] = A.groupby("coin")["sd30"].rank(pct=True)
    neg = A[A["z1"] < -1].copy()
    neg["volt"] = pd.cut(neg["volt"], [0, 1/3, 2/3, 1], labels=["low", "mid", "hi"])
    out["u1 after z1<-1 by vol tercile"] = neg.groupby("volt", observed=True).apply(lambda g: clu(g, "u1"))
    neg["trd"] = np.where(neg["z7"] > 0, "wk up", "wk down")
    out["u1 after z1<-1 by 7d sign"] = neg.groupby("trd").apply(lambda g: clu(g, "u1"))
    # 3-day horizon on non-overlapping grid of 3
    G3 = A[(A["pos"] % 3 == 0) & A["fwd3"].notna()].copy()
    G3["u3"] = G3["fwd3"] - G3["coin"].map(G3.groupby("coin")["fwd3"].mean())
    G3["z1bin"] = pd.cut(G3["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["u3 by z1 bin (grid 3)"] = G3.groupby("z1bin", observed=True).apply(lambda g: clu(g, "u3"))
    out["u1 by weekday (clustered)"] = A.groupby("wd").apply(lambda g: clu(g, "u1"))
    # book share of exposure on big down days
    out["share of drop days z1<-2 with long book"] = pd.Series({"share": (A.loc[A.z1 < -2, "alloc"] > 0).mean()})
    return out

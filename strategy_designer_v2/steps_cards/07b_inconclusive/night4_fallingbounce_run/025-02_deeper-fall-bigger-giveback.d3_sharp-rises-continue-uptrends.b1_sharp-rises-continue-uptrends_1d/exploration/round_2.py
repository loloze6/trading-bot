import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    drift = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl)-10, 10)
            rs.extend(cl[idx+10]/cl[idx]-1)
        drift[c] = np.mean(rs)
    F = []; A = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]; n = len(df)
            r1 = cl.pct_change(); z = r1 / r1.rolling(20).std()
            r90 = cl/cl.shift(90)-1
            up = np.where(r90.notna(), r90 > 0, df["regime"] == "trending")
            fwd = cl.shift(-10)/cl - 1 - drift[c]
            yr = pd.to_datetime(df["timestamp"]).dt.year
            f = df["forecast"].fillna(0)
            sig = (f > 0) & (f.diff() >= 2)
            d = pd.DataFrame({"f": f, "z": z, "fwd": fwd, "cell": np.arange(n)//10, "yr": yr})
            d2 = d[sig & fwd.notna()].groupby("cell").first().reset_index(); d2["coin"] = c
            F.append(d2)
            d3 = d[(d.z > 0) & d.fwd.notna() & up].groupby("cell").apply(lambda g: g.loc[g.z.idxmax()]).reset_index(drop=True)
            d3["coin"] = c
            A.append(d3)
    F = pd.concat(F); A = pd.concat(A)
    def agg(g):
        x = g["fwd"]; return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    F["zb"] = pd.cut(F.z, [-100,0,1,2,3,100], labels=["<=0","0-1","1-2","2-3",">3"])
    out["fc cases by raw z bucket"] = F.groupby("zb", observed=True).apply(agg)
    out["fc cases forecast mean by zb"] = F.groupby("zb", observed=True)["f"].mean()
    A["zb"] = pd.cut(A.z, [0,1,2,3,100], labels=["0-1","1-2","2-3",">3"])
    out["up regime, largest z per cell, by zb"] = A.groupby("zb", observed=True).apply(agg)
    out["up regime z>2 by year"] = A[A.z > 2].groupby("yr").apply(agg)
    x = A.dropna(subset=["z", "fwd"])
    out["corr z vs fwd up regime"] = float(np.corrcoef(x.z, x.fwd)[0, 1])
    out["n cells"] = len(x)
    return out

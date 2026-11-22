import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1,3,5,10,20]
    # coin drift per horizon on grid
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl)-h, h)
                rs.extend(cl[idx+h]/cl[idx]-1)
            drift[(c,h)] = np.mean(rs)
    rows = []
    fc_rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            r1 = cl.pct_change()
            z = r1 / r1.rolling(20).std()
            r90 = cl/cl.shift(90)-1
            up = np.where(r90.notna(), r90 > 0, df["regime"] == "trending")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in H:
                fwd = cl.shift(-h)/cl - 1 - drift[(c,h)]
                d = pd.DataFrame({"z": z, "up": up, "fwd": fwd, "cell": np.arange(n)//h, "yr": yr})
                d = d[(d.z > 0) & d.fwd.notna()]
                d["zb"] = pd.cut(d.z, [0,1,2,3,100], labels=["0-1","1-2","2-3",">3"])
                d = d.groupby(["up","zb","cell"], observed=True).first().reset_index()
                d["coin"] = c; d["h"] = h
                rows.append(d)
            # forecast cases
            f = df["forecast"].fillna(0)
            fwd10 = cl.shift(-10)/cl - 1 - drift[(c,10)]
            sig = (f > 0) & (f.diff() >= 2)
            d2 = pd.DataFrame({"f": f, "fwd": fwd10, "cell": np.arange(n)//10, "yr": yr, "z": z})[sig & fwd10.notna()]
            d2 = d2.groupby("cell").first().reset_index(); d2["coin"] = c; d2["w"] = w
            fc_rows.append(d2)
    A = pd.concat(rows); F = pd.concat(fc_rows)
    def agg(g):
        x = g["fwd"]; return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["h10 by regime x zbucket"] = A[A.h==10].groupby(["up","zb"], observed=True).apply(agg)
    out["z>2 by regime x horizon"] = A[A.z>2].groupby(["up","h"]).apply(agg)
    out["z>2 up h10 by coin"] = A[(A.z>2)&(A.h==10)&(A.up)].groupby("coin").apply(agg)
    out["fc cases by coin"] = F.groupby("coin").apply(agg)
    out["fc cases by year"] = F.groupby("yr").apply(agg)
    F["fq"] = pd.qcut(F.f.rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["fc cases by forecast quartile"] = F.groupby("fq", observed=True).apply(agg)
    out["fc cases all"] = agg(F)
    return out

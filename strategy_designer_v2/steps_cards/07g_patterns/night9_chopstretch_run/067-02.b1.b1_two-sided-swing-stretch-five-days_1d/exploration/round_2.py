import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r1.rolling(20).std()
            z = (c - sma) / sma / sd
            p60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30).std()
            f5 = c.shift(-5) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]), "z": z, "p60": p60, "sd30": sd30,
                "f5": f5, "chop": (b["regime"] == "unknown"),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    out["share chop bars"] = float(A["chop"].mean())
    # agitation proxy: sd30 rank within coin across all its windows
    A["agit"] = A.groupby("coin")["sd30"].rank(pct=True) > 0.5
    G = A[A["pos"] % 5 == 0].dropna(subset=["f5"]).copy()
    G["drift"] = G.groupby("coin")["f5"].transform("mean")
    G["ex5"] = G["f5"] - G["drift"]
    G["day"] = G["ts"].dt.floor("D")
    G["yr"] = G["ts"].dt.year
    def dayt(x):
        x = x.dropna(subset=["ex5"])
        s = x.groupby("day")["ex5"].sum(); n = len(x)
        m = x["ex5"].mean()
        se = np.sqrt(((s - s.index.map(x.groupby("day").size()) * m) ** 2).sum()) / n if n > 2 else np.nan
        return pd.Series({"n": n, "days": x["day"].nunique(), "mean": m, "t_day": m / se if se else np.nan})
    def slope(x, col="z"):
        x = x.dropna(subset=[col, "ex5"])
        if len(x) < 10: return pd.Series({"n": len(x)})
        X = x[col] - x[col].mean(); bta = (X * x["ex5"]).sum() / (X ** 2).sum()
        e = x["ex5"] - x["ex5"].mean() - bta * X
        g = (X * e).groupby(x["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(x), "slope": bta, "t": bta / se})
    C = G[G["chop"]].dropna(subset=["z"])
    N = G[~G["chop"]].dropna(subset=["z"])
    out["chop below avg: by z band"] = C[C.z < 0].groupby(pd.cut(C[C.z < 0]["z"], [-20, -2, -1, 0])).apply(dayt)
    out["chop above avg: by z band"] = C[C.z > 0].groupby(pd.cut(C[C.z > 0]["z"], [0, 1, 2, 20])).apply(dayt)
    out["chop slope below / above"] = pd.DataFrame({"below": slope(C[C.z < 0]), "above": slope(C[C.z > 0])})
    out["chop below avg z<-1 by year"] = C[C.z < -1].groupby("yr").apply(dayt)
    out["chop below avg z<-1 by coin"] = C[C.z < -1].groupby("coin").apply(dayt)
    out["chop z<-1 by agitation"] = C[C.z < -1].groupby("agit").apply(dayt)
    out["chop all by agitation"] = C.groupby("agit").apply(dayt)
    # trend side outside chop, using p60 where available
    N2 = N.dropna(subset=["p60"]).copy()
    N2["tr"] = np.where(N2.p60 > 0.10, "rising", np.where(N2.p60 < -0.10, "falling", "choppy60"))
    out["non-chop slope by trend"] = N2.groupby("tr").apply(slope)
    out["non-chop falling: z band"] = N2[N2.tr == "falling"].groupby(pd.cut(N2[N2.tr == "falling"]["z"], [-20, -2, -1, 0, 1, 2, 20])).apply(dayt)
    out["non-chop falling by agitation slope"] = N2[N2.tr == "falling"].groupby("agit").apply(slope)
    out["non-chop falling z<0 by year"] = N2[(N2.tr == "falling") & (N2.z < 0)].groupby("yr").apply(dayt)
    # forecast sign vs raw z sign on active bars
    act = A[A["chop"] & (A["fc"] != 0)].dropna(subset=["z"])
    out["fc sign vs z sign (active)"] = pd.crosstab(np.sign(act["fc"]), np.sign(act["z"]))
    out["chop excess by fc sign (grid)"] = C[C.fc != 0].groupby(np.sign(C[C.fc != 0]["fc"])).apply(dayt)
    return out

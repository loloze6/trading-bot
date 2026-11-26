import numpy as np, pandas as pd

def ct(y, day):
    y = np.asarray(y, float); m = y.mean()
    s = pd.Series(y - m).groupby(np.asarray(day)).sum()
    se = np.sqrt((s ** 2).sum()) / len(y)
    return m / se if se > 0 else np.nan

def slope(d, key, val="x5"):
    d = d.dropna(subset=[key, val])
    if len(d) < 10: return pd.Series({"n": len(d), "days": d.day.nunique(), "slope": np.nan, "t_day": np.nan})
    z = d[key] - d[key].mean(); y = d[val] - d[val].mean()
    b = (z * y).sum() / (z ** 2).sum(); e = y - b * z
    s = (z * e).groupby(d.day.values).sum()
    se = np.sqrt((s ** 2).sum()) / (z ** 2).sum()
    return pd.Series({"n": len(d), "days": d.day.nunique(), "slope": b, "t_day": b / se})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "r20": (c / c.shift(20) - 1) / (sd30 * np.sqrt(20)),
                "r10": (c / c.shift(10) - 1) / (sd30 * np.sqrt(10)),
                "s1": r1 / sd30,
                "r60": c / c.shift(60) - 1,
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1, "f1": c.shift(-1) / c - 1,
                "prof": (b["regime"] == "unknown"), "yr": ts.dt.year, "day": ts.dt.floor("D")}))
    A = pd.concat(rows, ignore_index=True)
    A["x1"] = A.f1 - A.coin.map(A.groupby("coin").f1.mean())
    A["tr"] = np.where(A.r60 > 0.10, "rising", np.where(A.r60 < -0.10, "falling", np.where(A.r60.notna(), "choppy", "na")))
    A["ag"] = np.where(A.prof, "calm", "agit")
    G = A[A.pos % 5 == 0].dropna(subset=["f5"]).copy()
    G["x5"] = G.f5 - G.coin.map(G.groupby("coin").f5.mean())
    G10 = A[A.pos % 10 == 0].dropna(subset=["f10"]).copy()
    G10["x10"] = G10.f10 - G10.coin.map(G10.groupby("coin").f10.mean())
    out = {}
    C = G[G.tr == "choppy"]
    out["choppy r20 slope by agitation"] = pd.DataFrame({a: slope(C[C.ag == a], "r20") for a in ["calm", "agit"]}).T.round(4)
    out["choppy r10 slope by agitation"] = pd.DataFrame({a: slope(C[C.ag == a], "r10") for a in ["calm", "agit"]}).T.round(4)
    out["choppy r20 slope by year"] = pd.DataFrame({y: slope(C[C.yr == y], "r20") for y in sorted(C.yr.unique())}).T.round(4)
    out["choppy r20 slope by window"] = pd.DataFrame({w: slope(C[C.w == w], "r20") for w in sorted(C.w.unique())}).T.round(4)
    out["choppy r20<0 slope / r20>0 slope"] = pd.DataFrame({"neg": slope(C[C.r20 < 0], "r20"), "pos": slope(C[C.r20 > 0], "r20")}).T.round(4)
    d = C.dropna(subset=["r20"]).copy(); d["b"] = pd.qcut(d.r20, 4, labels=False)
    out["choppy r20 quartile x5"] = d.groupby("b").apply(lambda g: pd.Series({"n": len(g), "days": g.day.nunique(), "r20": g.r20.mean(), "x5": g.x5.mean(), "t_day": ct(g.x5, g.day)})).round(4)
    C10 = G10[G10.tr == "choppy"]
    out["choppy r20 slope 10d"] = slope(C10, "r20", "x10").round(4)
    out["choppy r20 slope by coin"] = pd.DataFrame({k: slope(C[C.coin == k], "r20") for k in sorted(C.coin.unique())}).T.round(4)
    A1 = A.dropna(subset=["s1", "x1"])
    out["s1 slope next day by trend (all bars)"] = pd.DataFrame({t: slope(A1[A1.tr == t], "s1", "x1") for t in ["rising", "choppy", "falling", "na"]}).T.round(4)
    out["s1 slope next day by agitation"] = pd.DataFrame({a: slope(A1[A1.ag == a], "s1", "x1") for a in ["calm", "agit"]}).T.round(4)
    return out

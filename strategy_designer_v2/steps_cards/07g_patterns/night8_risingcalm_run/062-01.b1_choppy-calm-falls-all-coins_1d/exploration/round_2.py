import numpy as np, pandas as pd
from scipy import stats

def ct(y, day):
    # t of mean with cases of one day pooled (deviations summed per day)
    y = np.asarray(y, float); m = y.mean()
    s = pd.Series(y - m).groupby(np.asarray(day)).sum()
    se = np.sqrt((s ** 2).sum()) / len(y)
    return m / se if se > 0 else np.nan

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "s5": (c / c.shift(5) - 1) / (sd30 * np.sqrt(5)),
                "r20": (c / c.shift(20) - 1) / (sd30 * np.sqrt(20)),
                "r60": c / c.shift(60) - 1,
                "vr": sd30.rolling(60, min_periods=30).rank(pct=True),
                "vchg": sd30 / sd30.shift(20) - 1,
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                "prof": (b["regime"] == "unknown"), "yr": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.pos % 5 == 0].dropna(subset=["f5"]).copy()
    G["x5"] = G["f5"] - G["coin"].map(G.groupby("coin")["f5"].mean())
    G["tr"] = np.where(G.r60 > 0.10, "rising", np.where(G.r60 < -0.10, "falling", np.where(G.r60.notna(), "choppy", "na")))
    out = {}
    def qt(d, key, q=5):
        d = d.dropna(subset=[key, "x5"]).copy()
        d["b"] = pd.qcut(d[key], q, labels=False, duplicates="drop")
        r = d.groupby("b").apply(lambda g: pd.Series({"n": len(g), "days": g.day.nunique(), "key": g[key].mean(),
                                 "x5": g.x5.mean(), "t_day": ct(g.x5, g.day)}))
        return r.round(4)
    def slope(d, key):
        d = d.dropna(subset=[key, "x5"])
        z = (d[key] - d[key].mean()); y = d.x5 - d.x5.mean()
        b = (z * y).sum() / (z ** 2).sum()
        e = y - b * z
        s = (z * e).groupby(d.day.values).sum()
        se = np.sqrt((s ** 2).sum()) / (z ** 2).sum()
        return pd.Series({"n": len(d), "slope": b, "t_day": b / se})
    out["vr quint, cluster t"] = qt(G, "vr")
    out["vchg quint, cluster t"] = qt(G, "vchg")
    out["r20 quint, cluster t"] = qt(G, "r20")
    out["slopes all"] = pd.DataFrame({k: slope(G, k) for k in ["s5", "r20", "vr", "vchg"]}).T.round(4)
    out["r20 slope by trend"] = pd.DataFrame({t: slope(G[G.tr == t], "r20") for t in ["rising", "choppy", "falling", "na"]}).T.round(4)
    out["vr slope by trend"] = pd.DataFrame({t: slope(G[G.tr == t], "vr") for t in ["rising", "choppy", "falling", "na"]}).T.round(4)
    out["r20 slope by year"] = pd.DataFrame({y: slope(G[G.yr == y], "r20") for y in sorted(G.yr.unique())}).T.round(4)
    out["vr slope by year"] = pd.DataFrame({y: slope(G[G.yr == y], "vr") for y in sorted(G.yr.unique())}).T.round(4)
    out["vr top quint x5 by trend"] = G[G.vr >= G.vr.quantile(0.8)].groupby("tr").apply(
        lambda g: pd.Series({"n": len(g), "x5": g.x5.mean(), "t_day": ct(g.x5, g.day)})).round(4)
    P = G[G.prof]
    out["in profile s5 slope"] = slope(P, "s5").round(4)
    out["in profile s5<0 slope by year"] = pd.DataFrame({y: slope(P[(P.yr == y) & (P.s5 < 0)], "s5") for y in sorted(P.yr.unique())}).T.round(4)
    out["in profile s5 bottom tercile by coin"] = P[P.s5 <= P.s5.quantile(1/3)].groupby("coin").x5.agg(["count", "mean"]).round(4)
    return out

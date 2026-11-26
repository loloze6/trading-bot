def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            df["active"] = (b["regime"] != "chop").values
            df["r30"] = c / c.shift(30) - 1
            df["r60"] = c / c.shift(60) - 1
            df["vol30"] = r1.rolling(30).std()
            df["z30"] = df["r30"] / (df["vol30"] * np.sqrt(30))
            df["z1"] = r1 / r1.rolling(30).std().shift(1)
            df["volrat"] = v.rolling(10).mean() / v.rolling(60).mean()
            df["v1"] = v / v.rolling(30).mean().shift(1)
            df["f5"] = c.shift(-5) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            df["f2"] = c.shift(-2) / c - 1
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.pos % 5 == 0].groupby("coin")["f5"].mean()
    A["x5"] = A["f5"] - A["coin"].map(drift5)
    A["x1"] = A["f1"] - A["coin"].map(A.groupby("coin")["f1"].mean())
    A["x2"] = A["f2"] - A["coin"].map(A[A.pos % 2 == 0].groupby("coin")["f2"].mean())
    A["trend"] = pd.cut(A["r60"], [-9, -0.10, 0.10, 99], labels=["falling", "choppy", "rising"])
    def dp(g, col):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 5: return pd.Series({"n": n, "days": g.day.nunique(), "mean": np.nan, "t_day": np.nan})
        m = g[col].mean(); s = (g[col] - m).groupby(g["day"]).sum()
        D = len(s); se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean": m, "t_day": m / se})
    out = {}
    G = A[A.pos % 5 == 0].dropna(subset=["x5", "z30"])
    G["zq"] = pd.qcut(G["z30"], 5, labels=False)
    out["x5 by z30 quintile, day-pooled"] = G.groupby("zq").apply(lambda g: dp(g, "x5"))
    F = G[G.z30 < 0].dropna(subset=["volrat"])
    F["vt"] = pd.qcut(F["volrat"], 3, labels=["quiet", "mid", "heavy"])
    out["falls x5 by volume tercile, day-pooled"] = F.groupby("vt").apply(lambda g: dp(g, "x5"))
    Ft = F.dropna(subset=["trend"])
    out["falls x5 by trend x volume"] = Ft.groupby(["trend", "vt"]).apply(lambda g: dp(g, "x5"))
    F["deep"] = pd.qcut(F["z30"], 2, labels=["deep", "shallow"])
    out["falls x5 by depth x volume"] = F.groupby(["deep", "vt"]).apply(lambda g: dp(g, "x5"))
    out["falls x5 quiet vs heavy by window half"] = F[F.vt != "mid"].assign(h=F.win.isin(["w7","w8","w9","w10","w11","w12"]).map({True: "B", False: "C"})).groupby(["h", "vt"]).apply(lambda g: dp(g, "x5"))
    D = A.dropna(subset=["x1", "z1"]).copy()
    D["z1b"] = pd.cut(D["z1"], [-99, -2.5, -1.5, 1.5, 99])
    out["next day x1 by z1, day-pooled"] = D.groupby("z1b").apply(lambda g: dp(g, "x1"))
    S = D[D.z1 <= -1.5].copy()
    S["vb"] = pd.qcut(S["v1"], 2, labels=["lighter", "heavier"])
    out["after sharp down day: x1 by day's volume"] = S.groupby("vb").apply(lambda g: dp(g, "x1"))
    out["after sharp down day: x1 by trend"] = S.dropna(subset=["trend"]).groupby("trend").apply(lambda g: dp(g, "x1"))
    Sg = A[(A.pos % 2 == 0) & (A.z1 <= -1.5)]
    out["after sharp down day: x2 grid2"] = dp(Sg, "x2").to_frame().T
    out["weekday x1 day-pooled"] = A.dropna(subset=["x1"]).assign(nwd=lambda d: (d.wd + 1) % 7).groupby("nwd").apply(lambda g: dp(g, "x1"))
    out["weekday by half"] = A.dropna(subset=["x1"]).assign(nwd=lambda d: (d.wd + 1) % 7, h=lambda d: d.win.isin(["w7","w8","w9","w10","w11","w12"]).map({True: "B", False: "C"})).query("nwd in [3,5]").groupby(["nwd", "h"]).apply(lambda g: dp(g, "x1"))
    return out

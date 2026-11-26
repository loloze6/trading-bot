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
            sd30 = r1.rolling(30).std()
            df["z30"] = df["r30"] / (sd30 * np.sqrt(30))
            df["agit"] = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            df["z1"] = r1 / sd30.shift(1)
            df["v1"] = v / v.rolling(30).mean().shift(1)
            df["volrat"] = v.rolling(10).mean() / v.rolling(60).mean()
            df["f5"] = c.shift(-5) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["x5"] = A["f5"] - A["coin"].map(A[A.pos % 5 == 0].groupby("coin")["f5"].mean())
    A["x1"] = A["f1"] - A["coin"].map(A.groupby("coin")["f1"].mean())
    A["trend"] = pd.cut(A["r60"], [-9, -0.10, 0.10, 99], labels=["falling", "choppy", "rising"])
    A["ag"] = np.where(A["agit"].isna(), "na", np.where(A["agit"] > 0.5, "agitated", "calm"))
    A["half"] = A.win.isin(["w7","w8","w9","w10","w11","w12"]).map({True: "B", False: "C"})
    def dp(g, col):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 5: return pd.Series({"n": n, "days": g.day.nunique(), "mean": np.nan, "t_day": np.nan})
        m = g[col].mean(); s = (g[col] - m).groupby(g["day"]).sum()
        D = len(s); se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean": m, "t_day": m / se})
    out = {}
    G = A[(A.pos % 5 == 0)].dropna(subset=["x5", "z30", "trend"])
    F = G[G.z30 < 0]
    out["falls x5 by trend x agitation"] = F[F.ag != "na"].groupby(["trend", "ag"]).apply(lambda g: dp(g, "x5"))
    Fc = F[F.trend == "choppy"].copy()
    Fc["dq"] = pd.qcut(Fc["z30"], 2, labels=["deep", "shallow"])
    out["choppy falls x5 by depth"] = Fc.groupby("dq").apply(lambda g: dp(g, "x5"))
    out["choppy falls x5 by half"] = Fc.groupby("half").apply(lambda g: dp(g, "x5"))
    out["choppy rises x5"] = G[(G.trend == "choppy") & (G.z30 > 0)].groupby("half").apply(lambda g: dp(g, "x5"))
    Fc2 = F[(F.trend == "falling") & (F.ag == "calm")].dropna(subset=["volrat"]).copy()
    Fc2["dq"] = pd.qcut(Fc2["z30"], 2, labels=["deep", "shallow"])
    Fc2["vt"] = pd.qcut(Fc2["volrat"], 2, labels=["quiet", "heavy"])
    out["falling calm falls: depth x volume"] = Fc2.groupby(["dq", "vt"]).apply(lambda g: dp(g, "x5"))
    S = A.dropna(subset=["x1", "z1", "v1"])
    S = S[S.z1 <= -1.5].copy()
    S["vb"] = pd.qcut(S["v1"], 2, labels=["lighter", "heavier"])
    out["sharp down day x1: volume by half"] = S.groupby(["half", "vb"]).apply(lambda g: dp(g, "x1"))
    out["sharp down day x1: volume by agitation"] = S[S.ag != "na"].groupby(["ag", "vb"]).apply(lambda g: dp(g, "x1"))
    S["vq"] = pd.qcut(S["v1"], 4, labels=False)
    out["sharp down day x1 by volume quartile"] = S.groupby("vq").apply(lambda g: dp(g, "x1"))
    return out

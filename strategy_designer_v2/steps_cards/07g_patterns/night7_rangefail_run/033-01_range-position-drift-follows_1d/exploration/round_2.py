def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi20 = c.rolling(20, min_periods=20).max(); lo20 = c.rolling(20, min_periods=20).min()
            pos = (c - lo20) / (hi20 - lo20)
            prevhi = c.shift(1).rolling(20, min_periods=20).max()
            brk = c / prevhi - 1
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=25).std()
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)), "pos": pos, "brk": brk,
                "vol30": vol30, "r60": r60, "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year}))
    A = pd.concat(rows, ignore_index=True)
    A["volrk"] = A.groupby("coin")["vol30"].rank(pct=True)
    G = A[(A["i"] % H == 0) & A["fwd"].notna()].copy()
    G["ex"] = G["fwd"] - G["coin"].map(G.groupby("coin")["fwd"].mean())
    G = G.dropna(subset=["pos"])
    def slope(g, x="pos"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 30: return pd.Series({"n": len(g)})
        s = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out = {}
    Gv = G.dropna(subset=["volrk"]).copy()
    Gv["calm"] = np.where(Gv["volrk"] <= 0.5, "calm", "agit")
    out["slope by calm/agit (30d vol vs coin median)"] = Gv.groupby("calm").apply(slope).round(4)
    out["slope by calm/agit x year"] = Gv.groupby(["calm", "yr"]).apply(slope).round(4)
    out["slope by calm/agit x coin"] = Gv.groupby(["calm", "coin"]).apply(slope).round(4)
    Gv["vt"] = pd.qcut(Gv["volrk"], 4, labels=["q1", "q2", "q3", "q4"])
    out["slope by vol quartile"] = Gv.groupby("vt", observed=True).apply(slope).round(4)
    # standardized-in-vol version: ex/vol
    Gt = G.dropna(subset=["r60"]).copy()
    Gt["tr"] = pd.cut(Gt["r60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["slope by 60d trend"] = Gt.groupby("tr", observed=True).apply(slope).round(4)
    # breakout distance above prior 20d high
    Gb = G.dropna(subset=["brk"]).copy()
    Gb = Gb[Gb["brk"] > 0]
    out["breakout cases: n, mean ex, t"] = pd.Series({"n": len(Gb), "mean": Gb["ex"].mean(),
        "t": Gb["ex"].mean() / (Gb["ex"].std() / np.sqrt(len(Gb)))}).round(4)
    out["breakout ex by year"] = Gb.groupby("yr")["ex"].agg(["count", "mean"]).round(4)
    out["slope ex~breakout size"] = slope(Gb, "brk").round(4)
    # weekday next-day by year
    A1 = A.dropna(subset=["fwd1"]).copy()
    A1["ex"] = A1["fwd1"] - A1["coin"].map(A1.groupby("coin")["fwd1"].mean())
    A1["thfr"] = np.where(A1["wd"].isin([3, 4]), "thu-fri", "other")
    t = A1.groupby(["yr", "thfr"])["ex"].mean().unstack().round(4)
    out["next1d ex thu-fri vs other by year"] = t
    # book gain calm vs agitated per bar
    A1["gain"] = A1["alloc"] * A1["fwd1"]
    A1["calm"] = np.where(A1["volrk"] <= 0.5, "calm", "agit")
    out["book gain per bar calm/agit"] = A1.dropna(subset=["volrk"]).groupby("calm")["gain"].agg(["count", "mean", "std"]).round(5)
    return out

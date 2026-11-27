def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=20).std()
            d["z"] = r / sd20
            for h in [1, 3, 5]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["ret5"] = c / c.shift(5) - 1
            d["ret5z"] = d["ret5"] / (sd20 * np.sqrt(5))
            d["ret20"] = c / c.shift(20) - 1
            d["clpos"] = (c - d["low"]) / (d["high"] - d["low"])
            d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(len(d))
            ts = pd.to_datetime(d["timestamp"])
            d["day"] = ts.dt.floor("D"); d["yr"] = ts.dt.year; d["wd"] = ts.dt.weekday
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 3, 5]:
        dr = A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    def ct(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "days": 0, "mean": np.nan, "t_day": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": m, "t_day": m / se})
    def grid(df, h): return df[df["pos"] % h == 0]
    out = {}
    # 1 profile overall drift
    out["profile overall"] = pd.DataFrame({f"in u{h}": ct(grid(A[A.inprof], h), f"u{h}") for h in [1,3,5]} |
                                          {f"out u{h}": ct(grid(A[~A.inprof], h), f"u{h}") for h in [1,3,5]}).T.round(5)
    # 2 big rise in profile minus other in-profile bars
    P = grid(A[A.inprof], 1).dropna(subset=["z","u1"])
    out["in profile z>=1 vs rest, u1"] = pd.DataFrame({"z>=1": ct(P[P.z>=1], "u1"), "z<1": ct(P[P.z<1], "u1"), "0<=z<1": ct(P[(P.z>=0)&(P.z<1)], "u1")}).T.round(5)
    # 3 big down day rebound out of profile, by year and graded
    O = grid(A[~A.inprof], 1).dropna(subset=["z","u1"])
    out["out prof z<=-1 by year u1"] = O[O.z<=-1].groupby("yr").apply(lambda g: ct(g,"u1")).round(5)
    # 4 ret5 momentum, scaled, in/out profile, by year
    for h in [3,5]:
        G = grid(A, h).dropna(subset=["ret5z", f"u{h}"]).copy()
        G["q"] = pd.qcut(G["ret5z"], 5, labels=False)
        out[f"ret5z quintile u{h} day-t"] = G.groupby("q").apply(lambda g: ct(g, f"u{h}")).round(5)
        G["sgn"] = np.sign(G["ret5z"])
        G["mom"] = G[f"u{h}"] * G["sgn"]
        out[f"momentum signed u{h} by year"] = G.groupby("yr").apply(lambda g: ct(g, "mom")).round(5)
        out[f"momentum signed u{h} in/out"] = G.groupby("inprof").apply(lambda g: ct(g, "mom")).round(5)
        out[f"bottom quintile u{h} by year"] = G[G.q==0].groupby("yr").apply(lambda g: ct(g, f"u{h}")).round(5)
        out[f"top quintile u{h} by year"] = G[G.q==4].groupby("yr").apply(lambda g: ct(g, f"u{h}")).round(5)
    # 5 close position by year
    C = grid(A,1).dropna(subset=["clpos","u1"]).copy()
    C["q"] = pd.qcut(C["clpos"], 5, labels=False)
    out["low close q0 by year"] = C[C.q==0].groupby("yr").apply(lambda g: ct(g,"u1")).round(5)
    out["weekday thu-fri minus wed by year"] = C.groupby("yr").apply(lambda g: pd.Series({
        "thufri": g[g.wd.isin([3,4])]["u1"].mean(), "wed": g[g.wd==2]["u1"].mean()})).round(5)
    return out

def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w, "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(df["timestamp"]).dt.year,
                "fwd5": c.shift(-5)/c - 1, "fwd1": c.shift(-1)/c - 1, "r1": r1,
                "r30": c/c.shift(30) - 1, "r60": c/c.shift(60) - 1,
                "vol30": r1.rolling(30).std(),
                "pos30": (c - c.rolling(30).min())/(c.rolling(30).max()-c.rolling(30).min()),
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday, "pos": df.index})
            f["r1z"] = f["r1"]/f["vol30"]
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    d5 = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    d1 = A.groupby("coin")["fwd1"].mean()
    A["adj5"] = A["fwd5"] - A["coin"].map(d5); A["adj1"] = A["fwd1"] - A["coin"].map(d1)
    A["agit"] = A["vol30"] > A.groupby("coin")["vol30"].transform("median")
    A["trend"] = pd.cut(A["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["fall", "chop", "rise"])
    G = A[A.pos % 5 == 0].dropna(subset=["adj5"])
    def cl(g, col="adj5"):
        g = g.dropna(subset=[col]); dm = g.groupby("day")[col].sum()
        n = len(g); nd = len(dm)
        m = g[col].mean()
        se = np.sqrt(((g.groupby("day")[col].apply(lambda x: (x - m).sum()))**2).sum())/n if n > 1 else np.nan
        return pd.Series({"n": n, "days": nd, "mean%": 100*m, "t_cl": m/se if se else np.nan})
    out = {}
    G["pq"] = pd.cut(G["pos30"], [-0.01, 0.1, 0.35, 0.65, 0.9, 1.01], labels=False)
    out["pos30_cl"] = G.groupby("pq").apply(cl)
    out["pos30_by_trend"] = G.groupby(["trend", "pq"]).apply(cl)
    out["pos30_low_by_agit_fall"] = G[G.trend == "fall"].groupby(["agit", "pq"]).apply(cl)
    out["pos30_mid_low_by_year"] = G[G.pq == 1].groupby("year").apply(cl)
    G["rq"] = pd.qcut(G["r30"].rank(method="first"), 5, labels=False)
    out["r30_cl"] = G.groupby("rq").apply(cl)
    out["r30_by_trend"] = G.groupby(["trend", "rq"]).apply(cl)
    D = A.dropna(subset=["adj1", "r1z"]).copy()
    D["zq"] = pd.cut(D["r1z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf], labels=False)
    out["r1z_next1_cl"] = D.groupby("zq").apply(lambda g: cl(g, "adj1"))
    D["rq"] = pd.qcut(D["r1"].rank(method="first"), 10, labels=False)
    out["r1dec_next1_cl"] = D.groupby("rq").apply(lambda g: cl(g, "adj1"))
    out["r1dec3_by_year"] = D[D.rq == 3].groupby("year").apply(lambda g: cl(g, "adj1"))
    out["weekday_cl"] = D.groupby("wd").apply(lambda g: cl(g, "adj1"))
    out["weekday_by_year_wed"] = D[D.wd == 2].groupby("year").apply(lambda g: cl(g, "adj1"))
    return out

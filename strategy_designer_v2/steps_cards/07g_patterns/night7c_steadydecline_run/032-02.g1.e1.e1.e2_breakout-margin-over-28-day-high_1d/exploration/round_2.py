def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            df["pos"] = np.arange(len(b))
            phi = c.shift(1).rolling(28).max(); plo = c.shift(1).rolling(28).min()
            df["dist_hi"] = c / phi - 1
            df["stoch"] = (c - plo) / (phi - plo)
            df["ret28"] = c / c.shift(28) - 1
            df["vr"] = r1.rolling(7).std() / r1.rolling(42).std()
            rng = (h - l) / c
            df["rr"] = rng.rolling(7).mean() / rng.rolling(42).mean()
            df["vl"] = v.rolling(7).mean() / v.rolling(42).mean()
            df["fwd5"] = c.shift(-5) / c - 1
            df["fwd1"] = c.shift(-1) / c - 1
            df["grid"] = df["pos"] % 5 == 0
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D"); D["year"] = D["ts"].dt.year
    G = D[D["grid"] & D["fwd5"].notna()].copy()
    drift = G.groupby("coin")["fwd5"].mean(); sd = G.groupby("coin")["fwd5"].std()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift); G["z5"] = G["ex5"] / G["coin"].map(sd)
    def mt(S, y="ex5"):
        S = S[[y, "day"]].dropna()
        if len(S) < 3: return pd.Series({"mean": np.nan, "t_day": np.nan, "n": len(S), "days": 0})
        m = S[y].mean(); dd = (S[y] - m).groupby(S["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / len(S)
        return pd.Series({"mean": m, "t_day": m / se, "n": len(S), "days": S["day"].nunique()})
    def sl(S, x):
        S = S[[x, "z5", "day"]].dropna().copy()
        S["xs"] = (S[x] - S[x].mean()) / S[x].std()
        b = (S["xs"] * S["z5"]).sum() / (S["xs"] ** 2).sum()
        dd = (S["xs"] * (S["z5"] - S["z5"].mean() - b * S["xs"])).groupby(S["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / (S["xs"] ** 2).sum()
        return pd.Series({"slope": b, "t_day": b / se, "n": len(S), "days": S["day"].nunique()})
    out = {}
    bo = G[G["dist_hi"] > 0]
    out["breakout_all"] = mt(bo)
    out["breakout_by_year"] = bo.groupby("year").apply(mt)
    out["breakout_by_coin"] = bo.groupby("coin").apply(mt)
    out["breakout_by_win"] = bo.groupby("win").apply(mt)
    G["dbin"] = pd.cut(G["dist_hi"], [-1, -0.4, -0.25, -0.15, -0.08, -0.03, 0, 1])
    out["dist_hi_bins"] = G.groupby("dbin", observed=True).apply(mt)
    G["sbin"] = pd.cut(G["stoch"], [-0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 10])
    out["stoch_bins"] = G.groupby("sbin", observed=True).apply(mt)
    out["slopes"] = pd.DataFrame({x: sl(G, x) for x in ["vr", "rr", "vl", "stoch", "dist_hi"]}).T
    for x in ["vr", "rr", "vl"]:
        S = G.dropna(subset=[x]).copy()
        S["q"] = pd.qcut(S[x], 5, labels=[f"q{i}" for i in range(1, 6)])
        out["quint_" + x] = S.groupby("q", observed=True).apply(mt)
    S = G.dropna(subset=["vr"]).copy(); S["lo"] = S["vr"] < S["vr"].median()
    out["vr_low_by_year"] = S[S["lo"]].groupby("year").apply(mt)
    # weekday, day-clustered
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    D["wd"] = (D["ts"] + pd.Timedelta(days=1)).dt.dayofweek
    out["weekday_day_clustered"] = D.groupby("wd").apply(lambda s: mt(s, "ex1"))
    E = D[D["wd"].isin([4, 5])]
    out["fri_sat_by_year"] = E.groupby("year").apply(lambda s: mt(s, "ex1"))
    out["fri_sat_by_coin"] = E.groupby("coin").apply(lambda s: mt(s, "ex1"))
    return out

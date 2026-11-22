def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            ma = r1.abs().rolling(720, min_periods=120).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            d = pd.DataFrame({"coin": coin, "w": w, "r1": r1, "s": r1 / ma,
                              "vr": v / v.rolling(720, min_periods=120).mean(),
                              "hour": ts.dt.hour, "year": ts.dt.year, "ma": ma,
                              "pos": np.arange(len(b))})
            d["n2"] = c.shift(-2) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            d["n6"] = c.shift(-6) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    def st(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    # evening: trailing 30-day mean of the coin's own evening 2h return (known at bar 20 close: uses previous days only)
    E = D[D["hour"] == 20].copy()
    E["trail"] = E.groupby(["coin", "w"])["n2"].transform(lambda x: x.shift(1).rolling(30, min_periods=15).mean())
    E["tq"] = pd.qcut(E["trail"], 5, labels=False, duplicates="drop")
    out["eve2h_by_trailing30d_eve_quint"] = E.groupby("tq")["n2"].apply(st).unstack().round(2)
    E["vq"] = pd.qcut(E["ma"], 5, labels=False, duplicates="drop")
    out["eve2h_by_vol_level_quint"] = E.groupby("vq")["n2"].apply(st).unstack().round(2)
    E["n2s"] = E["n2"] / (E["ma"] * np.sqrt(2))
    out["eve2h_strength_by_coin"] = E.groupby("coin")["n2s"].apply(st).unstack().round(3)
    E["vr20q"] = pd.qcut(E["vr"], 5, labels=False, duplicates="drop")
    out["eve2h_by_hour20_volume_quint"] = E.groupby("vr20q")["n2"].apply(st).unstack().round(2)
    # falls x volume: graded score, per coin, by year, horizons
    G = D[(D["pos"] % 3 == 0) & (D["s"] < -1.5)].copy()
    G["score"] = (-G["s"]) * np.log1p(G["vr"])
    G["scq"] = pd.qcut(G["score"], 5, labels=False, duplicates="drop")
    out["fall_fwd3_by_depth_x_logvol_quint"] = G.groupby("scq")["n3"].apply(st).unstack().round(2)
    G["vq"] = pd.qcut(G["vr"], 3, labels=False, duplicates="drop")
    out["fall_fwd3_by_coin_voltercile"] = G.groupby(["coin", "vq"])["n3"].apply(st).unstack().round(2)
    G6 = D[(D["pos"] % 6 == 0) & (D["s"] < -1.5)].copy()
    G6["vq"] = pd.qcut(G6["vr"], 3, labels=False, duplicates="drop")
    out["fall_fwd6_by_voltercile"] = G6.groupby("vq")["n6"].apply(st).unstack().round(2)
    hi = G[G["vq"] == 2]
    out["fall_hivol_fwd3_by_year"] = hi.groupby("year")["n3"].apply(st).unstack().round(2)
    out["fall_corr_logvr_n3"] = pd.Series({"corr": G[["vr", "n3"]].assign(vr=np.log(G["vr"])).dropna().corr().iloc[0, 1], "n": G["n3"].notna().sum()})
    return out

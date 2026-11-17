def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            vr = v / v.rolling(20).mean()
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            near = c / c.rolling(30).max()
            vol20 = r1.rolling(20).std()
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (df["high"] - df["low"]) / c
            pos = np.arange(len(df))
            d = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "r1": r1, "vr": vr, "ret30": ret30,
                              "ret7": ret7, "near": near, "vol20": vol20, "fwd3": fwd3, "fwd1": fwd1,
                              "rng": rng, "fc": df["forecast"], "alloc": df["postRebalance_current_allocation"],
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                              "yr": pd.to_datetime(df["timestamp"]).dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["fwd3d"] = A["fwd3"] - A.groupby("coin")["fwd3"].transform(lambda s: s[A.loc[s.index, "pos"] % 3 == 0].mean())
    G = A[(A.pos % 3 == 0)].dropna(subset=["fwd3d"])
    out = {}
    def tab(df, key, q=5):
        d = df.dropna(subset=[key]).copy()
        d["b"] = d.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("b")["fwd3d"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.drop(columns="std")
    def slope(df, key):
        d = df.dropna(subset=[key, "fwd3d"])
        r = stats.linregress(d[key], d["fwd3d"])
        return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)})
    up = G[G.ret30 > 0]; dn = G[G.ret30 <= 0]
    out["vr_up_quint"] = tab(up, "vr")
    out["vr_down_quint"] = tab(dn, "vr")
    out["slopes"] = pd.DataFrame({
        "vr_up": slope(up, "vr"), "vr_down": slope(dn, "vr"),
        "near_all": slope(G, "near"), "near_up": slope(up, "near"),
        "r1_all": slope(G, "r1"), "ret7_all": slope(G, "ret7"), "ret30_all": slope(G, "ret30"),
        "rng_all": slope(G, "rng"), "vol20_all": slope(G, "vol20")}).T
    out["near_quint_all"] = tab(G, "near")
    out["r1_quint_all"] = tab(G, "r1")
    out["vol20_quint"] = tab(G, "vol20")
    # vr slope by coin within up
    out["vr_up_by_coin"] = up.groupby("coin").apply(lambda d: slope(d, "vr"))
    # interaction vr x r1 sign within up
    up2 = up.copy(); up2["r1pos"] = up2.r1 > 0
    out["vr_up_by_r1sign"] = up2.groupby("r1pos").apply(lambda d: slope(d, "vr"))
    # weekday of daily return (all bars, fwd1)
    wd = A.dropna(subset=["fwd1"]).groupby("wd")["fwd1"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_fwd1"] = wd.drop(columns="std")
    # book daily by year
    D = pd.concat([df.assign(coin=c, w=w) for c, ws in days.items() for w, df in ws.items()])
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bd = D.dropna(subset=["book_return"]).groupby(["yr"])[["book_return", "coin_return"]].mean()
    out["book_by_year"] = bd
    return out

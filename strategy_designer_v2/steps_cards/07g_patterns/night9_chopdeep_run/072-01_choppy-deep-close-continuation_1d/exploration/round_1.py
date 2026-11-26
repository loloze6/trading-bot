def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            sd20 = r.rolling(20).std()
            hh = h.rolling(20).max()
            depth = (c - hh) / hh / sd20
            ll = l.rolling(20).min()
            pos = (c - ll) / (hh - ll)
            r5 = c / c.shift(5) - 1
            rng = (h - l) / c
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"], "ret": r, "nxt": nxt, "z1": r / sd20,
                "depth": depth, "pos": pos, "z5": r5 / (sd20 * np.sqrt(5)),
                "rngz": rng / (rng.rolling(20).mean()), "sd20": sd20,
                "alloc": b["postRebalance_current_allocation"],
                "gain": b["postRebalance_current_allocation"] * nxt,
                "up": (c > o).astype(int)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - cm
    d["wd"] = d["ts"].dt.dayofweek
    d["yr"] = d["ts"].dt.year
    d = d.dropna(subset=["ex"])
    out = {}
    def grp(g):
        x = g["ex"]
        n = len(x)
        return pd.Series({"n": n, "mean_ex_%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    d["choppy"] = (d["regime"] == "unknown").astype(int)
    dd = d.dropna(subset=["depth"])
    dd["dq"] = dd.groupby("choppy")["depth"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["depth quintile x choppy"] = dd.groupby(["choppy", "dq"]).apply(grp)
    dz = d.dropna(subset=["z1"]).copy()
    dz["zq"] = pd.cut(dz["z1"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["day z-move bins x choppy"] = dz.groupby(["choppy", "zq"]).apply(grp)
    d5 = d.dropna(subset=["z5"]).copy()
    d5["q"] = pd.qcut(d5["z5"], 5, labels=False)
    out["5-day z quintile (all)"] = d5.groupby("q").apply(grp)
    dp = d.dropna(subset=["pos"]).copy()
    dp["q"] = pd.qcut(dp["pos"], 5, labels=False)
    out["range position quintile x choppy"] = dp.groupby(["choppy", "q"]).apply(grp)
    dr = d.dropna(subset=["rngz"]).copy()
    dr["q"] = pd.qcut(dr["rngz"], 5, labels=False)
    out["range width quintile x up"] = dr.groupby(["up", "q"]).apply(grp)
    out["weekday"] = d.groupby("wd").apply(grp)
    dv = d.dropna(subset=["sd20"]).copy()
    dv["q"] = dv.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["vol tercile x choppy"] = dv.groupby(["choppy", "q"]).apply(grp)
    out["year"] = d.groupby("yr").apply(grp)
    # book: largest gains/losses
    dg = d.dropna(subset=["gain"])
    dg = dg[dg["alloc"].abs() > 0]
    dg["gq"] = pd.qcut(dg["gain"].rank(method="first"), 10, labels=False)
    out["book bar gains decile: features"] = dg.groupby("gq")[["gain", "z1", "depth", "pos", "up"]].mean()
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    days = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            r7p = c / c.shift(7) - 1
            r30p = c / c.shift(30) - 1
            dist = c / c.rolling(20, min_periods=20).max() - 1
            vr = v / v.rolling(30, min_periods=30).mean()
            vol20 = r1.rolling(20, min_periods=20).std()
            volrank = vol20 / vol20.rolling(120, min_periods=60).median()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n), "fwd": fwd, "r1": r1,
                              "r7p": r7p, "r30p": r30p, "dist": dist, "vr": vr, "volrank": volrank,
                              "fc": b["forecast"].astype(float),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "nh": b.get("debug_info.components.near_high.post_pipeline_value"),
                              "vv": b.get("debug_info.components.vol_ratio.post_pipeline_value")})
            rows.append(d[d["pos"] % H == 0])
    S = pd.concat(rows)
    S = S.dropna(subset=["fwd"])
    S["ex"] = S["fwd"] - S.groupby("coin")["fwd"].transform("mean")
    out = {}
    def slope_t(x, y):
        m = pd.concat([x, y], axis=1).dropna()
        r = stats.linregress(m.iloc[:, 0], m.iloc[:, 1])
        return round(r.slope / r.stderr, 2), len(m)
    res = {}
    for col in ["nh", "vv", "fc", "dist", "vr", "r1", "r7p", "r30p", "volrank"]:
        t, n = slope_t(S[col], S["ex"])
        res[col] = {"t": t, "n": n}
    out["slope t of 7d excess on each var"] = pd.DataFrame(res).T
    for col in ["dist", "vr", "r7p", "r30p", "volrank"]:
        q = pd.qcut(S[col], 5, labels=False, duplicates="drop")
        g = S.groupby(q)["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out[f"ex by {col} quintile"] = g.round(4)
    # per coin slope of dist and vr
    pc = {}
    for coin, g in S.groupby("coin"):
        pc[coin] = {"dist_t": slope_t(g["dist"], g["ex"])[0], "vr_t": slope_t(g["vr"], g["ex"])[0],
                    "fc_t": slope_t(g["fc"], g["ex"])[0], "n": len(g)}
    out["per coin t"] = pd.DataFrame(pc).T
    py = {}
    for y, g in S.groupby("yr"):
        py[y] = {"fc_t": slope_t(g["fc"], g["ex"])[0], "dist_t": slope_t(g["dist"], g["ex"])[0],
                 "vr_t": slope_t(g["vr"], g["ex"])[0], "n": len(g)}
    out["per year t"] = pd.DataFrame(py).T
    # interaction: dist near high split by vr
    S["near"] = pd.qcut(S["dist"], 3, labels=["far", "mid", "near"])
    S["vrq"] = pd.qcut(S["vr"], 3, labels=["thin", "mid", "heavy"])
    out["ex mean near x vol"] = S.pivot_table(index="near", columns="vrq", values="ex", aggfunc="mean").round(4)
    out["count near x vol"] = S.pivot_table(index="near", columns="vrq", values="ex", aggfunc="count")
    # book days
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w
            dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
            D.append(dd)
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    out["book by weekday"] = bk.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"]).round(5)
    out["book by window"] = bk.groupby("w")[["book_return", "coin_return"]].mean().round(5)
    return out

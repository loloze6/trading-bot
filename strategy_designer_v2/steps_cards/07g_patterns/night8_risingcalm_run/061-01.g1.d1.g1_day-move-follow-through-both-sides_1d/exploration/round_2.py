def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            z = r1 / vol30
            volz = b["volume"] / b["volume"].rolling(30, min_periods=20).mean()
            volrank = vol30 / vol30.expanding(min_periods=30).median()
            ret60 = c / c.shift(min(59, len(c)-1)) - 1
            ret20 = c / c.shift(20) - 1
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z": z, "volz": volz, "volrank": volrank, "ret20": ret20, "clv": clv,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f2", "f3", "f5"]:
        d[h + "x"] = d[h] - d.groupby("coin")[h].transform("mean")
    out = {}

    def tday(sub, col):
        sub = sub.dropna(subset=[col])
        s = sub.groupby("day")[col].sum()
        if len(s) < 5: return (np.nan, np.nan, len(sub), len(s))
        return (sub[col].mean(), s.mean() / (s.std(ddof=1) / np.sqrt(len(s))), len(sub), len(s))

    def slope_t(sub, x, y):
        sub = sub.dropna(subset=[x, y])
        X = sub[x].values; Y = sub[y].values
        X = X - X.mean()
        bta = (X * (Y - Y.mean())).sum() / (X ** 2).sum()
        e = Y - Y.mean() - bta * X
        # cluster by day
        g = pd.Series(X * e).groupby(sub["day"].values).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        return (bta, bta / se, len(sub))

    # 1. volume-weighted reversal of the day's move, next 1 and 2 days
    d["zv"] = d["z"] * np.log(d["volz"].clip(lower=0.05))
    d["zxv"] = d["z"] * d["volz"]
    for h, step in [("f1x", 1), ("f2x", 2), ("f3x", 3), ("f5x", 5)]:
        g = d[d.pos % step == 0]
        out[f"slope_{h}_on_z"] = pd.Series(slope_t(g, "z", h), index=["b", "t", "n"])
        out[f"slope_{h}_on_z_x_volz"] = pd.Series(slope_t(g, "zxv", h), index=["b", "t", "n"])
    g1 = d.dropna(subset=["z", "volz", "f1x"]).copy()
    g1["vq"] = pd.qcut(g1["volz"], 3, labels=["lowV", "midV", "highV"])
    g1["zb"] = pd.cut(g1["z"], [-99, -1, 0, 1, 99], labels=["bigdn", "dn", "up", "bigup"])
    res = {}
    for k, sub in g1.groupby(["vq", "zb"], observed=True):
        res[str(k)] = tday(sub, "f1x")
    out["f1x_by_volume_tercile_and_day"] = pd.DataFrame(res, index=["mean", "t", "n", "days"]).T
    # high-volume reversal by coin and by window half
    hv = g1[g1.vq == "highV"].copy()
    hv["dir"] = -np.sign(hv["z"]) * hv["f1x"]
    out["highV_reversal_by_coin"] = hv.groupby("coin")["dir"].agg(["mean", "size"])
    hv["half"] = np.where(hv["wn"] <= 12, "w7-12", "w13-18")
    res = {}
    for k, sub in hv.groupby("half"):
        res[k] = tday(sub, "dir")
    out["highV_reversal_by_half"] = pd.DataFrame(res, index=["mean", "t", "n", "days"]).T
    res = {}
    for k, sub in hv.groupby(np.where(hv["volrank"] <= 1, "calm", "agit")):
        res[k] = tday(sub, "dir")
    out["highV_reversal_by_agitation"] = pd.DataFrame(res, index=["mean", "t", "n", "days"]).T
    # 2. up-day continuation over 5 days (positive z only), graded
    g5 = d[(d.pos % 5 == 0)].dropna(subset=["z", "f5x"]).copy()
    up = g5[g5.z > 0]; dn = g5[g5.z < 0]
    out["f5x_slope_on_z_up_days"] = pd.Series(slope_t(up, "z", "f5x"), index=["b", "t", "n"])
    out["f5x_slope_on_z_down_days"] = pd.Series(slope_t(dn, "z", "f5x"), index=["b", "t", "n"])
    up = up.copy(); up["agit"] = np.where(up["volrank"] <= 1, "calm", "agit")
    up["tr"] = pd.cut(up["ret20"], [-9, -0.07, 0.07, 9], labels=["fall", "chop", "rise"])
    res = {}
    for k, sub in up.groupby("agit"):
        res[k] = slope_t(sub, "z", "f5x")
    for k, sub in up.groupby("tr", observed=True):
        res[str(k)] = slope_t(sub, "z", "f5x")
    out["up_day_f5_slope_by_regime"] = pd.DataFrame(res, index=["b", "t", "n"]).T
    out["up_big_by_coin"] = up[up.z > 1].groupby("coin")["f5x"].agg(["mean", "size"])
    # 3. close location graded: slope of f1x on clv, and by agitation
    out["slope_f1x_on_clv"] = pd.Series(slope_t(d, "clv", "f1x"), index=["b", "t", "n"])
    res = {}
    for k, sub in d.groupby(np.where(d["volrank"] <= 1, "calm", "agit")):
        res[k] = slope_t(sub, "clv", "f1x")
    out["slope_f1x_on_clv_by_agitation"] = pd.DataFrame(res, index=["b", "t", "n"]).T
    return out

def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            down = (r < 0).astype(int)
            run = np.zeros(len(b), int); cnt = 0
            prev_run = np.zeros(len(b), int)
            for i in range(len(b)):
                prev_run[i] = cnt
                if r.iloc[i] < 0: cnt += 1
                elif r.iloc[i] >= 0: cnt = 0
            tr = c / c.shift(60) - 1
            vol = r.rolling(30).std()
            vrank = vol.rolling(len(b), min_periods=30).rank(pct=True)
            rng = (h - l) / c
            pos = (c - l) / (h - l).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "nxt": nxt, "nxt2": nxt2, "prun": prev_run,
                               "tr": tr, "vol": vol, "vrank": vrank, "rng": rng, "pos": pos,
                               "alloc": b["postRebalance_current_allocation"], "fc": b["forecast"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    drift = D.groupby("coin")["nxt"].mean()
    D["dev"] = D["nxt"] - D["coin"].map(drift)
    D["trend"] = np.where(D["tr"] > 0.10, "rising", np.where(D["tr"] < -0.10, "falling", "choppy"))
    D.loc[D["tr"].isna(), "trend"] = "na"
    D["up"] = D["r"] > 0
    D["zr"] = D["r"] / D["vol"]

    def stat(g, col="dev", sign=-1):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "mean": np.nan, "t": np.nan, "days": 0})
        x = sign * g[col]
        m = x.mean()
        s = (x - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt((s**2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t": m / se if se > 0 else np.nan, "days": G})

    out = {}
    U = D[D["up"]].copy()
    U["runc"] = U["prun"].clip(upper=5)
    out["upday short-dev by trend x prior run"] = U.groupby(["trend", "runc"]).apply(stat)
    A = D.copy()
    out["all days short-dev by trend x upday"] = A.groupby(["trend", "up"]).apply(stat)
    F = U[U["trend"] == "falling"].copy()
    F["zq"] = pd.qcut(F["zr"], 4, labels=False, duplicates="drop")
    out["falling upday by up-size quartile"] = F.groupby("zq").apply(stat)
    F["posq"] = pd.qcut(F["pos"], 3, labels=False, duplicates="drop")
    out["falling upday by close position tercile"] = F.groupby("posq").apply(stat)
    F["vq"] = pd.qcut(F["vrank"], 2, labels=False, duplicates="drop")
    out["falling upday by vol rank half"] = F.groupby("vq").apply(stat)
    F["trq"] = pd.qcut(F["tr"], 3, labels=False, duplicates="drop")
    out["falling upday by trend depth tercile"] = F.groupby("trq").apply(stat)
    out["falling upday by coin"] = F.groupby("coin").apply(stat)
    F["wd"] = F["ts"].dt.dayofweek
    out["falling upday by weekday"] = F.groupby("wd").apply(stat)
    out["falling upday 2day short"] = stat(F.assign(dev2=F["nxt2"]), "dev2")
    # down days in falling market
    Dn = D[(~D["up"]) & (D["trend"] == "falling")].copy()
    Dn["zq"] = pd.qcut(Dn["zr"], 4, labels=False, duplicates="drop")
    out["falling downday by size quartile (short)"] = Dn.groupby("zq").apply(stat)
    Rr = U[U["trend"] == "rising"].copy()
    Rr["zq"] = pd.qcut(Rr["zr"], 4, labels=False, duplicates="drop")
    out["rising upday by size quartile (short)"] = Rr.groupby("zq").apply(stat)
    return out

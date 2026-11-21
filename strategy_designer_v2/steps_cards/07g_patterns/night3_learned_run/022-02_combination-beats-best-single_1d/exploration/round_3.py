def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    daily = []; grid = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            vol = r1.rolling(30).std()
            daily.append(pd.DataFrame({"coin": coin, "win": w, "yr": ts.dt.year, "wd": ts.dt.weekday, "r": r1,
                "vol_prev": vol.shift(1), "wk_prev": (c.shift(1) / c.shift(8) - 1), "r_prev": r1.shift(1),
                "volu_prev": (b["volume"].astype(float) / b["volume"].astype(float).rolling(30).mean()).shift(1)}))
            f = pd.DataFrame({"coin": coin, "win": w, "yr": ts.dt.year, "ret1z": r1 / vol,
                "volu": b["volume"].astype(float) / b["volume"].astype(float).rolling(30).mean(),
                "y": c.shift(-5) / c - 1})
            g = f.iloc[::5]; grid.append(g[g["y"].notna()])
    D = pd.concat(daily).dropna(subset=["r"])
    D["rd"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    out = {}
    S = D[D.wd == 5].dropna(subset=["vol_prev", "wk_prev"]).copy()
    S["rz"] = S["rd"] / S["vol_prev"]
    for s in ["vol_prev", "wk_prev", "r_prev", "volu_prev"]:
        e = S.dropna(subset=[s]).copy()
        e["q"] = e.groupby("coin")[s].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out["sat_by_" + s] = e.groupby("q").agg(n=("rd", "size"), mean_pct=("rd", lambda x: x.mean() * 100), mean_z=("rz", "mean")).assign(t=e.groupby("q")["rd"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    W = D.groupby("wd")["rd"].agg(["mean", "std", "count"])
    out["weekday_t_and_abs"] = W.assign(t=W["mean"] / (W["std"] / np.sqrt(W["count"])), mean=W["mean"] * 100)
    G = pd.concat(grid, ignore_index=True)
    G["y"] = G["y"] - G.groupby("coin")["y"].transform("mean")
    e = G.dropna(subset=["ret1z", "volu"]).copy()
    e["up"] = e["ret1z"].clip(lower=0)
    e["vq"] = e.groupby("coin")["volu"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    res = []
    for k, h in e.groupby("vq"):
        r, p = stats.pearsonr(h["ret1z"], h["y"])
        res.append([k, len(h), round(r, 3), round(p, 3)])
    out["ret1z_corr_by_volume_tercile"] = pd.DataFrame(res, columns=["vq", "n", "r", "p"])
    return out

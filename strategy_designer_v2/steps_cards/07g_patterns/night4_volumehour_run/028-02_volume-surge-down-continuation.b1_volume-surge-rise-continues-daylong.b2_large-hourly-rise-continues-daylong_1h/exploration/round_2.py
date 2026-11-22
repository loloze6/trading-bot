def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            scale = r.abs().rolling(720, min_periods=240).mean().shift(1)
            vbase = v.rolling(720, min_periods=240).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": r / scale,
                              "vr": v / vbase, "r1": r, "hour": ts.dt.hour, "year": ts.dt.year,
                              "wd": ts.dt.weekday})
            d["f1"] = c.shift(-1) / c - 1
            d["f24"] = c.shift(-24) / c - 1
            d["f12"] = c.shift(-12) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 12, 24):
        dr = {k: g[g["pos"] % h == 0][f"f{h}"].dropna().mean() for k, g in D.groupby("coin")}
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(dr)

    def ev(E, h):
        E = E[E[f"x{h}"].notna()].copy()
        E["cell"] = E["pos"] // h
        E = E.groupby(["coin", "w", "cell"]).head(1)
        x = E[f"x{h}"] * np.sign(E["z"])
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    big = D["z"].abs() >= 2
    vb = pd.cut(D["vr"], [0, 1, 1.5, 2, 3, 4, 6, 1e9])
    t = {}
    for lab, g in D[big].groupby(vb[big], observed=True):
        for h in (12, 24):
            s = ev(g, h); t[(str(lab), h)] = s
    out["signed continuation |z|>=2 by volume ratio"] = pd.DataFrame(t).T.round(3)
    # 2-4x volume, |z| 2-5, by side, coin and year
    m = big & (D["z"].abs() < 5) & (D["vr"] >= 2) & (D["vr"] < 4)
    t = {}
    for k, g in D[m].groupby([np.sign(D["z"][m]), "coin"]):
        t[k] = ev(g, 24)
    out["vr2-4 z2-5 h24 by side,coin"] = pd.DataFrame(t).T.round(3)
    t = {}
    for k, g in D[m].groupby("year"):
        t[k] = ev(g, 24)
    out["vr2-4 z2-5 h24 by year"] = pd.DataFrame(t).T.round(3)
    # hour 20-21 effect: by coin and by year
    H = D[D["hour"].isin([20, 21])].dropna(subset=["x1"])
    g = H.groupby(["coin"])["x1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["mean"] *= 100
    out["hour20-21 by coin"] = g.round(4)
    g = H.groupby(["year"])["x1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["mean"] *= 100
    out["hour20-21 by year"] = g.round(4)
    g = H.groupby(["wd"])["x1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["mean"] *= 100
    out["hour20-21 by weekday"] = g.round(4)
    # graded: hour 20-21 return vs prior 24h return sign
    D["p24"] = D.groupby(["coin", "w"])["r1"].transform(lambda s: s.rolling(24).sum())
    H = D[D["hour"].isin([20, 21])].dropna(subset=["x1", "p24"])
    q = H.groupby("coin")["p24"].transform(lambda s: pd.qcut(s, 4, labels=False))
    g = H.groupby(q)["x1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["mean"] *= 100
    out["hour20-21 by prior24h quartile"] = g.round(4)
    # book's worst/best days: what preceded
    dd = []
    for coin, wins in data["days"].items():
        for w, tb in wins.items():
            tb = tb.copy(); tb["coin"] = coin; dd.append(tb)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    DD["gap"] = DD["book_return"] - DD["coin_return"]
    lo = DD["book_return"].quantile(0.02); hi = DD["book_return"].quantile(0.98)
    out["worst2% days: mean book, coin"] = DD[DD["book_return"] <= lo][["book_return", "coin_return"]].mean().round(4)
    out["best2% days: mean book, coin"] = DD[DD["book_return"] >= hi][["book_return", "coin_return"]].mean().round(4)
    return out

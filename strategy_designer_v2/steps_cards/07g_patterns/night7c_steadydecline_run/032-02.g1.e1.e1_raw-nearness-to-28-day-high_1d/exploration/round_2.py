def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi28 = c.rolling(28, min_periods=28).max()
            lo28 = c.rolling(28, min_periods=28).min()
            rg = (b["high"] - b["low"]) / c
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]).values,
                "near": (c / hi28 - 1).values,
                "fromlo": (c / lo28 - 1).values,
                "ret28": (c / c.shift(27) - 1).values,
                "ret5p": (c / c.shift(5) - 1).values,
                "ret1": r1.values,
                "vol20": r1.rolling(20).std().values,
                "volrel": (r1.rolling(10).std() / r1.rolling(60, min_periods=30).std()).values,
                "rng": (rg.rolling(5).mean() / rg.rolling(60, min_periods=30).mean()).values,
                "vrel": (b["volume"].rolling(5).mean() / b["volume"].rolling(60, min_periods=30).mean()).values,
                "fc": b["forecast"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "fwd": (c.shift(-H) / c - 1).values,
                "pos": np.arange(len(b)),
            })
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"]).reset_index(drop=True)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    out = {}
    def clus_t(xcol):
        d = pd.DataFrame({"x": xcol.values, "y": g["ex"].values, "day": g["day"].values}).dropna()
        X = np.c_[np.ones(len(d)), d["x"].values]
        beta = np.linalg.lstsq(X, d["y"].values, rcond=None)[0]
        e = d["y"].values - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        s = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = len(s)
        V = XtXi @ (s.T @ s) @ XtXi * G / (G - 1)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), len(d), G
    sl = {}
    feats = ["near", "fromlo", "ret28", "ret5p", "ret1", "vol20", "volrel", "rng", "vrel", "fc", "alloc"]
    for f in feats:
        x = (g[f] - g.groupby("coin")[f].transform("mean")) / g.groupby("coin")[f].transform("std")
        b_, t_, n_, G_ = clus_t(x)
        sl[f] = {"slope_per_sd": b_, "t_day": t_, "n": n_, "days": G_}
    out["slopes"] = pd.DataFrame(sl).T
    def qtab(d, f, q=5):
        d = d.dropna(subset=[f]).copy()
        d["q"] = d.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("q")["ex"].agg(["mean", "std", "count"])
        r["t"] = r["mean"] / r["std"] * np.sqrt(r["count"])
        return r.drop(columns="std")
    for f in ["near", "fromlo", "ret28", "ret5p", "vol20", "volrel", "rng", "vrel"]:
        out["q_" + f] = qtab(g, f)
    d = g.dropna(subset=["near", "ret28", "rng", "vol20"]).copy()
    d["near_t"] = d.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["calm"] = d.groupby("coin")["rng"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=False))
    d["hv"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=False))
    d["up28"] = (d["ret28"] > 0).astype(int)
    for k in ["up28", "calm", "hv"]:
        r = d.groupby([k, "near_t"])["ex"].agg(["mean", "std", "count"])
        r["t"] = r["mean"] / r["std"] * np.sqrt(r["count"])
        out["near_x_" + k] = r.drop(columns="std")
    # down28 calm: brief's own claim
    dn = d[d["ret28"] < 0].copy()
    dn["r28t"] = dn.groupby("coin")["ret28"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    r = dn.groupby(["calm", "r28t"])["ex"].agg(["mean", "std", "count"])
    r["t"] = r["mean"] / r["std"] * np.sqrt(r["count"])
    out["down28_calm_x_depth"] = r.drop(columns="std")
    out["by_win"] = g.groupby("win")["ex"].agg(["mean", "count"])
    out["by_coin_near_slope"] = g.groupby("coin").apply(lambda s: pd.Series({"corr_near_ex": s["near"].corr(s["ex"]), "n": s["near"].notna().sum()}))
    r = g.assign(wd=pd.to_datetime(g["ts"]).dt.weekday).groupby("wd")["ex"].agg(["mean", "count"])
    out["by_wd_grid"] = r
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    dd = pd.concat(dd, ignore_index=True)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    out["book_by_wd"] = bk.groupby("wd")[["book_return", "coin_return"]].mean()
    out["book_by_win"] = bk.groupby("win")[["book_return", "coin_return"]].mean()
    cr = bk["coin_return"]
    bk["cq"] = pd.qcut(cr.rank(method="first"), 5, labels=False)
    out["book_by_coin_quintile"] = bk.groupby("cq")[["book_return", "coin_return"]].mean()
    out["book_stats"] = pd.Series({"corr": bk["book_return"].corr(cr), "beta": np.polyfit(cr, bk["book_return"], 1)[0],
                                   "mean_book": bk["book_return"].mean(), "mean_coin": cr.mean(), "n_days": len(bk)})
    # coin-level daily: return after large 1-day moves (next 5 days)
    ev = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].astype(float).reset_index(drop=True)
            r1 = c.pct_change(); sd = r1.rolling(60, min_periods=30).std()
            z = r1 / sd
            f5 = c.shift(-5) / c - 1
            ev.append(pd.DataFrame({"z": z.values, "f5": f5.values, "pos": np.arange(len(c)), "coin": coin}))
    ev = pd.concat(ev, ignore_index=True)
    ev = ev[ev["pos"] % 5 == 0].dropna()
    ev["f5ex"] = ev["f5"] - ev.groupby("coin")["f5"].transform("mean")
    ev["zb"] = pd.cut(ev["z"], [-99, -2, -1, 0, 1, 2, 99])
    r = ev.groupby("zb", observed=True)["f5ex"].agg(["mean", "std", "count"])
    r["t"] = r["mean"] / r["std"] * np.sqrt(r["count"])
    out["after_1d_move_z"] = r.drop(columns="std")
    return out

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
            sd60 = r1.rolling(60, min_periods=30).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]).values,
                "near": (c / hi28 - 1).values,
                "vol20": r1.rolling(20).std().values,
                "z1": (r1 / sd60).values,
                "ret3p": (c / c.shift(3) - 1).values,
                "fwd": (c.shift(-H) / c - 1).values,
                "fwd10": (c.shift(-10) / c - 1).values,
                "pos": np.arange(len(b)),
            })
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"]).reset_index(drop=True)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    out = {}
    def clus(d, xc, yc="ex"):
        d = d[[xc, yc, "day"]].dropna()
        if len(d) < 30:
            return pd.Series({"slope": np.nan, "t_day": np.nan, "n": len(d), "days": np.nan})
        X = np.c_[np.ones(len(d)), d[xc].values]
        beta = np.linalg.lstsq(X, d[yc].values, rcond=None)[0]
        e = d[yc].values - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        s = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = len(s)
        V = XtXi @ (s.T @ s) @ XtXi * G / (G - 1)
        return pd.Series({"slope": beta[1], "t_day": beta[1] / np.sqrt(V[1, 1]), "n": len(d), "days": G})
    d = g.dropna(subset=["near", "vol20"]).copy()
    d["vt"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["nz"] = (d["near"] - d.groupby("coin")["near"].transform("mean")) / d.groupby("coin")["near"].transform("std")
    out["near_slope_by_vol_tertile"] = d.groupby("vt").apply(lambda s: clus(s, "nz"))
    d["nq"] = d.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    r = d.groupby(["vt", "nq"])["ex"].agg(["mean", "std", "count"])
    r["t"] = r["mean"] / r["std"] * np.sqrt(r["count"])
    out["vt_x_near_quartile"] = r.drop(columns="std")
    lo = d[d["vt"] == 0]
    out["lowvol_near_slope_by_win"] = lo.groupby("win").apply(lambda s: pd.Series({"corr": s["near"].corr(s["ex"]), "n": len(s)}))
    out["lowvol_near_slope_by_coin"] = lo.groupby("coin").apply(lambda s: pd.Series({"corr": s["near"].corr(s["ex"]), "n": len(s)}))
    # interaction: near * (-vol z)
    d["vz"] = (d["vol20"] - d.groupby("coin")["vol20"].transform("mean")) / d.groupby("coin")["vol20"].transform("std")
    d["inter"] = d["nz"] * (-d["vz"])
    out["interaction_slope"] = clus(d, "inter")
    # 10-day horizon in low vol
    lo2 = lo.copy()
    lo2["ex10"] = lo2["fwd10"] - g.groupby("coin")["fwd10"].transform("mean").reindex(lo2.index)
    out["lowvol_near_slope_10d"] = clus(lo2, "nz", "ex10")
    # z1 graded
    e = g.dropna(subset=["z1"]).copy()
    out["z1_slope"] = clus(e, "z1")
    e["zb"] = pd.cut(e["z1"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    r = e.groupby("zb", observed=True)["ex"].agg(["mean", "std", "count"])
    r["t"] = r["mean"] / r["std"] * np.sqrt(r["count"])
    out["z1_bins"] = r.drop(columns="std")
    return out

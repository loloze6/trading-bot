def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r0": r, "vol": vol,
                "calm": (b["regime"] != "chop").astype(int),
                "clv": ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)),
                "r1": c.shift(-1) / c - 1,
                "pos": np.arange(len(b)),
            })
            for h in [3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
                df[f"p{h}z"] = (c / c.shift(h) - 1) / (vol * np.sqrt(h))
            df["p60"] = c / c.shift(60) - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["yr"] = d["day"].dt.year
    mu = d.groupby("coin")["r0"].mean()
    d["xr1"] = d["r1"] - d["coin"].map(mu)
    for h in [3, 5, 10]:
        d[f"xf{h}"] = d[f"f{h}"] - h * d["coin"].map(mu)
    d["trend"] = np.where(d.p60 > 0.10, "rising", np.where(d.p60 < -0.10, "falling", "choppy"))
    def cslope(x, y, day):
        m = pd.DataFrame({"x": x, "y": y, "d": day}).dropna()
        if len(m) < 20: return (np.nan, np.nan, len(m))
        X = np.c_[np.ones(len(m)), m["x"]]
        beta = np.linalg.lstsq(X, m["y"].values, rcond=None)[0]
        e = m["y"].values - X @ beta
        S = pd.DataFrame(X * e[:, None]).groupby(m["d"].values).sum().values
        B = np.linalg.inv(X.T @ X)
        V = B @ (S.T @ S) @ B
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(m))
    out = {}
    # A. calm momentum: horizons and grid offsets
    res = []
    for h in [3, 5, 10]:
        for off in range(min(h, 5)):
            g = d[(d.pos % h == off)]
            for calm in [1, 0]:
                gg = g[g.calm == calm]
                b_, t, n = cslope(gg[f"p{h}z"], gg[f"xf{h}"], gg["day"])
                res.append({"h": h, "off": off, "calm": calm, "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    out["mom_h_offset"] = pd.DataFrame(res)
    # B. calm 5d momentum by coin, year, trend (offset 0)
    g = d[(d.pos % 5 == 0) & (d.calm == 1)]
    res = []
    for k, gg in g.groupby("coin"):
        b_, t, n = cslope(gg["p5z"], gg["xf5"], gg["day"]); res.append({"by": k, "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    for k, gg in g.groupby("yr"):
        b_, t, n = cslope(gg["p5z"], gg["xf5"], gg["day"]); res.append({"by": str(k), "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    for k, gg in g.groupby("trend"):
        b_, t, n = cslope(gg["p5z"], gg["xf5"], gg["day"]); res.append({"by": k, "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    for s, gg in [("up", g[g.p5z > 0]), ("down", g[g.p5z < 0])]:
        b_, t, n = cslope(gg["p5z"], gg["xf5"], gg["day"]); res.append({"by": s, "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    out["calm_mom5_split"] = pd.DataFrame(res)
    # C. agitated close-location next day: by coin, year, trend, and clv quintile means
    g = d[d.calm == 0]
    res = []
    for k, gg in g.groupby("coin"):
        b_, t, n = cslope(gg["clv"], gg["xr1"], gg["day"]); res.append({"by": k, "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    for k, gg in g.groupby("yr"):
        b_, t, n = cslope(gg["clv"], gg["xr1"], gg["day"]); res.append({"by": str(k), "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    for k, gg in g.groupby("trend"):
        b_, t, n = cslope(gg["clv"], gg["xr1"], gg["day"]); res.append({"by": k, "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    # controlling for the day's return: residual of clv on z
    z = g["r0"] / g["vol"]
    m = pd.DataFrame({"clv": g["clv"], "z": z, "y": g["xr1"], "d": g["day"]}).dropna()
    X = np.c_[np.ones(len(m)), m["z"]]
    bb = np.linalg.lstsq(X, m["clv"].values, rcond=None)[0]
    m["clv_res"] = m["clv"].values - X @ bb
    b_, t, n = cslope(m["clv_res"], m["y"], m["d"]); res.append({"by": "clv_resid_of_z", "slope_bp": round(b_*1e4, 1), "t": round(t, 2), "n": n})
    out["agit_clv_split"] = pd.DataFrame(res)
    g = g.dropna(subset=["clv", "xr1"]).copy()
    g["q"] = pd.qcut(g["clv"], 5, labels=False)
    out["agit_clv_quintiles_bp"] = (g.groupby("q")["xr1"].agg(["mean", "count"]).assign(mean=lambda x: (x["mean"]*1e4).round(1)))
    return out

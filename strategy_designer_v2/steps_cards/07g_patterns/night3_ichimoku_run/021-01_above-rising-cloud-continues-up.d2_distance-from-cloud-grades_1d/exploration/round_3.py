def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "ret1": r1, "ret26": c / c.shift(26) - 1, "ret14": c / c.shift(14) - 1,
                "vol14": r1.rolling(14).std(), "vol60": r1.rolling(60).std(),
                "f7": c.shift(-7) / c - 1, "f14": c.shift(-14) / c - 1, "f26": c.shift(-26) / c - 1,
                "wd": ts.dt.weekday, "year": ts.dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["vr"] = A["vol14"] / A["vol60"]
    def reg(gg, x, y):
        s = stats.linregress(gg[x], gg[y]); return s.slope, s.slope / s.stderr, len(gg)
    res = []
    for H, col in [(7, "f7"), (14, "f14"), (26, "f26")]:
        g = A[A["pos"] % H == 0].dropna(subset=[col, "vol14", "ret26", "vol60"]).copy()
        g["ex"] = g[col] - g.groupby("coin")[col].transform("mean")
        g["vq"] = g.groupby("coin")["vol14"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        g["calm"] = g.groupby("coin")["vr"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        for lab, gg in [("all", g), ("lowvol", g[g.vq == 0]), ("lowvol_w1-12", g[(g.vq == 0) & (g.wn <= 12)]),
                        ("lowvol_w13-24", g[(g.vq == 0) & (g.wn > 12)]), ("highvol", g[g.vq == 2]),
                        ("vr_low", g[g.calm == 0]), ("vr_high", g[g.calm == 2])]:
            s, t, n = reg(gg, "ret26", "ex")
            res.append({"H": H, "grp": lab, "n": n, "slope": s, "t": t})
        # interaction: momentum scaled by inverse vol
        g["mz"] = g["ret26"] / g["vol14"]
        s, t, n = reg(g, "mz", "ex")
        res.append({"H": H, "grp": "ret26/vol14", "n": n, "slope": s, "t": t})
    out["mom_vol"] = pd.DataFrame(res).round(4)
    g = A[A["pos"] % 7 == 0].dropna(subset=["f7", "vol14", "ret26"]).copy()
    g["ex"] = g["f7"] - g.groupby("coin")["f7"].transform("mean")
    g["vq"] = g.groupby("coin")["vol14"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    bc = []
    for coin, gg in g[g.vq == 0].groupby("coin"):
        s, t, n = reg(gg, "ret26", "ex"); bc.append({"coin": coin, "n": n, "slope": s, "t": t})
    out["lowvol_f7_by_coin"] = pd.DataFrame(bc).round(3)
    # Saturday excess graded by volatility
    d = A.dropna(subset=["ret1", "vol14"]).copy()
    d["ex"] = d["ret1"] - d.groupby("coin")["ret1"].transform("mean")
    d["prevvol"] = d.groupby(["coin", "win"])["vol14"].shift(1)
    s = d[d.wd == 5].dropna(subset=["prevvol"]).copy()
    s["vq"] = s.groupby("coin")["prevvol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["sat_by_vol"] = s.groupby("vq")["ex"].agg(["mean", "count"]).round(5)
    s["prev26"] = d.groupby(["coin", "win"])["ret26"].shift(1).reindex(s.index)
    ss = s.dropna(subset=["prev26"])
    sl, t, n = reg(ss, "prev26", "ex")
    out["sat_on_ret26"] = pd.Series({"slope": sl, "t": t, "n": n})
    out["sat_by_half"] = s.assign(h=s.wn > 12).groupby("h")["ex"].agg(["mean", "count"]).round(5)
    return out

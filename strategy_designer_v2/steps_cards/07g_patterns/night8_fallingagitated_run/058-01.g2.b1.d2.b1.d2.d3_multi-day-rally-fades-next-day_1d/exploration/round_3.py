def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r1": r1, "z1": r1 / sd30,
                               "zp4": (c.shift(1) / c.shift(5) - 1) / sd30,
                               "z5": (c / c.shift(5) - 1) / sd30,
                               "regime": b["regime"], "pos_i": np.arange(len(b))})
            for h in (1, 2, 3):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["inprof"] = d["regime"] != "chop"
    for h in (1, 2, 3):
        g = d[d.pos_i % h == 0]
        mu = g.groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(mu)
        d.loc[d.pos_i % h != 0, f"u{h}"] = np.nan
    d["day"] = d.ts.dt.floor("D"); d["year"] = d.ts.dt.year

    def tclust(x, day):
        s = pd.DataFrame({"x": x, "d": day}).dropna()
        if len(s) < 5: return np.nan
        m = s.x.mean(); dv = (s.x - m).groupby(s.d).sum()
        return m / (np.sqrt((dv ** 2).sum()) / len(s))

    out = {}
    for name, mask in [("in", d.inprof), ("out", ~d.inprof)]:
        up = d[mask & (d.r1 > 0)].copy()
        for h in (1, 2, 3):
            up[f"s{h}"] = -up[f"u{h}"]
        # theme check: z5 among up days
        s = up[["z5", "u1"]].dropna(); r, p = stats.spearmanr(s.z5, s.u1)
        out[f"{name}_up_z5_rho_u1"] = f"rho {r:.3f} p {p:.4f} n {len(s)}"
        # bounce after a fall: prior 4-day fall size, among up days with prior fall
        f = up[up.zp4 < 0].copy()
        f["q"] = pd.qcut(f.zp4, 4, labels=False)
        res = []
        for q, g in f.groupby("q"):
            row = {"q": q, "zp4": g.zp4.mean()}
            for h in (1, 2, 3):
                row[f"s{h}"] = g[f"s{h}"].mean(); row[f"t{h}"] = tclust(g[f"s{h}"], g.day); row[f"n{h}"] = g[f"s{h}"].notna().sum()
            res.append(row)
        out[f"{name}_bounce_by_prior_fall"] = pd.DataFrame(res).round(4)
        for h in (1, 3):
            s = f[["zp4", f"s{h}"]].dropna(); r, p = stats.spearmanr(-s.zp4, s[f"s{h}"])
            out[f"{name}_bounce_rho_s{h}"] = f"rho {r:.3f} p {p:.4f} n {len(s)}"
        out[f"{name}_bounce_all"] = pd.Series({"s1": f.s1.mean(), "t1": tclust(f.s1, f.day), "n1": f.s1.notna().sum(),
                                               "days": f.dropna(subset=["s1"]).day.nunique(),
                                               "s3": f.s3.mean(), "t3": tclust(f.s3, f.day), "n3": f.s3.notna().sum()})
        if name == "in":
            out["in_bounce_by_year"] = f.groupby("year").s1.agg(["mean", "count"]).round(4)
            out["in_bounce_by_coin"] = f.groupby("coin").s1.agg(["mean", "count"]).round(4)
            big = f[f.zp4 < f.zp4.median()]
            out["in_bounce_bighalf_by_year"] = big.groupby("year").s1.agg(["mean", "count"]).round(4)
    return out

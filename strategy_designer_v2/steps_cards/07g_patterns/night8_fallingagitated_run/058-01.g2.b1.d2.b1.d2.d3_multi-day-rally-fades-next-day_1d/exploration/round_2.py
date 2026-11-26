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
                               "rng": (b["high"] - b["low"]) / c / sd30,
                               "clv": (c - b["low"]) / (b["high"] - b["low"]),
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
        up["q"] = pd.qcut(up.z1, 4, labels=False)
        res = []
        for q, g in up.groupby("q"):
            row = {"q": q, "z1": g.z1.mean()}
            for h in (1, 2, 3):
                row[f"u{h}"] = g[f"u{h}"].mean(); row[f"t{h}"] = tclust(g[f"u{h}"], g.day); row[f"n{h}"] = g[f"u{h}"].notna().sum()
            res.append(row)
        out[f"{name}_upday_z1_quart"] = pd.DataFrame(res).round(4)
        s = up[["z1", "u1"]].dropna(); r, p = stats.spearmanr(s.z1, s.u1)
        out[f"{name}_upday_rho"] = f"rho {r:.3f} p {p:.4f} n {len(s)}"
        dn = d[mask & (d.r1 < 0)][["z1", "u1"]].dropna(); r, p = stats.spearmanr(dn.z1, dn.u1)
        out[f"{name}_downday_rho"] = f"rho {r:.3f} p {p:.4f} n {len(dn)}"
    up = d[d.inprof & (d.r1 > 0)].copy()
    # graded: short signal = z1 on up days; per-case short move u1 * -1, weighted
    up["s"] = -up.u1
    up["pq"] = pd.qcut(up.zp4, 3, labels=False)
    out["in_up_by_prior4_tercile"] = up.groupby("pq").agg(zp4=("zp4", "mean"), s=("s", "mean"), n=("s", "count")).round(4)
    out["in_up_rho_by_prior_tercile"] = pd.Series({q: "rho %.3f n %d" % (stats.spearmanr(g.dropna(subset=["u1"]).z1, g.dropna(subset=["u1"]).u1)[0], g.u1.notna().sum()) for q, g in up.groupby("pq")})
    # by year and by window: mean short move on up days, and top half z1
    top = up[up.z1 > up.z1.median()]
    out["in_up_top_by_year"] = top.groupby("year").s.agg(["mean", "count"]).round(4)
    out["in_up_all_by_win"] = up.groupby("win").s.agg(["mean", "count"]).round(4)
    out["in_up_top_t"] = pd.Series({"mean": top.s.mean(), "t": tclust(top.s, top.day), "n": top.s.notna().sum(), "days": top.dropna(subset=["s"]).day.nunique()})
    out["in_up_all_t"] = pd.Series({"mean": up.s.mean(), "t": tclust(up.s, up.day), "n": up.s.notna().sum()})
    out["in_up_by_coin"] = up.groupby("coin").s.agg(["mean", "count"]).round(4)
    # close near high on up days in profile
    up["cq"] = pd.qcut(up.clv, 3, labels=False)
    out["in_up_by_clv"] = up.groupby("cq").agg(clv=("clv", "mean"), s=("s", "mean"), n=("s", "count")).round(4)
    return out

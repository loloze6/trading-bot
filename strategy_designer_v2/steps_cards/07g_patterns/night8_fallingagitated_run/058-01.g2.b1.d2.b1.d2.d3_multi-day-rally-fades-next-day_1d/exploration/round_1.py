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
                               "z5": (c / c.shift(5) - 1) / sd30,
                               "z10": (c / c.shift(10) - 1) / sd30,
                               "rng": (b["high"] - b["low"]) / c / sd30,
                               "clv": (c - b["low"]) / (b["high"] - b["low"]),
                               "regime": b["regime"], "fc": b["forecast"],
                               "pos": b["postRebalance_current_allocation"], "pos_i": np.arange(len(b))})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["inprof"] = d["regime"] != "chop"
    for h in (1, 2, 3, 5):
        g = d[d.pos_i % h == 0]
        mu = g.groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(mu)
        d.loc[d.pos_i % h != 0, f"u{h}"] = np.nan
    d["day"] = d.ts.dt.floor("D")

    def tclust(x, day):
        s = pd.DataFrame({"x": x, "d": day}).dropna()
        if len(s) < 5: return np.nan
        m = s.x.mean(); dv = (s.x - m).groupby(s.d).sum()
        return m / (np.sqrt((dv ** 2).sum()) / len(s))

    out = {}
    d["q5"] = pd.qcut(d["z5"], 5, labels=False)
    d["q1"] = pd.qcut(d["z1"], 5, labels=False)
    for name, mask in [("in", d.inprof), ("out", ~d.inprof)]:
        for qc in ("q5", "q1"):
            res = []
            for q, g in d[mask].groupby(qc):
                row = {"q": q, "zmean": g[qc.replace("q", "z")].mean()}
                for h in (1, 2, 3, 5):
                    row[f"u{h}"] = g[f"u{h}"].mean(); row[f"t{h}"] = tclust(g[f"u{h}"], g.day); row[f"n{h}"] = g[f"u{h}"].notna().sum()
                res.append(row)
            out[f"{name}_{qc}"] = pd.DataFrame(res).round(4)
    # in-profile: last day up vs down, by z5 quintile, next 1 and 3 days
    g = d[d.inprof].copy(); g["up"] = g.r1 > 0
    out["in_z5_by_up_u1"] = g.groupby(["q5", "up"])["u1"].agg(["mean", "count"]).round(4)
    out["in_z5_by_up_u3"] = g.groupby(["q5", "up"])["u3"].agg(["mean", "count"]).round(4)
    # range & close location in profile
    g["rq"] = pd.qcut(g["rng"], 4, labels=False)
    g["cq"] = pd.qcut(g["clv"], 3, labels=False)
    out["in_range_close_u1"] = g.groupby(["rq", "cq"])["u1"].agg(["mean", "count"]).round(4)
    out["in_range_close_u3"] = g.groupby(["rq", "cq"])["u3"].agg(["mean", "count"]).round(4)
    # weekday
    d["wd"] = d.ts.dt.weekday
    out["wd"] = d.groupby(["wd", "inprof"])["u1"].agg(["mean", "count"]).unstack().round(4)
    # correlations
    cor = {}
    for name, mask in [("in", d.inprof), ("out", ~d.inprof)]:
        for z in ("z1", "z5", "z10", "rng"):
            for h in (1, 3, 5):
                s = d[mask][[z, f"u{h}"]].dropna()
                r, p = stats.spearmanr(s[z], s[f"u{h}"])
                cor[f"{name}_{z}_u{h}"] = f"rho {r:.3f} p {p:.3f} n {len(s)}"
    out["spearman"] = pd.Series(cor)
    # book: largest gain/loss days
    dd = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()])
    bk = dd.groupby("day")["book_return"].mean().dropna()
    out["book_share_by_quantile"] = pd.Series({"n_days": len(bk), "top10_sum": bk.nlargest(10).sum(), "bot10_sum": bk.nsmallest(10).sum(), "total": bk.sum()})
    out["share_in_prof"] = d.inprof.mean()
    return out

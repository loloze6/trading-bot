def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "r1n": c.shift(-1)/c - 1})
            for L in (24, 72):
                df[f"z{L}"] = (c/c.shift(L) - 1) / (sd*np.sqrt(L))
            for h in (1, 4, 24, 72):
                df[f"f{h}"] = c.shift(-h)/c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (1, 4, 24, 72):
        dr = d[d.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(dr)
    def tt(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    # reversal: graded, per coin, per half
    res = []
    for L, h in ((24, 24), (72, 72), (24, 72)):
        g = d[d.pos % h == 0].dropna(subset=[f"z{L}", f"u{h}"])
        for key, gg in [("all", g)] + [(c, x) for c, x in g.groupby("coin")] + [("w1-12", g[g.wn <= 12]), ("w13-24", g[g.wn > 12])]:
            rho, p = stats.spearmanr(gg[f"z{L}"], gg[f"u{h}"])
            sl = np.polyfit(gg[f"z{L}"], gg[f"u{h}"], 1)[0]
            res.append({"past": L, "h": h, "grp": key, "n": len(gg), "rho": rho, "p": p, "slope_bp_per_z": sl*1e4})
    out["reversal graded"] = pd.DataFrame(res)
    g = d[d.pos % 24 == 0].dropna(subset=["z24", "u24"])
    q = pd.qcut(g.z24, 5)
    out["u24 by z24 quintile by coin"] = g.groupby([q, "coin"], observed=True)["u24"].mean().unstack()*1e4
    # hour 20-21 effect by year and coin, and 4h after 20:00
    g1 = d.dropna(subset=["u1"])
    e = g1[g1.hour.isin([20, 21])]
    out["u1 hours20-21 by year"] = e.groupby("yr")["u1"].apply(tt).unstack()
    out["u1 hours20-21 by half"] = e.groupby(e.wn > 12)["u1"].apply(tt).unstack()
    n0 = g1[g1.hour.isin([0, 1, 2])]
    out["u1 hours0-2 by year"] = n0.groupby("yr")["u1"].apply(tt).unstack()
    th = g1[g1.wd == 3]
    out["u1 thursday by year"] = th.groupby("yr")["u1"].apply(tt).unstack()
    # book: position and market rise
    d["gain"] = d.alloc * d.r1n
    mr = d.groupby("coin")["r1n"].mean()
    d["mkt"] = d.alloc * d["coin"].map(mr)
    out["book hourly decomposition bp"] = d.groupby("coin")[["gain", "mkt", "alloc"]].mean().assign(gain=lambda x: x.gain*1e4, mkt=lambda x: x.mkt*1e4)
    out["share of bars short"] = d.groupby("coin")["alloc"].apply(lambda x: (x < -0.01).mean())
    return out

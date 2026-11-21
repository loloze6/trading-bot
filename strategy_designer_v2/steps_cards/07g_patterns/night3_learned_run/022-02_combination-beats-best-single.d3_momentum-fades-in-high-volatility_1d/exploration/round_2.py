def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["wn"] = int(w[1:])
            df["vol30"] = r1.rolling(30, min_periods=20).std()
            for L in [1, 7, 14, 28]:
                df[f"z{L}"] = (c / c.shift(L) - 1) / (df["vol30"] * np.sqrt(L))
            ts = pd.to_datetime(b["timestamp"])
            df["wd"] = ts.dt.dayofweek
            df["yr"] = ts.dt.year
            for h in [1, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in [1, 5, 10]:
        g = D[D.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean(); sd = g.groupby("coin")[f"f{h}"].std()
        D[f"dr{h}"] = D.coin.map(dr); D[f"sd{h}"] = D.coin.map(sd)
    out = {}
    # size of momentum (z14) at 10 days: cases = sign of z14 on grid; graded by |z14| tercile
    res = []
    for s in ["z7", "z14", "z28"]:
        for h in [5, 10]:
            g = D[D.pos % h == 0].dropna(subset=[s, f"f{h}"]).copy()
            sg = np.sign(g[s])
            g["unus"] = sg * (g[f"f{h}"] - g[f"dr{h}"])
            g["tot"] = sg * g[f"f{h}"]
            g["str"] = g["unus"] / g[f"sd{h}"]
            g["mag"] = pd.qcut(g[s].abs(), 3, labels=False)
            for m, gg in g.groupby("mag"):
                res.append([s, h, m, len(gg), gg.unus.mean() * 1e4, gg.tot.mean() * 1e4, gg["str"].mean(),
                            gg.unus.mean() / (gg.unus.std() / np.sqrt(len(gg)))])
            g["half"] = np.where(g.wn <= 12, "early", "late")
            for hf, gg in g.groupby("half"):
                res.append([s, h, hf, len(gg), gg.unus.mean() * 1e4, gg.tot.mean() * 1e4, gg["str"].mean(),
                            gg.unus.mean() / (gg.unus.std() / np.sqrt(len(gg)))])
    out["mom_size"] = pd.DataFrame(res, columns=["sig", "h", "grp", "n", "unus_bps", "tot_bps", "strength", "t"])
    # 1-day reversal by coin and half: product of -sign(z1) * excess next day, size in bps by |z1| tercile
    g = D.dropna(subset=["z1", "f1"]).copy()
    g["unus"] = -np.sign(g.z1) * (g.f1 - g.dr1)
    g["mag"] = pd.qcut(g.z1.abs(), 3, labels=False)
    out["rev1_by_mag"] = g.groupby("mag").unus.agg(["count", "mean"]).assign(bps=lambda x: x["mean"] * 1e4)
    out["rev1_top_by_coin"] = g[g.mag == 2].groupby("coin").unus.agg(lambda x: x.mean() * 1e4)
    out["rev1_top_by_half"] = g[g.mag == 2].groupby(np.where(g[g.mag == 2].wn <= 12, "early", "late")).unus.agg(["count", lambda x: x.mean() * 1e4, lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # weekday excess by coin sign and by half
    g = D.dropna(subset=["f1"]).copy(); g["e1"] = g.f1 - g.dr1
    piv = g.groupby(["wd", "coin"]).e1.mean().unstack() * 1e4
    piv["half_early"] = g[g.wn <= 12].groupby("wd").e1.mean() * 1e4
    piv["half_late"] = g[g.wn > 12].groupby("wd").e1.mean() * 1e4
    out["weekday_coin_half"] = piv.round(1)
    return out

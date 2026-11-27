def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            ret1 = c.pct_change()
            for h in (3, 5, 10):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["r3"] = c / c.shift(3) - 1
            b["r10"] = c / c.shift(10) - 1
            b["lowdist"] = c / c.rolling(30, min_periods=10).min() - 1
            b["depth"] = c / c.rolling(30, min_periods=10).max() - 1
            b["volrel"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            b["sd30"] = ret1.rolling(30, min_periods=15).std()
            b["r3z"] = b["r3"] / (b["sd30"] * np.sqrt(3))
            b["r10z"] = b["r10"] / (b["sd30"] * np.sqrt(10))
            b["inprof"] = (b["regime"] == "unknown").values
            b["coin"] = coin; b["win"] = w
            b["day"] = ts.dt.floor("D")
            b["year"] = ts.dt.year
            b["pos"] = np.arange(n)
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    def clslope(x, y, g):
        x = x - x.mean(); 
        beta = (x * (y - y.mean())).sum() / (x * x).sum()
        e = (y - y.mean()) - beta * x
        s = pd.Series(x * e).groupby(g.values).sum()
        G = len(s)
        var = (s ** 2).sum() / (x * x).sum() ** 2 * G / (G - 1)
        return beta, beta / np.sqrt(var), G
    res = {}
    for h in (3, 5, 10):
        g = df[(df.pos % h == 0) & df[f"f{h}"].notna()].copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift)
        p = g[g.inprof]
        for f in ["r3", "r3z", "r10", "r10z", "lowdist", "depth", "volrel"]:
            q = p[[f, "ex", "day", "coin", "year"]].dropna()
            b_, t_, G = clslope(q[f].values, q.ex.values, q.day)
            pc = q.groupby("coin").apply(lambda z: stats.spearmanr(z[f], z.ex)[0] if len(z) > 8 else np.nan)
            early = q[q.year <= 2019]; late = q[q.year > 2019]
            re = stats.spearmanr(early[f], early.ex)[0] if len(early) > 8 else np.nan
            rl = stats.spearmanr(late[f], late.ex)[0] if len(late) > 8 else np.nan
            res[f"h{h}_{f}"] = {"slope": b_, "t": t_, "days": G, "n": len(q),
                                "rho_BTC": pc.get("BTCUSD"), "rho_XMR": pc.get("XMRUSD"), "rho_DOGE": pc.get("DOGEUSD"),
                                "rho_to2019": re, "rho_after2019": rl}
    out["slopes"] = pd.DataFrame(res).T
    # out of profile comparison for r3 at h3
    g = df[(df.pos % 3 == 0) & df.f3.notna()].copy()
    drift = g.groupby("coin").f3.mean(); g["ex"] = g.f3 - g.coin.map(drift)
    o = g[~g.inprof][["r3z", "ex", "day"]].dropna()
    b_, t_, G = clslope(o.r3z.values, o.ex.values, o.day)
    out["outprof_h3_r3z"] = pd.Series({"slope": b_, "t": t_, "days": G})
    # book's largest days in profile: preceding r3z
    return out

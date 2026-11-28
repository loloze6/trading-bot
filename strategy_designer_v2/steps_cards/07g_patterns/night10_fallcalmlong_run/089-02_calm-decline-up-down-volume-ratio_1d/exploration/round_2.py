def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            for h in [3, 5, 10]:
                b[f"fwd{h}"] = c.shift(-h) / c - 1
            b["past5"] = c / c.shift(5) - 1
            for L in [10, 20, 40]:
                b[f"lo{L}"] = c / b["low"].rolling(L).min() - 1
                b[f"loz{L}"] = np.log(c / b["low"].rolling(L).min()) / (vol20 * np.sqrt(L))
            b["ratio"] = b.get("debug_info.components.updown_vol.last_history_value")
            b["inp"] = b["regime"] == "unknown"
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["pos"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows)
    out = {}
    res = []
    for h in [3, 5, 10]:
        G = B[B["pos"] % h == 0].copy()
        drift = G.groupby("coin")[f"fwd{h}"].mean()
        G["ex"] = G[f"fwd{h}"] - G["coin"].map(drift)
        for grp, S in [("in", G[G.inp]), ("out", G[~G.inp])]:
            for f in ["lo10", "lo20", "lo40", "loz10", "loz20", "loz40", "past5", "ratio"]:
                d = S[[f, "ex", "day"]].dropna()
                if len(d) < 30: continue
                rho, p = stats.spearmanr(d[f], d["ex"])
                # slope t clustered by day on rank
                x = d[f].rank(pct=True) - 0.5
                y = d["ex"]
                beta = (x * y).sum() / (x * x).sum()
                e = (x * (y - beta * x)).groupby(d["day"]).sum()
                se = np.sqrt((e ** 2).sum()) / (x * x).sum()
                res.append([h, grp, f, len(d), round(rho, 3), round(p, 3), round(beta / se, 2)])
    out["rank slope by horizon, in/out of profile"] = pd.DataFrame(res, columns=["h", "grp", "f", "n", "rho", "p", "t_clu"])
    G = B[(B["pos"] % 5 == 0) & B.inp].copy()
    drift = B[B["pos"] % 5 == 0].groupby("coin")["fwd5"].mean()
    G["ex"] = G["fwd5"] - G["coin"].map(drift)
    d = G[["lo20", "ex", "coin", "year", "win"]].dropna()
    d["q"] = pd.qcut(d["lo20"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["lo20 terciles by coin"] = d.pivot_table(index="coin", columns="q", values="ex", aggfunc="mean")
    out["lo20 terciles by year"] = d.pivot_table(index="year", columns="q", values="ex", aggfunc="mean")
    out["lo20 tercile count/mean/ranges"] = d.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), lo20_mean=("lo20", "mean"))
    out["lo20 rho by coin"] = d.groupby("coin").apply(lambda s: stats.spearmanr(s.lo20, s.ex)[0] if len(s) > 8 else np.nan)
    return out

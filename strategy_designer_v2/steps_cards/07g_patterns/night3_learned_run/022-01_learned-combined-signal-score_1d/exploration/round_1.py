def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            ret28 = c / c.shift(28) - 1
            hi90 = c.rolling(90, min_periods=30).max()
            near = c / hi90
            vol30 = r1.rolling(30, min_periods=20).std()
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": r1, "ret28": ret28, "near": near, "vol30": vol30,
                "fwd5": fwd5, "fwd1": fwd1, "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # coin drift (5d grid, all windows) and usual move
    G = D[(D["pos"] % 5 == 0) & D["fwd5"].notna()].copy()
    drift = G.groupby("coin")["fwd5"].mean(); sd = G.groupby("coin")["fwd5"].std()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    G["z5"] = G["ex5"] / G["coin"].map(sd)
    out = {}
    # per-signal: rank by within-coin quintile, mean excess 5d return
    def quint(col):
        g = G.dropna(subset=[col]).copy()
        g["q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = g.groupby("q")["z5"].agg(["mean", "count"])
        t["t"] = g.groupby("q")["z5"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        # rank correlation pooled within coin
        cs = g.groupby("coin").apply(lambda x: stats.spearmanr(x[col], x["ex5"])[0])
        t.loc["spearman_mean_over_coins", "mean"] = cs.mean()
        return t
    for col in ["ret28", "r1", "near", "vol30", "fc"]:
        out["quintile z5 by " + col] = quint(col)
    # per-coin spearman per signal
    cc = {}
    for col in ["ret28", "r1", "near", "vol30", "fc"]:
        g = G.dropna(subset=[col])
        cc[col] = g.groupby("coin").apply(lambda x: stats.spearmanr(x[col], x["ex5"])[0])
    out["spearman by coin"] = pd.DataFrame(cc)
    # per year spearman per signal (pooled)
    cy = {}
    for col in ["ret28", "r1", "near", "vol30", "fc"]:
        g = G.dropna(subset=[col])
        cy[col] = g.groupby("yr").apply(lambda x: stats.spearmanr(x[col], x["ex5"])[0])
    cy["n"] = G.groupby("yr").size()
    out["spearman by year"] = pd.DataFrame(cy)
    # weekday daily returns
    d1 = D.dropna(subset=["fwd1"])
    wd = d1.groupby("wd")["fwd1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["next-day return by weekday of signal bar"] = wd
    # after large 1d moves: next 5d excess (grid), by |r1| sign
    g = G.dropna(subset=["r1"]).copy()
    g["r1z"] = g["r1"] / g["coin"].map(D.groupby("coin")["r1"].std())
    g["bin"] = pd.cut(g["r1z"], [-99, -2, -1, 0, 1, 2, 99])
    t = g.groupby("bin")["z5"].agg(["mean", "count"]); 
    t["t"] = g.groupby("bin")["z5"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["z5 after 1d move size"] = t
    # forecast sign vs position sign agreement, and book days
    allD = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            allD.append(dd.assign(coin=coin, win=w))
    DD = pd.concat(allD, ignore_index=True)
    out["book mean daily by coin"] = DD.groupby("coin")[["book_return", "coin_return"]].mean()
    D["absfc"] = D["fc"].abs()
    out["share long / short / flat"] = pd.Series({"long": (D.alloc > 0.001).mean(), "short": (D.alloc < -0.001).mean(), "flat": (D.alloc.abs() <= 0.001).mean()})
    return out

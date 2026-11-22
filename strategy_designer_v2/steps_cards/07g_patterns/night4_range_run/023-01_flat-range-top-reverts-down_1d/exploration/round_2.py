def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    for H in [5, 10]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
                mx = hi.rolling(30).max(); mn = lo.rolling(30).min(); rng = mx - mn
                sratio = (c - c.shift(29)) / rng
                rngpos = (c - mn) / rng
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(b), H)
                yr = pd.to_datetime(b["timestamp"]).dt.year.values[idx]
                rows.append(pd.DataFrame({"coin": coin, "win": w, "yr": yr,
                    "sratio": sratio.values[idx], "rngpos": rngpos.values[idx], "fwd": fwd.values[idx]}))
        g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
        cm = g.groupby("coin")["fwd"].agg(["mean", "std"])
        g["ex"] = (g["fwd"] - g["coin"].map(cm["mean"])) / g["coin"].map(cm["std"])
        g = g.dropna(subset=["sratio", "rngpos"])
        g["q"] = g.groupby("coin")["sratio"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = g.groupby("q")["ex"].agg(["mean", "std", "count"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        out[f"H{H}: signed net/range quintile -> strength"] = t[["mean", "t", "count"]]
        r, p = stats.spearmanr(g["sratio"], g["ex"])
        out[f"H{H}: spearman signed ratio"] = f"rho={r:.4f} p={p:.4f} n={len(g)}"
        if H == 5:
            g["agree"] = g["sratio"]  # continuation score
            pc = {}
            for coin, d in g.groupby("coin"):
                r, p = stats.spearmanr(d["sratio"], d["ex"]); pc[coin] = (round(r, 3), round(p, 3), len(d))
            out["H5 per coin spearman"] = pd.Series(pc).astype(str)
            py = {}
            for y, d in g.groupby("yr"):
                r, p = stats.spearmanr(d["sratio"], d["ex"]); py[y] = (round(r, 3), round(p, 3), len(d))
            out["H5 per year spearman"] = pd.Series(py).astype(str)
            # top/bottom quintile of rngpos within strong |ratio|
            s = g[g["sratio"].abs() > 0.33]
            r, p = stats.spearmanr(s["rngpos"], s["ex"])
            out["H5 trend only: rngpos spearman"] = f"rho={r:.4f} p={p:.4f} n={len(s)}"
            # OLS slope t
            sl = stats.linregress(g["sratio"], g["ex"])
            out["H5 OLS slope ex on sratio"] = f"slope={sl.slope:.4f} t={sl.slope/sl.stderr:.2f}"
    # weekday on daily coin returns
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["wd"] = pd.to_datetime(d["day"]).dt.weekday; dl.append(d)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["coin_return"])
    wt = D.groupby("wd")["coin_return"].agg(["mean", "std", "count"]); wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["weekday daily coin return"] = wt[["mean", "t", "count"]]
    return out

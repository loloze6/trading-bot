def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    # coin mean 20-bar return on grid
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 20, 20):
                rr.append(c[i + 20] / c[i] - 1)
        drift[coin] = np.mean(rr); usual[coin] = np.std(rr, ddof=1)
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            last = -999
            for t in range(60, n):
                if c[t] > c[t-60:t].max() and t - last >= 20:
                    last = t
                    pr20 = c[t-1] / c[t-21] - 1 if t >= 21 else np.nan
                    dist = c[t] / c[t-60:t].max() - 1
                    rng = c[t-60:t].max() / c[t-60:t].min() - 1
                    r = {}
                    for h in (5, 10, 20, 40):
                        r[h] = c[t+h] / c[t] - 1 if t + h < n else np.nan
                    rows.append(dict(coin=coin, w=w, pr20=pr20, dist=dist, rng=rng,
                                     fc=df["forecast"].iloc[t],
                                     **{f"f{h}": r[h] for h in r},
                                     x20=(r[20] - drift[coin]) if not np.isnan(r[20]) else np.nan))
    d = pd.DataFrame(rows).dropna(subset=["x20", "pr20"])
    out = {}
    out["n"] = len(d)
    d["q_pr"] = pd.qcut(d["pr20"].rank(method="first"), 4, labels=["q1low", "q2", "q3", "q4high"])
    out["by_prior_runup"] = d.groupby("q_pr")[["pr20", "f5", "f10", "f20", "f40", "x20"]].agg(["mean"]).round(4).assign(n=d.groupby("q_pr").size())
    d["q_dist"] = pd.qcut(d["dist"].rank(method="first"), 4, labels=["d1small", "d2", "d3", "d4large"])
    out["by_break_dist"] = d.groupby("q_dist")[["dist", "f5", "f10", "f20", "f40", "x20"]].mean().round(4).assign(n=d.groupby("q_dist").size())
    d["q_rng"] = pd.qcut(d["rng"].rank(method="first"), 3, labels=["narrow", "mid", "wide"])
    out["by_range_width"] = d.groupby("q_rng")[["rng", "f5", "f10", "f20", "x20"]].mean().round(4).assign(n=d.groupby("q_rng").size())
    def corr(g):
        if len(g) < 5: return pd.Series({"n": len(g)})
        s = stats.spearmanr(g["pr20"], g["x20"])
        return pd.Series({"n": len(g), "rho_pr_x20": round(s[0], 3), "mean_x20": round(g["x20"].mean(), 4)})
    out["by_coin"] = d.groupby("coin").apply(corr)
    out["by_window"] = d.groupby("w").apply(corr)
    for h in (5, 10, 20, 40):
        g = d.dropna(subset=[f"f{h}"])
        s = stats.spearmanr(g["pr20"], g[f"f{h}"])
        out[f"rho_pr_f{h}"] = f"{s[0]:.3f} p={s[1]:.3f} n={len(g)}"
        s = stats.spearmanr(g["dist"], g[f"f{h}"])
        out[f"rho_dist_f{h}"] = f"{s[0]:.3f} p={s[1]:.3f} n={len(g)}"
    out["x20_t_all"] = f"mean {d['x20'].mean():.4f} t {stats.ttest_1samp(d['x20'],0)[0]:.2f}"
    return out

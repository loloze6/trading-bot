def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}; usual = {}
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 20, 20):
                rr.append(c[i + 20] / c[i] - 1)
        drift[coin] = np.mean(rr); usual[coin] = np.std(rr, ddof=1)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            reg = df["regime"].values
            ru = df.get("debug_info.components.runup.last_history_value")
            ru = ru.values if ru is not None else np.full(n, np.nan)
            last = -999
            for t in range(n):
                if reg[t] == "trending" and t - last >= 20 and t + 20 < n:
                    last = t
                    k = min(t, 60)
                    if k >= 20:
                        pm = c[t-k:t].max(); pn = c[t-k:t].min()
                        dist = c[t] / pm - 1; rng = pm / pn - 1
                    else:
                        dist = np.nan; rng = np.nan
                    pr20 = c[t-1] / c[t-21] - 1 if t >= 21 else np.nan
                    rows.append(dict(coin=coin, w=w, t=t, dist=dist, rng=rng, pr20=pr20, ru=ru[t],
                                     fc=df["forecast"].iloc[t],
                                     f10=c[t+10]/c[t]-1, f20=c[t+20]/c[t]-1,
                                     x20=c[t+20]/c[t]-1-drift[coin],
                                     s20=(c[t+20]/c[t]-1-drift[coin])/usual[coin]))
    d = pd.DataFrame(rows)
    out = {"n_all": len(d), "n_with_dist": int(d["dist"].notna().sum())}
    out["x20_all"] = f"mean {d['x20'].mean():.4f} t {stats.ttest_1samp(d['x20'],0)[0]:.2f} n {len(d)}"
    g = d.dropna(subset=["dist"])
    g["qd"] = pd.qcut(g["dist"].rank(method="first"), 3, labels=["small", "mid", "large"])
    out["by_dist"] = g.groupby("qd")[["dist", "f10", "f20", "x20", "s20"]].mean().round(4).assign(n=g.groupby("qd").size())
    sm, lg = g[g.qd == "small"]["x20"], g[g.qd == "large"]["x20"]
    out["welch_small_minus_large_x20"] = f"{stats.ttest_ind(sm, lg, equal_var=False)[0]:.2f}"
    s = stats.spearmanr(g["dist"], g["x20"]); out["rho_dist_x20"] = f"{s[0]:.3f} p={s[1]:.3f} n={len(g)}"
    g2 = d.dropna(subset=["ru"])
    if len(g2) > 10:
        s = stats.spearmanr(g2["ru"], g2["x20"]); out["rho_runup_x20"] = f"{s[0]:.3f} p={s[1]:.3f} n={len(g2)}"
    g3 = d.dropna(subset=["fc"])
    s = stats.spearmanr(g3["fc"], g3["x20"]); out["rho_fc_x20"] = f"{s[0]:.3f} p={s[1]:.3f} n={len(g3)}"
    g3["qf"] = pd.qcut(g3["fc"].rank(method="first"), 2, labels=["low", "high"])
    out["by_fc_half"] = g3.groupby("qf")[["fc", "x20"]].mean().round(4).assign(n=g3.groupby("qf").size())
    def per(gg):
        if len(gg) < 5 or gg["dist"].notna().sum() < 5: return pd.Series({"n": len(gg), "mean_x20": round(gg["x20"].mean(), 4)})
        h = gg.dropna(subset=["dist"])
        return pd.Series({"n": len(gg), "mean_x20": round(gg["x20"].mean(), 4), "rho_dist": round(stats.spearmanr(h["dist"], h["x20"])[0], 3)})
    out["by_coin"] = d.groupby("coin").apply(per)
    out["by_window"] = d.groupby("w").apply(per)
    g["qr"] = pd.qcut(g["rng"].rank(method="first"), 2, labels=["narrow", "wide"])
    out["dist_x_range"] = g.groupby(["qr", "qd"])["x20"].agg(["mean", "count"]).round(4)
    return out

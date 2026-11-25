def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    drift = {h: {} for h in (1, 2, 3, 5)}
    for coin, wins in bars.items():
        for h in (1, 2, 3, 5):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i+h]/c[i]-1)
            drift[h][coin] = np.mean(rr)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values; hi = df["high"].values
            n = len(df)
            rngpct = pd.Series((hi - lo) / c)
            ratio = (rngpct.rolling(30, min_periods=30).mean() / rngpct.rolling(365, min_periods=120).mean()).values
            prior_low = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            ret30 = pd.Series(c).pct_change(30).values
            reg = (df["regime"] == "mean_reversion").values
            fc = df["forecast"].fillna(0).values
            for t in range(n):
                if np.isnan(prior_low[t]) or not c[t] < prior_low[t]:
                    continue
                rec = {"coin": coin, "w": w, "t": t, "reg": reg[t], "fc": fc[t],
                       "depth": c[t]/prior_low[t]-1, "ratio": ratio[t], "ret30": ret30[t],
                       "day": str(pd.Timestamp(df["timestamp"].iloc[t]).date())}
                for h in (1, 2, 3, 5):
                    rec[f"u{h}"] = (c[t+h]/c[t]-1 - drift[h][coin]) if t+h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def clus(g, col):
        x = g[["day", col]].dropna()
        if len(x) < 3: return (len(x), np.nan, np.nan, np.nan)
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        G = len(s)
        se = np.sqrt((s**2).sum() * G/(G-1)) / len(x) if G > 1 else np.nan
        return (len(x), m, x[col].median(), m/se)

    def tab(g):
        res = {}
        for col in ("u1", "u2", "u3", "u5"):
            n, m, med, t = clus(g, col)
            res[f"n_{col}"] = n; res[f"mean_{col}"] = m; res[f"t_{col}"] = t
        return pd.Series(res)

    # every break-bar (overlapping across h but each bar once), regime vs not
    out["breaks all bars: regime vs not (day-clustered)"] = d.groupby("reg").apply(tab)
    # first break-bar of each break episode (a fresh break: prior bar not a break)
    d = d.sort_values(["coin", "w", "t"])
    d["fresh"] = ~((d.groupby(["coin", "w"])["t"].diff() == 1))
    F = d[d.fresh]
    out["fresh breaks: regime vs not"] = F.groupby("reg").apply(tab)
    out["fresh breaks all"] = tab(F)
    # graded by range ratio (wider month vs year), among fresh breaks with ret30<0
    G = F[(F.ret30 < 0) & F.ratio.notna()].copy()
    G["ratio_q"] = pd.qcut(G["ratio"].rank(method="first"), 3, labels=["narrow", "mid", "wide"])
    out["fresh breaks ret30<0 by range-ratio tercile"] = G.groupby("ratio_q").apply(tab)
    G["dq"] = pd.qcut(G["depth"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["fresh breaks ret30<0 by depth tercile"] = G.groupby("dq").apply(tab)
    W = G[G.ratio_q == "wide"].copy()
    W["dq"] = pd.qcut(W["depth"].rank(method="first"), 2, labels=["deeper", "shallower"])
    out["wide-range fresh breaks by depth half"] = W.groupby("dq").apply(tab)
    R = d[d.reg]
    out["regime bars by coin u1"] = R.groupby("coin").apply(tab)[["n_u1", "mean_u1", "t_u1", "mean_u5"]]
    out["corr u1 with ratio (fresh, ret30<0)"] = float(G[["u1", "ratio"]].corr().iloc[0, 1])
    out["corr u5 with ratio (fresh, ret30<0)"] = float(G[["u5", "ratio"]].corr().iloc[0, 1])
    out["corr u1 with depth (regime bars)"] = float(R[["u1", "depth"]].corr().iloc[0, 1])
    return out

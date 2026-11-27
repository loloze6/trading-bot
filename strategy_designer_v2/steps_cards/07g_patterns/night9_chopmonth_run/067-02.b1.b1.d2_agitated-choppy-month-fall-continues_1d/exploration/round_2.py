def explore(data):
    import numpy as np, pandas as pd
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "r14": c / c.shift(14) - 1,
                "vol30": r1.rolling(30).std(),
                "fwd": c.shift(-H) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "regime": b["regime"].values,
            })
            df["pos"] = np.arange(len(df))
            df["vrank"] = df["vol30"].rolling(90, min_periods=45).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % H == 0)].dropna(subset=["fwd"]).copy()
    drift = G.groupby("coin")["fwd"].mean()
    usual = G.groupby("coin")["fwd"].std()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    G["day"] = G["ts"].dt.floor("D")
    G["yr"] = G["ts"].dt.year
    G = G.dropna(subset=["r60", "r30"])
    G["trend"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
    G["agit"] = np.where(G.vrank > 0.5, "agit", "calm")
    G.loc[G.vrank.isna(), "agit"] = "na"
    G["sd"] = np.sign(G.r30)

    def summ(g, col="ex"):
        d = g.groupby("day")[col].sum()
        n = len(d)
        t = d.mean() / (d.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": len(g), "days": n, "mean_ex": g[col].mean(), "t_day": t})

    def slope(g, x="r30"):
        # signed product: ex * r30 standardized, day clustered
        z = (g[x] - g[x].mean()) / g[x].std()
        p = (g.ex * z)
        d = p.groupby(g.day).sum()
        n = len(d)
        t = d.mean() / (d.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": len(g), "days": n, "cov": p.mean(), "corr": g[x].corr(g.ex), "t_day": t})

    out = {}
    out["slope r30 by trend"] = G.groupby("trend").apply(slope)
    out["slope r30 by trend x agit"] = G[G.agit != "na"].groupby(["trend", "agit"]).apply(slope)
    out["choppy sign x agit"] = G[(G.trend == "choppy") & (G.agit != "na")].groupby(["agit", "sd"]).apply(summ)
    out["rising sign x agit"] = G[(G.trend == "rising") & (G.agit != "na")].groupby(["agit", "sd"]).apply(summ)
    R = G[(G.trend == "rising") & (G.sd < 0)].copy()
    R["q"] = pd.qcut(R.r30, 3, labels=False)
    out["rising, r30<0, tercile"] = R.groupby("q").apply(summ)
    out["rising r30<0 by year"] = R.groupby("yr").apply(summ)
    out["rising r30<0 by window"] = R.groupby("win").apply(summ)
    C = G[G.trend == "choppy"].copy()
    out["choppy slope by year"] = C.groupby("yr").apply(slope)
    out["choppy slope by coin"] = C.groupby("coin").apply(slope)
    # gap: r30 vs r60 disagreement (r60 - r30 = older month)
    G["old"] = (1 + G.r60) / (1 + G.r30) - 1
    out["slope older month by trend"] = G.groupby("trend").apply(lambda g: slope(g, "old"))
    out["slope r14 by trend"] = G.dropna(subset=["r14"]).groupby("trend").apply(lambda g: slope(g, "r14"))
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            n = len(b)
            fwd3 = c.shift(-3) / c - 1
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            r3p = c / c.shift(3) - 1
            r1d = r1
            rng = (b["high"] - b["low"]).astype(float)
            cl = (c - b["low"]) / rng.replace(0, np.nan)
            low20 = b["low"].rolling(20, min_periods=10).min()
            high20 = b["high"].rolling(20, min_periods=10).max()
            pos20 = (c - low20) / (high20 - low20).replace(0, np.nan)
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(20, min_periods=10).mean()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "fwd3": fwd3, "s7": r7 / (sd30 * np.sqrt(7)), "s3": r3p / (sd30 * np.sqrt(3)),
                "s1": r1d / sd30, "cl": cl, "pos20": pos20, "vrel": vrel,
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "infc": (b["regime"] == "unknown"),
                "fc": b["forecast"].astype(float),
                "rngs": (rng / c) / sd30,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[(D["pos"] % 3 == 0) & D["fwd3"].notna()].copy()
    drift = G.groupby("coin")["fwd3"].mean()
    G["unus"] = G["fwd3"] - G["coin"].map(drift)
    F = G[G["infc"]].copy()
    out = {}
    out["counts"] = pd.Series({"grid_all": len(G), "grid_fallcalm": len(F),
                               "fallcalm_mean_unus": F["unus"].mean(),
                               "t": F["unus"].mean() / (F["unus"].std() / np.sqrt(len(F)))})
    def bucket(col, q=5):
        x = F[[col, "unus"]].dropna()
        x["b"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        g = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("unus", "size"),
                               mean=("unus", "mean"), sd=("unus", "std"))
        g["t"] = g["mean"] / (g["sd"] / np.sqrt(g["n"]))
        return g.drop(columns="sd")
    for col in ["s7", "s3", "s1", "cl", "pos20", "vrel", "rngs"]:
        out["q_" + col] = bucket(col)
    g = F.groupby("wd")["unus"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["weekday"] = g
    g = F.groupby("year")["unus"].agg(["size", "mean"]); out["year"] = g
    g = F.groupby("coin")["unus"].agg(["size", "mean"]); out["coin"] = g
    # forecast>0 vs ==0 inside profile
    F["fpos"] = F["fc"] > 0
    g = F.groupby("fpos")["unus"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["fc_pos"] = g
    # falls: s7<0 combined with close location
    x = F[F["s7"] < 0].dropna(subset=["cl"]).copy()
    x["clb"] = pd.qcut(x["cl"], 3, labels=False)
    g = x.groupby("clb")["unus"].agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["fall7_by_closeloc"] = g
    # book trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    if T:
        T = pd.concat(T)
        p = T["net_profit_loss_percent"].astype(float)
        out["trades"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(), "win": (p > 0).mean(),
                                   "top5_share": p.nlargest(5).sum() / p.sum() if p.sum() != 0 else np.nan,
                                   "dur_days_mean": T["duration_minutes"].astype(float).mean() / 1440})
        T["efb"] = pd.qcut(T["entry_forecast"].astype(float).rank(method="first"), 3, labels=False)
        out["trades_by_entryfc"] = T.groupby("efb")["net_profit_loss_percent"].agg(["size", "mean"])
    return out

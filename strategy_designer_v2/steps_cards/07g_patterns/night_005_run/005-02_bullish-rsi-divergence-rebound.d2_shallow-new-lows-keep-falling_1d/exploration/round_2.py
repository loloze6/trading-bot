def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": r1, "z1": r1 / vol20.shift(1),
                "r3p": c / c.shift(3) - 1,
                "r30p": c / c.shift(30) - 1,
                "r30z": (c / c.shift(30) - 1) / (vol20 * np.sqrt(30)),
                "vol20": vol20,
                "volratio": r1.rolling(5).std() / r1.rolling(30).std(),
                "rng": (h - l) / c,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "f10": c.shift(-10) / c - 1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def grid(hh):
        return A[(A["pos"] % hh == 0)].dropna(subset=[f"f{hh}"])

    def slope(feat, hh):
        res = []
        g = grid(hh).dropna(subset=[feat])
        for coin, gg in list(g.groupby("coin")) + [("pooled", g)]:
            y = gg[f"f{hh}"] - gg.groupby("coin")[f"f{hh}"].transform("mean")
            x = gg[feat].rank(pct=True)
            sl = stats.linregress(x, y)
            res.append({"coin": coin, "n": len(gg), "slope": sl.slope, "t": sl.slope / sl.stderr,
                        "spearman": stats.spearmanr(gg[feat], y)[0]})
        return pd.DataFrame(res)

    for feat, hh in [("z1", 1), ("z1", 3), ("r1", 3), ("r3p", 3), ("r30p", 10), ("r30z", 10),
                     ("vol20", 10), ("volratio", 5), ("rng", 1), ("rng", 5), ("clv", 1), ("clv", 3)]:
        out[f"slope_{feat}_f{hh}"] = slope(feat, hh)

    # r30p deciles pooled f10
    g = grid(10).dropna(subset=["r30p"]).copy()
    g["ex"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
    g["q"] = g.groupby("coin")["r30p"].transform(lambda s: pd.qcut(s, 10, labels=False))
    t = g.groupby("q")["ex"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["r30p_dec_f10_pooled"] = t

    # z1 deciles pooled f1, f3 on grid 3
    g = grid(3).dropna(subset=["z1"]).copy()
    g["ex"] = g["f3"] - g.groupby("coin")["f3"].transform("mean")
    g["q"] = g.groupby("coin")["z1"].transform(lambda s: pd.qcut(s, 10, labels=False))
    t = g.groupby("q")["ex"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["z1_dec_f3_pooled"] = t

    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    out["trades"] = T.groupby("coin").agg(n=("side", "count"), mean_pl=("net_profit_loss_percent", "mean"),
                                          hit=("net_profit_loss_percent", lambda s: (s > 0).mean()),
                                          dur_days=("duration_minutes", lambda s: s.mean() / 1440))
    T["fq"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
    out["trades_by_fq"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean"])
    return out

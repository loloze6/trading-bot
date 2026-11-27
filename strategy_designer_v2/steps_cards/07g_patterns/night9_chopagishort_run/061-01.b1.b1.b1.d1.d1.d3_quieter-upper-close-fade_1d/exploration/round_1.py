def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "rng": (h - l) / c,
                "r1": r1,
                "r5p": c / c.shift(5) - 1,
                "r20p": c / c.shift(20) - 1,
                "tr60": c / c.shift(60) - 1,
                "vol20": r1.rolling(20).std(),
                "vol60": r1.rolling(60).std(),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "reg": b["regime"].values,
                "fc": b["forecast"].values,
                "alloc": b["postRebalance_current_allocation"].values,
            })
            df["vr"] = df["vol20"] / df["vol60"]
            df["z1"] = df["r1"] / df["vol60"]
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift5 = D[D.pos % 5 == 0].groupby("coin")["f5"].mean()
    drift2 = D[D.pos % 2 == 0].groupby("coin")["f2"].mean()
    drift1 = D.groupby("coin")["f1"].mean()
    D["u5"] = D["f5"] - D["coin"].map(drift5)
    D["u2"] = D["f2"] - D["coin"].map(drift2)
    D["u1"] = D["f1"] - D["coin"].map(drift1)
    G5 = D[D.pos % 5 == 0].dropna(subset=["u5"])
    G2 = D[D.pos % 2 == 0].dropna(subset=["u2"])

    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    G5 = G5.copy()
    G5["trend"] = pd.cut(G5["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G5["clvq"] = pd.cut(G5["clv"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1", "q2", "q3", "q4"])
    G5["r5s"] = np.where(G5["r5p"] < 0, "r5neg", "r5pos")
    out["u5 by trend x clv"] = G5.groupby(["trend", "clvq"]).apply(lambda g: summ(g, "u5")).round(4)
    out["u5 chop by clv x r5sign"] = G5[G5.trend == "chop"].groupby(["r5s", "clvq"]).apply(lambda g: summ(g, "u5")).round(4)
    G5["vrq"] = pd.qcut(G5["vr"], 4, labels=["v1", "v2", "v3", "v4"])
    out["u5 by vr quartile x trend"] = G5.groupby(["trend", "vrq"]).apply(lambda g: summ(g, "u5")).round(4)
    G2 = G2.copy()
    G2["zq"] = pd.cut(G2["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["u2 by 1d move z"] = G2.groupby("zq").apply(lambda g: summ(g, "u2")).round(4)
    G2["r20q"] = pd.qcut(G2["r20p"], 5)
    out["u5 by 20d return quintile"] = G5.assign(r20q=pd.qcut(G5["r20p"], 5)).groupby("r20q").apply(lambda g: summ(g, "u5")).round(4)
    out["u1 by weekday"] = D.dropna(subset=["u1"]).groupby("wd").apply(lambda g: summ(g, "u1")).round(4)
    A = D[D.reg == "mean_reversion"].copy()
    out["regime bars count / by year"] = A.groupby("year").size()
    T = []
    for coin, wins in trades.items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin, win=w))
    T = pd.concat(T, ignore_index=True)
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades by year"] = T.groupby("year")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=["low", "mid", "high"], duplicates="drop")
    out["trades by |entry fc| tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    out["trades by duration days"] = T.assign(d=(T.duration_minutes / 1440).round()).groupby("d")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    return out

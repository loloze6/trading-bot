def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    trades = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f1 = c.shift(-1) / c - 1
            f10 = c.shift(-10) / c - 1
            vol20 = r1.rolling(20).std()
            pos20 = (c - c.rolling(20).min()) / (c.rolling(20).max() - c.rolling(20).min())
            d = pd.DataFrame({
                "coin": coin, "w": w, "i": np.arange(len(b)),
                "fc": b["forecast"].astype(float), "reg": b["regime"].astype(str),
                "r1": r1, "f1": f1, "f10": f10, "vol20": vol20, "pos20": pos20,
                "z": r1 / vol20.shift(1),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "sh": b.get("debug_info.components.since_high.last_history_value", pd.Series(np.nan, index=b.index)).astype(float),
            })
            rows.append(d)
        for w, t in data["trades"][coin].items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; trades.append(t)
    D = pd.concat(rows, ignore_index=True)
    T = pd.concat(trades, ignore_index=True)

    def agg(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "hit": (x > 0).mean()})

    out = {}
    out["fc_dist"] = D["fc"].describe()
    out["sh_values"] = D["sh"].value_counts().sort_index().head(25)
    out["fc_bucket_f1"] = D.groupby(pd.cut(D["fc"], [-21, -0.01, 0.01, 5, 10, 15, 21])).apply(lambda g: agg(g, "f1"))
    D10 = D[D["i"] % 10 == 0]
    out["fc_bucket_f10_nonov"] = D10.groupby(pd.cut(D10["fc"], [-21, -0.01, 0.01, 5, 10, 15, 21])).apply(lambda g: agg(g, "f10"))
    out["pos20_f10_nonov"] = D10.groupby(pd.cut(D10["pos20"], [-0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1.0])).apply(lambda g: agg(g, "f10"))
    out["z_f1"] = D.groupby(pd.cut(D["z"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])).apply(lambda g: agg(g, "f1"))
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["volq_f10_nonov"] = D[D["i"] % 10 == 0].groupby("vq").apply(lambda g: agg(g, "f10"))
    out["weekday_f1"] = D.groupby("wd").apply(lambda g: agg(g, "f1"))
    out["regime_f1"] = D.groupby("reg").apply(lambda g: agg(g, "f1"))
    out["regime_fc_active"] = D.groupby("reg")["fc"].apply(lambda s: (s != 0).mean())
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_dur"] = T.groupby(pd.cut(T["dur_d"], [0, 1.5, 3.5, 7.5, 15, 1000]))["net_profit_loss_percent"].agg(["count", "mean", "median", lambda s: (s > 0).mean()])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    return out

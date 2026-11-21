def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [12, 24, 48]
    rows = []
    for coin, wins in data["bars"].items():
        for h in H:
            grid = []
            for w, df in wins.items():
                c = df["close"].astype(float).reset_index(drop=True)
                r24 = c / c.shift(24) - 1
                sc = r24.abs().rolling(720, min_periods=120).mean().shift(1)
                z = r24 / sc
                r6 = c / c.shift(6) - 1
                fwd = c.shift(-h) / c - 1
                ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
                idx = np.arange(0, len(c), h)
                g = pd.DataFrame({"z": z.iloc[idx].values, "r6s": (r6 / sc).iloc[idx].values,
                                  "f": fwd.iloc[idx].values,
                                  "yr": ts.iloc[idx].dt.year.values,
                                  "hr": ts.iloc[idx].dt.hour.values, "win": w})
                grid.append(g)
            g = pd.concat(grid).dropna(subset=["f"])
            drift, sd = g["f"].mean(), g["f"].std()
            g = g.dropna(subset=["z"])
            g["u"] = g["f"] - drift
            g["s"] = g["u"] / sd
            g["coin"] = coin; g["h"] = h
            rows.append(g)
    A = pd.concat(rows)
    def agg(x):
        n = len(x); m = x["u"].mean(); s = x["u"].std()
        return pd.Series({"n": n, "unusual_bps": m * 1e4, "total_bps": x["f"].mean() * 1e4,
                          "strength": x["s"].mean(), "t": m / (s / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    A["zb"] = pd.cut(A["z"], [-np.inf, -4, -3, -2.5, -2, -1, 0, np.inf])
    out["fine_bucket"] = A.groupby(["h", "zb"], observed=True).apply(agg).round(3)
    d3 = A[(A["h"] == 24) & (A["z"] <= -2.5)]
    out["drop25_h24_coin"] = d3.groupby("coin").apply(agg).round(3)
    out["drop25_h24_year"] = d3.groupby("yr").apply(agg).round(3)
    # where in the drop: recent 6h share of the fall
    d2 = A[(A["h"] == 24) & (A["z"] <= -2)].copy()
    d2["late"] = pd.cut(d2["r6s"] / d2["z"], [-np.inf, 0.33, 0.66, np.inf])
    out["drop2_h24_by_late_share"] = d2.groupby("late", observed=True).apply(agg).round(3)
    sp = {}
    for h in H:
        x = A[(A["h"] == h) & (A["z"] <= -1)]
        sp[h] = stats.spearmanr(-x["z"], x["u"]).correlation
    out["spearman_beyond1"] = pd.Series(sp).round(4)
    # book trades by entry forecast
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["fb"] = pd.cut(T["entry_forecast"].astype(float), [0, 3, 8, 15, 20.01])
    out["trades_by_entry_fc"] = T.groupby("fb", observed=True).agg(
        n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"),
        hours=("duration_minutes", lambda v: v.mean() / 60)).round(3)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [6, 24, 72, 168, 240]
    bins = [-np.inf, -3, -2, -1.5, -1, 0, 1, 1.5, 2, 3, np.inf]
    rows = []
    for coin, wins in data["bars"].items():
        for h in H:
            grid = []
            for w, df in wins.items():
                c = df["close"].astype(float).reset_index(drop=True)
                r24 = c / c.shift(24) - 1
                sc = r24.abs().rolling(720, min_periods=120).mean().shift(1)
                z = r24 / sc
                fwd = c.shift(-h) / c - 1
                ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
                idx = np.arange(0, len(c), h)
                g = pd.DataFrame({"z": z.iloc[idx].values, "f": fwd.iloc[idx].values,
                                  "yr": ts.iloc[idx].dt.year.values, "win": w})
                grid.append(g)
            g = pd.concat(grid).dropna(subset=["f"])
            drift, sd = g["f"].mean(), g["f"].std()
            g = g.dropna(subset=["z"])
            g["u"] = g["f"] - drift
            g["s"] = g["u"] / sd
            g["coin"] = coin; g["h"] = h; g["sd"] = sd; g["drift"] = drift
            rows.append(g)
    A = pd.concat(rows)
    A["zb"] = pd.cut(A["z"], bins)
    def agg(x):
        n = len(x); m = x["u"].mean(); s = x["u"].std()
        return pd.Series({"n": n, "unusual_bps": m * 1e4, "total_bps": x["f"].mean() * 1e4,
                          "strength": x["s"].mean(), "t": m / (s / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out["by_bucket_h"] = A.groupby(["h", "zb"], observed=True).apply(agg).round(3)
    big = A[A["z"] <= -2]
    out["drop2_by_coin_h"] = big[big["h"].isin([24, 168])].groupby(["h", "coin"]).apply(agg).round(3)
    out["drop2_by_year_h168"] = big[big["h"] == 168].groupby("yr").apply(agg).round(3)
    up = A[A["z"] >= 2]
    out["rise2_by_coin_h168"] = up[up["h"] == 168].groupby("coin").apply(agg).round(3)
    sp = {}
    for h in H:
        x = A[(A["h"] == h) & (A["z"] < 0)]
        sp[h] = stats.spearmanr(-x["z"], x["u"]).correlation
    out["spearman_drop_vs_u"] = pd.Series(sp).round(4)
    return out

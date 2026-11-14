def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df) - H, H):
                rows.append((coin, w, ts.iloc[i].year, f[i], c[i + H] / c[i] - 1))
    b = pd.DataFrame(rows, columns=["coin", "win", "year", "f", "r"])
    b["ex"] = b["r"] - b.groupby("coin")["r"].transform("mean")
    b["pos"] = (b["r"] > 0).astype(float)
    b["exp"] = b["pos"] - b.groupby("coin")["pos"].transform("mean")

    def slope(g):
        if len(g) < 8 or g["f"].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g["f"], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})

    out = {}
    out["pooled"] = slope(b)
    out["by_coin"] = b.groupby("coin").apply(slope)
    out["by_year"] = b.groupby("year").apply(slope)
    out["by_window"] = b.groupby("win").apply(slope)
    bins = [-0.01, 0, 5, 10, 15, 20.01]
    b["fb"] = pd.cut(b["f"], bins)
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(), "t_ex": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_r": g["r"].mean(), "sd_r": g["r"].std(), "pos_minus": g["exp"].mean()})
    out["by_fbucket"] = b.groupby("fb").apply(summ)
    out["by_coin_active_vs_flat"] = b.groupby(["coin", b["f"] > 0]).apply(summ)
    # market (equal-weight cross-coin) move: per year mean
    b["act"] = b["f"] > 0
    out["by_year_active_vs_flat"] = b.groupby(["year", "act"]).apply(summ)
    # does excess correlate with forecast within active only
    a = b[b["f"] > 0]
    out["active_only_slope"] = slope(a)
    return out

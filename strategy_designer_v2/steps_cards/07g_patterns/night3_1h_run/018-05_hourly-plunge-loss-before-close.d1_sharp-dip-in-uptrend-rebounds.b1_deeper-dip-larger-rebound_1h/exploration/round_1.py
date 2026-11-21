def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    rows24 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            ma = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / ma
            r30 = c / c.shift(720) - 1
            r7 = c / c.shift(168) - 1
            fwd = c.shift(-H) / c - 1
            fwd24 = c.shift(-24) / c - 1
            fc = b["forecast"].astype(float).reset_index(drop=True)
            idx = np.arange(0, len(c), H)
            d = pd.DataFrame({"coin": coin, "w": w, "z": z.iloc[idx].values, "r30": r30.iloc[idx].values,
                              "r7": r7.iloc[idx].values, "ma": ma.iloc[idx].values,
                              "fc": fc.iloc[idx].values, "fwd": fwd.iloc[idx].values})
            rows.append(d)
            idx2 = np.arange(0, len(c), 24)
            d2 = pd.DataFrame({"coin": coin, "z": z.iloc[idx2].values, "r30": r30.iloc[idx2].values,
                               "fwd": fwd24.iloc[idx2].values, "hour": ts.iloc[idx2].dt.hour.values,
                               "wd": ts.iloc[idx2].dt.weekday.values})
            rows24.append(d2)
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd"].transform("std")
    g["u"] = (g["fwd"] - g["drift"]) / g["sd"]
    gg = g.dropna(subset=["z", "r30"])
    gg["zbin"] = pd.qcut(gg["z"], 7, labels=False)
    gg["up30"] = np.where(gg["r30"] > 0, "up", "down")
    def summ(x):
        u = x["u"]; n = len(u)
        return pd.Series({"n": n, "mean_u": u.mean(), "t": u.mean() / (u.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "z_mid": x["z"].median()})
    out = {}
    out["z_bins_by_trend_72h_strength"] = gg.groupby(["up30", "zbin"]).apply(summ)
    gg["r30bin"] = pd.qcut(gg["r30"] / gg["ma"], 5, labels=False)
    out["r30_scaled_bins_72h"] = gg.groupby("r30bin").apply(lambda x: summ(x).drop("z_mid"))
    gg["r7bin"] = pd.qcut(gg["r7"] / gg["ma"], 5, labels=False)
    out["r7_scaled_bins_72h"] = gg.groupby("r7bin").apply(lambda x: summ(x).drop("z_mid"))
    gg["vbin"] = gg.groupby("coin")["ma"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["z_by_vol_tercile_corr"] = gg.groupby("vbin").apply(lambda x: pd.Series({"n": len(x), "spearman_z_u": stats.spearmanr(x["z"], x["u"])[0], "mean_u": x["u"].mean()}))
    out["z_corr_by_coin"] = gg.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "spearman_z_u": stats.spearmanr(x["z"], x["u"])[0]}))
    h = pd.concat(rows24).dropna(subset=["fwd"])
    h["u"] = (h["fwd"] - h.groupby("coin")["fwd"].transform("mean")) / h.groupby("coin")["fwd"].transform("std")
    out["24h_by_weekday"] = h.groupby("wd")["u"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = coin
            x["year"] = pd.to_datetime(d["day"]).dt.year.values
            dd.append(x)
    D = pd.concat(dd).dropna()
    out["book_by_year"] = D.groupby("year")[["book_return", "coin_return"]].mean() * 1e4
    out["book_by_coin_bps"] = D.groupby("coin")[["book_return", "coin_return"]].mean() * 1e4
    return out

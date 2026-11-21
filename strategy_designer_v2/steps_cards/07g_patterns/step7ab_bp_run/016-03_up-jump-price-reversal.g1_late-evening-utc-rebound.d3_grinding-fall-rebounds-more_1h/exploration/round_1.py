def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 48
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            v = df["volume"].astype(float)
            r1 = c.pct_change()
            out = pd.DataFrame({"coin": coin, "win": w})
            out["fwd"] = c.shift(-H) / c - 1
            out["fwd24"] = c.shift(-24) / c - 1
            out["r24"] = c / c.shift(24) - 1
            out["r168"] = c / c.shift(168) - 1
            out["r6"] = c / c.shift(6) - 1
            vol720 = r1.rolling(720, min_periods=200).std()
            vol24 = r1.rolling(24).std()
            out["z24"] = out["r24"] / (vol720 * np.sqrt(24))
            out["z168"] = out["r168"] / (vol720 * np.sqrt(168))
            out["z6"] = out["r6"] / (vol720 * np.sqrt(6))
            out["volratio"] = vol24 / vol720
            out["vol720"] = vol720
            out["maxabs_share"] = r1.abs().rolling(24).max() / r1.abs().rolling(24).sum()
            out["vmax_share"] = v.rolling(24).max() / v.rolling(24).sum()
            out["vrel"] = v.rolling(24).sum() / v.rolling(720, min_periods=200).sum() * 30
            out["fc"] = df["forecast"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            out["hour"] = ts.dt.hour
            out["wd"] = ts.dt.weekday
            out["pos"] = np.arange(len(df))
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    st = g.groupby("coin")["fwd"].agg(["mean", "std"])
    g["exc"] = g["fwd"] - g["coin"].map(st["mean"])
    g["sexc"] = g["exc"] / g["coin"].map(st["std"])
    g24 = A[A["pos"] % 24 == 0].dropna(subset=["fwd24"]).copy()
    st24 = g24.groupby("coin")["fwd24"].agg(["mean", "std"])
    g24["exc"] = g24["fwd24"] - g24["coin"].map(st24["mean"])
    g24["sexc"] = g24["exc"] / g24["coin"].map(st24["std"])

    def quint(df, col, q=5):
        d = df.dropna(subset=[col, "exc"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("q").agg(n=("exc", "size"), mean_exc=("exc", "mean"), strength=("sexc", "mean"),
                               med_x=(col, "median"))
        r["t"] = d.groupby("q")["exc"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        return r.round(5)

    def slopes(df, col):
        res = {}
        for coin, d in df.dropna(subset=[col, "sexc"]).groupby("coin"):
            x = (d[col] - d[col].mean()) / d[col].std()
            sl = stats.linregress(x, d["sexc"])
            res[coin] = sl.slope / sl.stderr
        d = df.dropna(subset=[col, "sexc"])
        x = d.groupby("coin")[col].transform(lambda s: (s - s.mean()) / s.std())
        sl = stats.linregress(x, d["sexc"])
        res["pooled"] = sl.slope / sl.stderr
        res["n"] = len(d)
        return res

    feats = ["z24", "z168", "z6", "volratio", "vol720", "maxabs_share", "vmax_share", "vrel"]
    slope_tab = pd.DataFrame({f: slopes(g, f) for f in feats}).T.round(2)
    falls = g[g["r24"] < 0]
    slope_falls = pd.DataFrame({f: slopes(falls, f) for f in ["z24", "maxabs_share", "vmax_share", "vrel", "volratio"]}).T.round(2)
    res = {
        "slope_t_48h_by_feature_per_coin": slope_tab,
        "slope_t_48h_net_falls_only": slope_falls,
        "q_z24": quint(g, "z24"),
        "q_z168": quint(g, "z168"),
        "q_volratio": quint(g, "volratio"),
        "q_vrel": quint(g, "vrel"),
        "q_fc_pos": quint(g[g["fc"] > 0], "fc"),
    }
    wd = g24.groupby("wd").agg(n=("exc", "size"), mean_exc=("exc", "mean"))
    wd["t"] = g24.groupby("wd")["exc"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    res["weekday_24h_exc"] = wd.round(5)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["prev3"] = (1 + d["coin_return"]).rolling(3).apply(np.prod, raw=True) - 1
            d["next1"] = d["coin_return"].shift(-1)
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    res["book_deciles"] = D.groupby("bq").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                              prev3=("prev3", "mean"), next_coin=("next1", "mean"), n=("book_return", "size")).round(5)
    yr = D.copy(); yr["year"] = pd.to_datetime(yr["day"]).dt.year
    res["book_by_year"] = yr.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size")).round(5)
    return res

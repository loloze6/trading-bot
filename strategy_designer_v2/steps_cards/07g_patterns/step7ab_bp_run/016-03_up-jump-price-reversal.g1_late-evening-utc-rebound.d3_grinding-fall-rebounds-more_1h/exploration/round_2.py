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
            out = pd.DataFrame(index=df.index)
            out["coin"] = coin
            out["win"] = w
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
            out["fc"] = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            out["hour"] = ts.dt.hour.values
            out["wd"] = ts.dt.weekday.values
            out["year"] = ts.dt.year.values
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

    def tstat(s):
        s = s.dropna()
        return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan

    def quint(df, col, q=5):
        d = df.dropna(subset=[col, "exc"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("q").agg(n=("exc", "size"), mean_exc=("exc", "mean"), strength=("sexc", "mean"),
                               med_x=(col, "median"))
        r["t"] = d.groupby("q")["exc"].apply(tstat)
        return r.round(5)

    def slopes(df, col):
        res = {}
        dd = df.dropna(subset=[col, "sexc"])
        for coin, d in dd.groupby("coin"):
            x = (d[col] - d[col].mean()) / d[col].std()
            sl = stats.linregress(x, d["sexc"])
            res[coin] = sl.slope / sl.stderr
        x = dd.groupby("coin")[col].transform(lambda s: (s - s.mean()) / s.std())
        sl = stats.linregress(x, dd["sexc"])
        res["pooled_t"] = sl.slope / sl.stderr
        res["pooled_slope"] = sl.slope
        res["n"] = len(dd)
        return pd.Series(res)

    def slope_by_year(df, col):
        res = {}
        dd = df.dropna(subset=[col, "sexc"]).copy()
        dd["x"] = dd.groupby("coin")[col].transform(lambda s: (s - s.mean()) / s.std())
        for y, d in dd.groupby("year"):
            if len(d) > 50:
                sl = stats.linregress(d["x"], d["sexc"])
                res[y] = sl.slope / sl.stderr
        return pd.Series(res)

    res = {}
    feats = ["z24", "z168", "z6", "volratio", "vol720", "maxabs_share", "vmax_share", "vrel"]
    try:
        res["slope_t_48h_per_coin"] = pd.DataFrame({f: slopes(g, f) for f in feats}).T.round(3)
    except Exception as e:
        res["err1"] = str(e)
    try:
        falls = g[g["r24"] < 0]
        res["slope_t_48h_net_falls"] = pd.DataFrame({f: slopes(falls, f) for f in ["z24", "maxabs_share", "vmax_share", "vrel", "volratio"]}).T.round(3)
    except Exception as e:
        res["err2"] = str(e)
    try:
        res["slope_t_by_year"] = pd.DataFrame({f: slope_by_year(g, f) for f in ["z24", "z168", "volratio", "vrel"]}).round(2)
    except Exception as e:
        res["err3"] = str(e)
    for f in ["z24", "z168", "volratio", "vrel"]:
        try:
            res["q_" + f] = quint(g, f)
        except Exception as e:
            res["errq_" + f] = str(e)
    try:
        res["q_fc_pos"] = quint(g[g["fc"] > 0], "fc")
    except Exception as e:
        res["errfc"] = str(e)
    try:
        wd = g24.groupby("wd").agg(n=("exc", "size"), mean_exc=("exc", "mean"))
        wd["t"] = g24.groupby("wd")["exc"].apply(tstat)
        res["weekday_24h_exc"] = wd.round(5)
        g4 = A.copy()
        g4["r_next4"] = np.nan
    except Exception as e:
        res["errwd"] = str(e)
    try:
        dd = []
        for coin, wins in data["days"].items():
            for w, d in wins.items():
                d = d.copy().reset_index(drop=True); d["coin"] = coin; d["win"] = w
                d["prev3"] = (1 + d["coin_return"]).rolling(3).apply(np.prod, raw=True) - 1
                d["next1"] = d["coin_return"].shift(-1)
                dd.append(d)
        D = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
        D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
        res["book_deciles"] = D.groupby("bq").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                  prev3=("prev3", "mean"), next_coin=("next1", "mean"),
                                                  n=("book_return", "size")).round(5)
        D["year"] = pd.to_datetime(D["day"]).dt.year
        res["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                    n=("book_return", "size")).round(5)
    except Exception as e:
        res["errbook"] = str(e)
    return res

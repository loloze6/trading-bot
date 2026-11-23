def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rets) if rets else np.nan
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            r30 = c / c.shift(30) - 1
            r5p = c / c.shift(5) - 1
            near = c / df["high"].rolling(90, min_periods=20).max()
            vol_rank = vol30 / vol30.rolling(180, min_periods=60).mean()
            ts = pd.to_datetime(df["timestamp"])
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                f = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, fwd=f, ex=f - drift[coin],
                                 fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                 r1z=r1.iloc[i] / vol30.iloc[i] if vol30.iloc[i] > 0 else np.nan,
                                 r30=r30.iloc[i], r5p=r5p.iloc[i] / (vol30.iloc[i] * np.sqrt(5)) if vol30.iloc[i] > 0 else np.nan,
                                 near=near.iloc[i], volr=vol_rank.iloc[i],
                                 year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    def bucket(col, q=5, sub=None):
        d = (g if sub is None else sub).dropna(subset=[col, "ex"])
        d = d.assign(b=pd.qcut(d[col], q, labels=False, duplicates="drop"))
        out = d.groupby("b").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"),
                                 mean_ex=("ex", "mean"), sd=("ex", "std"))
        out["t"] = out["mean_ex"] / (out["sd"] / np.sqrt(out["n"]))
        r, p = stats.spearmanr(d[col], d["ex"])
        out["spearman_all"] = r
        out["p_all"] = p
        return out.round(4)
    res = {}
    act = g[g.fc > 0]
    res["fc_quint_active"] = bucket("fc", 4, act)
    res["regime"] = g.groupby("reg")["ex"].agg(["size", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["size"]))).round(4)
    res["r30_all"] = bucket("r30")
    res["r5p_all"] = bucket("r5p")
    res["r1z_all"] = bucket("r1z")
    res["near_all"] = bucket("near")
    res["volr_all"] = bucket("volr")
    res["near_in_trending"] = bucket("near", 5, g[g.r30 > 0])
    res["r5p_in_trending"] = bucket("r5p", 5, g[g.r30 > 0])
    res["year_active"] = act.groupby("year")["ex"].agg(["size", "mean"]).round(4)
    # weekday on daily coin returns
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; d["coin"] = coin
            dd.append(d)
    D = pd.concat(dd)
    wd = D.groupby("wd")["coin_return"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["weekday_coin"] = wd.round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=coin))
    T = pd.concat(tr)
    T["pl"] = T["net_profit_loss_percent"]
    res["trades_by_entryfc"] = T.assign(b=pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")).groupby("b")["pl"].agg(["size", "mean", "median"]).round(3)
    res["trades_summary"] = pd.Series({"n": len(T), "mean": T.pl.mean(), "win": (T.pl > 0).mean(), "days_mean": T.duration_minutes.mean() / 1440}).round(3)
    return res

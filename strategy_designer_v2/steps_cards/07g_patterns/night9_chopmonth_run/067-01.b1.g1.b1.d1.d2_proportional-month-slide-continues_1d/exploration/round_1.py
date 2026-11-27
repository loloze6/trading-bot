def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            col = "debug_info.components.fall30.last_history_value"
            r30 = b[col].astype(float) if col in b else pd.Series(np.nan, index=b.index)
            r30c = (c / c.shift(30) - 1) * 100
            r30 = r30.fillna(r30c)
            r60 = (c / c.shift(60) - 1) * 100
            r10 = (c / c.shift(10) - 1) * 100
            r3 = (c / c.shift(3) - 1) * 100
            dret = c.pct_change()
            vol30 = dret.rolling(30).std()
            vol10 = dret.rolling(10).std()
            fwd = c.shift(-10) / c - 1
            fwd1 = c.shift(-1) / c - 1
            for i in range(0, n, 10):
                rows.append(dict(coin=coin, w=w, i=i, day=str(b["timestamp"].iloc[i])[:10],
                                 regime=b["regime"].iloc[i], r30=r30.iloc[i], r60=r60.iloc[i], r10=r10.iloc[i],
                                 r3=r3.iloc[i], vol30=vol30.iloc[i], vol10=vol10.iloc[i],
                                 volratio=vol10.iloc[i] / vol30.iloc[i] if vol30.iloc[i] else np.nan,
                                 fwd=fwd.iloc[i], wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["ex"] / g["coin"].map(sd)
    out = {}
    def tab(df, key, q=5):
        d = df.dropna(subset=[key]).copy()
        d["bin"] = pd.qcut(d[key], q, labels=False, duplicates="drop")
        def f(x):
            dd = x.groupby("day")["ex"].sum()
            t = dd.mean() / (dd.std() / np.sqrt(len(dd))) if len(dd) > 2 else np.nan
            return pd.Series(dict(n=len(x), days=len(dd), mean_key=x[key].mean(), ex=x["ex"].mean(), z=x["z"].mean(), t=t))
        return d.groupby("bin").apply(f)
    chop = g[g.regime == "chop"]
    nonchop = g[g.regime != "chop"]
    out["chop_r30_quint"] = tab(chop, "r30")
    out["nonchop_r30_quint"] = tab(nonchop, "r30")
    out["chop_r10_quint"] = tab(chop, "r10")
    out["chop_r3_quint"] = tab(chop, "r3")
    out["all_vol30_quint"] = tab(g, "vol30")
    out["all_volratio_quint"] = tab(g, "volratio")
    out["all_r60_quint"] = tab(g.dropna(subset=["r60"]), "r60")
    out["all_r10_quint"] = tab(g, "r10")
    out["regime_counts"] = g["regime"].value_counts()
    # correlations
    cr = {}
    for nm, d in [("chop", chop), ("nonchop", nonchop), ("all", g)]:
        for k in ["r30", "r10", "r3", "vol30", "volratio"]:
            dd = d.dropna(subset=[k, "z"])
            if len(dd) > 10:
                r, p = stats.spearmanr(dd[k], dd["z"])
                cr[f"{nm}_{k}"] = (round(r, 4), round(p, 4), len(dd))
    out["spearman"] = pd.Series({k: str(v) for k, v in cr.items()})
    # daily: weekday, after large daily moves
    dl = []
    for coin, wd in days.items():
        for w, d in wd.items():
            d = d.copy()
            d["coin"] = coin; d["w"] = w
            d["next"] = d["coin_return"].shift(-1)
            d["wdn"] = pd.to_datetime(d["day"]).dt.weekday
            d["zret"] = d["coin_return"] / d["coin_return"].rolling(30).std()
            dl.append(d)
    D = pd.concat(dl)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["weekday_coin_ret"] = D.groupby("wdn")["coin_return"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    Dz = D.dropna(subset=["zret", "next"]).copy()
    Dz["bin"] = pd.qcut(Dz["zret"], 7, labels=False)
    out["next_day_after_zret"] = Dz.groupby("bin").agg(zm=("zret", "mean"), nxt=("next", "mean"), n=("next", "size"),
                                                       t=("next", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    B = D.dropna(subset=["book_return"])
    out["book_by_year"] = B.groupby("year")["book_return"].agg(["mean", "count"])
    out["book_by_window"] = B.groupby("w")["book_return"].agg(["mean", "std", "count"])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 24
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            past2 = c / c.shift(2) - 1
            scale2 = past2.abs().rolling(720, min_periods=200).mean()
            past24 = c / c.shift(24) - 1
            scale24 = past24.abs().rolling(720, min_periods=200).mean()
            past168 = c / c.shift(168) - 1
            vol = r1.rolling(720, min_periods=200).std()
            vol24 = r1.rolling(24, min_periods=20).std()
            volu = b["volume"].astype(float)
            vrel = volu.rolling(24).sum() / volu.rolling(720, min_periods=200).sum() * 30
            fwd = c.shift(-H) / c - 1
            fwd8 = c.shift(-8) / c - 1
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.iloc[idx].values,
                "fwd8": fwd8.iloc[idx].values,
                "s2": (past2 / scale2).iloc[idx].values,
                "s24": (past24 / scale24).iloc[idx].values,
                "p168": past168.iloc[idx].values,
                "vol": vol.iloc[idx].values, "volratio": (vol24 / vol).iloc[idx].values,
                "vrel": vrel.iloc[idx].values,
                "hour": ts.dt.hour.iloc[idx].values, "wd": ts.dt.weekday.iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values,
            })
            rows.append(d)
            hourly.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values,
                                        "wd": ts.dt.weekday.values,
                                        "r": r1.shift(-1).values,
                                        "lv": np.log(volu.replace(0, np.nan)).values}))
    g = pd.concat(rows, ignore_index=True)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["usual"] = g.groupby("coin")["fwd"].transform("std")
    g["str"] = g["ex"] / g["usual"]

    def qtab(col, q=5):
        x = g.dropna(subset=[col, "ex"]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                               strength=("str", "mean"),
                               t=("ex", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
        return t
    for col in ["s2", "s24", "p168", "vol", "volratio", "vrel"]:
        out["fwd24 excess by quintile of " + col] = qtab(col)
    # slope of ex on s24 within vol tercile
    x = g.dropna(subset=["s24", "ex", "vol"]).copy()
    x["vt"] = x.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = []
    for k, gg in x.groupby("vt"):
        sl = stats.linregress(gg["s24"], gg["str"])
        res.append({"vol_tercile": k, "n": len(gg), "slope_str_on_s24": sl.slope, "t": sl.slope / sl.stderr})
    out["s24 slope by vol tercile"] = pd.DataFrame(res)
    res = []
    for coin, gg in x.groupby("coin"):
        sl = stats.linregress(gg["s24"], gg["str"])
        sl2 = stats.linregress(gg["s2"].fillna(0), gg["str"])
        res.append({"coin": coin, "n": len(gg), "slope_s24": sl.slope, "t24": sl.slope / sl.stderr,
                    "slope_s2": sl2.slope, "t2": sl2.slope / sl2.stderr})
    out["slopes by coin"] = pd.DataFrame(res)
    out["fwd24 excess by weekday"] = g.groupby("wd").agg(n=("ex", "size"), mean_ex=("ex", "mean"),
        t=("ex", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    h = pd.concat(hourly, ignore_index=True).dropna(subset=["r"])
    h["lvd"] = h["lv"] - h.groupby("coin")["lv"].transform("mean")
    out["next-hour return by hour"] = h.groupby("hour").agg(n=("r", "size"), mean=("r", "mean"),
        t=("r", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))), logvol_dev=("lvd", "mean"))
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy()
            d["coin"] = coin
            d["next_coin"] = d["coin_return"].shift(-1)
            dd.append(d)
    D = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book day decile vs coin same/next day"] = D.groupby("bq").agg(n=("book_return", "size"),
        book=("book_return", "mean"), coin=("coin_return", "mean"), next_coin=("next_coin", "mean"))
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book vs coin by year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    return out

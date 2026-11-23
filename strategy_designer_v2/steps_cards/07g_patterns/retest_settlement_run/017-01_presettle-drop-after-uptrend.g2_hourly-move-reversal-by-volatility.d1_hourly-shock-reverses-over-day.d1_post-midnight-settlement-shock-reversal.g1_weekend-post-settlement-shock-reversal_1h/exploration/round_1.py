def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(24, min_periods=24).std()
            z = r1 / sd
            r4 = c / c.shift(4) - 1
            z4 = r4 / (sd * 2)
            f24 = c.shift(-24) / c - 1
            f6 = c.shift(-6) / c - 1
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(168, min_periods=48).median()
            sdl = r1.rolling(24 * 30, min_periods=24 * 10).std()
            volreg = sd / sdl
            tr7 = c / c.shift(168) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "year": ts.dt.year, "z": z, "z4": z4, "f24": f24, "f6": f6,
                               "vrel": vrel, "volreg": volreg, "tr7z": tr7 / (sd * np.sqrt(168)),
                               "pos": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # coin mean 24h on non-overlapping grid
    d["f24x"] = d["f24"] - d.groupby("coin")["f24"].transform("mean")
    d = d.dropna(subset=["z", "f24x"])
    d["zc"] = d["z"].clip(-6, 6)

    def reg(g, x="zc", y="f24x"):
        g = g.dropna(subset=[x, y])
        if len(g) < 50:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        s = stats.linregress(-g[x], g[y])
        return pd.Series({"n": len(g), "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr})

    d["we"] = np.where(d["wd"] >= 5, "we", "wk")
    by_hour = d.groupby(["hour", "we"]).apply(reg).unstack("we")
    by_wd_h0 = d[d.hour == 0].groupby("wd").apply(reg)
    by_wd_all = d.groupby("wd").apply(reg)
    d["vq"] = pd.qcut(d["volreg"], 3, labels=["lowvol", "mid", "highvol"])
    by_vol = d.groupby(["vq", "we"]).apply(reg).unstack("we")
    d["vrq"] = pd.qcut(d["vrel"], 3, labels=["lowvolu", "mid", "highvolu"])
    by_vrel = d.groupby(["vrq", "we"]).apply(reg).unstack("we")
    # 4h move fade, any hour, grouped by weekend
    by_z4 = d.groupby("we").apply(lambda g: reg(g.assign(z4c=g["z4"].clip(-6, 6)), x="z4c"))
    by_coin = d.groupby(["coin", "we"]).apply(reg).unstack("we")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    book = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    book["year"] = pd.to_datetime(book["day"]).dt.year
    by_year = book.groupby("year").agg(n=("book_return", "size"),
        mean_bp=("book_return", lambda s: s.mean() * 1e4),
        sharpe=("book_return", lambda s: s.mean() / s.std() * np.sqrt(365)),
        coin_bp=("coin_return", lambda s: s.mean() * 1e4))
    by_coin_book = dd.groupby("coin")["book_return"].agg(
        mean_bp=lambda s: s.mean() * 1e4, sharpe=lambda s: s.mean() / s.std() * np.sqrt(365))
    return {"fade_by_hour": by_hour, "fade_h0_by_wd": by_wd_h0, "fade_allhours_by_wd": by_wd_all,
            "fade_by_volregime": by_vol, "fade_by_relvolume": by_vrel, "fade4h_by_we": by_z4,
            "fade_by_coin": by_coin, "book_by_year": by_year, "book_by_coin": by_coin_book}

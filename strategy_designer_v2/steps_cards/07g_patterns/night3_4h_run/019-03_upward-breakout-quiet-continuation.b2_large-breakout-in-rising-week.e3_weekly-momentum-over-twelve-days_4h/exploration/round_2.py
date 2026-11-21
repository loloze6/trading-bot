def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows, drows = [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            vol120 = r.rolling(120).std()
            ret42 = c / c.shift(42) - 1
            ret6 = c / c.shift(6) - 1
            rng42 = (b["high"].rolling(42).max() - b["low"].rolling(42).min()) / c
            rngrel = rng42 / (r.rolling(180).std() * np.sqrt(42))
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "yr": ts.dt.year.values[idx],
                "fc": b["forecast"].values[idx], "fwd": fwd.values[idx],
                "volratio": (vol20 / vol120).values[idx],
                "rngrel_prev": rngrel.shift(42).values[idx],
                "ret42s": (ret42 / (vol20 * np.sqrt(42))).values[idx],
                "ret6s": (ret6 / (vol20 * np.sqrt(6))).values[idx],
                "fwdvol": r[::-1].rolling(72).std()[::-1].shift(-1).values[idx] if False else np.nan,
            }))
        for w, d in data["days"][coin].items():
            dd = d.copy()
            dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
            dd["yr"] = pd.to_datetime(dd["day"]).dt.year
            dd["next"] = dd["coin_return"].shift(-1)
            dd["coin"] = coin
            dd["w"] = w
            drows.append(dd[["coin", "w", "wd", "yr", "coin_return", "next", "book_return"]])
    G = pd.concat(rows, ignore_index=True)
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G = G.dropna(subset=["ex", "fc", "volratio"])
    out = {}

    def tt(x):
        return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

    # vol ratio effect by sign of the 7-day return
    G["vq"] = pd.qcut(G["volratio"], 5, labels=False)
    G["sgn"] = np.where(G["ret42s"] > 0, "up7d", "down7d")
    o = G.groupby(["vq", "sgn"])["ex"].agg(["size", "mean"])
    o["t"] = G.groupby(["vq", "sgn"])["ex"].apply(tt)
    out["volratio_by_sign"] = o.round(4)
    # vol ratio slope by coin and by year
    pc = []
    for k, x in G.groupby("coin"):
        s = stats.linregress(x["volratio"], x["ex"])
        pc.append({"coin": k, "n": len(x), "slope": s.slope, "t": s.slope / s.stderr})
    out["volratio_slope_per_coin"] = pd.DataFrame(pc).round(4)
    py = []
    for k, x in G.groupby("yr"):
        if len(x) > 20:
            s = stats.linregress(x["volratio"], x["ex"])
            py.append({"yr": k, "n": len(x), "slope": s.slope, "t": s.slope / s.stderr})
    out["volratio_slope_per_year"] = pd.DataFrame(py).round(4)
    s = stats.linregress(G["volratio"], G["ex"])
    out["volratio_pooled"] = pd.Series({"n": len(G), "slope": s.slope, "t": s.slope / s.stderr})
    # joint regression: ex on fc and volratio
    X = np.column_stack([np.ones(len(G)), G["fc"], G["volratio"]])
    beta, *_ = np.linalg.lstsq(X, G["ex"].values, rcond=None)
    res = G["ex"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
    out["joint_fc_volratio"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                            index=["const", "fc", "volratio"]).round(5)
    # nonlinearity of forecast: |fc| tercile, signed capture
    G["dirx"] = np.sign(G["fc"]) * G["ex"]
    G["aq"] = pd.qcut(G["fc"].abs(), 4, labels=False)
    o = G.groupby("aq")["dirx"].agg(["size", "mean"])
    o["t"] = G.groupby("aq")["dirx"].apply(tt)
    out["capture_by_abs_fc"] = o.round(4)
    # brief's idea: narrow previous week then 7d move direction
    d = G.dropna(subset=["rngrel_prev"]).copy()
    d["nq"] = pd.qcut(d["rngrel_prev"], 3, labels=False)
    o = d.groupby("nq").agg(n=("ex", "size"), absfwd=("fwd", lambda x: x.abs().mean()))
    o["slope_t"] = [ (lambda s: s.slope / s.stderr)(stats.linregress(x["ret42s"], x["ex"])) for _, x in d.groupby("nq")]
    out["prev_week_range_tercile"] = o.round(4)
    # weekday, day-aligned
    D = pd.concat(drows, ignore_index=True)
    Dn = D.dropna(subset=["coin_return"])
    o = Dn.groupby("wd")["coin_return"].agg(["size", "mean"])
    o["t"] = Dn.groupby("wd")["coin_return"].apply(tt)
    out["coin_return_by_weekday"] = o.round(5)
    fri = Dn[Dn.wd.isin([4, 5])]
    o = fri.groupby("yr")["coin_return"].agg(["size", "mean"])
    o["t"] = fri.groupby("yr")["coin_return"].apply(tt)
    out["fri_sat_by_year"] = o.round(5)
    o = fri.groupby("coin")["coin_return"].agg(["size", "mean"])
    o["t"] = fri.groupby("coin")["coin_return"].apply(tt)
    out["fri_sat_by_coin"] = o.round(5)
    # book falls: book return quantiles vs coin return
    Db = D.dropna(subset=["book_return"])
    Db["bq"] = pd.qcut(Db["book_return"], 10, labels=False)
    out["book_deciles_vs_coin"] = Db.groupby("bq")[["book_return", "coin_return"]].mean().round(4)
    return out

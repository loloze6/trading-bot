def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "sd": sd,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "vr": v / v.rolling(720, min_periods=240).mean()})
            for L in (12, 24, 48, 72):
                df[f"p{L}"] = c / c.shift(L) - 1
            for h in (1, 12, 24, 48, 72):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["vr24"] = v.rolling(24).sum() / (v.rolling(720, min_periods=240).mean() * 24)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def grid(h, cols):
        d = A[(A["pos"] % h) == 0].dropna(subset=[f"f{h}"] + cols).copy()
        d["u"] = d[f"f{h}"] - d.groupby("coin")[f"f{h}"].transform("mean")
        return d

    # 1. graded reversal: slope of unusual move on scaled past return, lookback L, horizon h
    res = []
    for L in (12, 24, 48, 72):
        for h in (12, 24, 48, 72):
            d = grid(h, [f"p{L}", "sd"])
            for coin, g in d.groupby("coin"):
                x = g[f"p{L}"] / (g["sd"] * np.sqrt(L))
                s = stats.linregress(x, g["u"])
                res.append({"L": L, "h": h, "coin": coin, "n": len(g),
                            "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr})
    out["reversal_grid"] = pd.DataFrame(res).round(2)

    # 2. 24h->24h reversal by year (slope t) and by volume of the 24h
    d = grid(24, ["p24", "sd", "vr24"])
    d["x"] = d["p24"] / (d["sd"] * np.sqrt(24))
    yr = []
    for (y), g in d.groupby("year"):
        s = stats.linregress(g["x"], g["u"])
        yr.append({"year": y, "n": len(g), "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr})
    out["rev24_by_year"] = pd.DataFrame(yr).round(2)
    d["vq"] = pd.qcut(d["vr24"], 3, labels=False)
    vv = []
    for q, g in d.groupby("vq"):
        s = stats.linregress(g["x"], g["u"])
        vv.append({"vol_tercile": q, "n": len(g), "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr})
    out["rev24_by_volume"] = pd.DataFrame(vv).round(2)

    # 3. hour 20-21 and 0-3 by year and coin
    d = grid(1, [])
    d["hb"] = np.where(d["hour"].isin([20, 21]), "h20-21", np.where(d["hour"].isin([0, 1, 2, 3]), "h0-3", "other"))
    def summ(g):
        x = g["u"]; return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out["hours_by_year"] = d[d["hb"] != "other"].groupby(["hb", "year"]).apply(summ).round(2)
    out["hours_by_coin"] = d[d["hb"] != "other"].groupby(["hb", "coin"]).apply(summ).round(2)

    # 4. Thursday by year (24h grid aligned to day start)
    d = A[A["hour"] == 0].dropna(subset=["f24"]).copy()
    d["u"] = d["f24"] - d.groupby("coin")["f24"].transform("mean")
    out["thursday_by_year"] = d[d["wd"] == 3].groupby("year").apply(summ).round(2)

    # 5. trades: gross by duration
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["db"] = pd.qcut(T["duration_minutes"], 5, duplicates="drop")
    out["trades_by_duration"] = T.groupby("db", observed=True).agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), fc=("entry_forecast", "mean")).round(3)
    return out

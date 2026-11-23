def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour.values
            b["wd"] = ts.dt.weekday.values
            c = b["close"].astype(float)
            r1 = c.pct_change()
            b["r1"] = r1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd24"] = c.shift(-24) / c - 1
            b["fwd4"] = c.shift(-4) / c - 1
            b["ret24"] = c / c.shift(24) - 1
            vol24 = r1.rolling(24).std()
            b["z1"] = r1 / vol24.rolling(720, min_periods=240).mean()
            b["volratio"] = vol24 / vol24.rolling(720, min_periods=240).mean()
            b["z24"] = b["ret24"] / (vol24 * np.sqrt(24))
            b["vrel"] = b["volume"] / b["volume"].rolling(720, min_periods=240).median()
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["w"] = w
            rows.append(b[["coin","w","hour","wd","r1","fwd1","fwd4","fwd24","ret24","z1","volratio","z24","vrel","pos","forecast","postRebalance_current_allocation"]])
    df = pd.concat(rows, ignore_index=True)
    # drift per coin
    g24 = df[df.pos % 24 == 0].dropna(subset=["fwd24"])
    drift24 = g24.groupby("coin")["fwd24"].mean()
    drift1 = df.groupby("coin")["fwd1"].mean()
    df["ex1"] = df["fwd1"] - df["coin"].map(drift1)
    df["ex24"] = df["fwd24"] - df["coin"].map(drift24)
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # 1 hourly excess return by hour of bar's close -> next hour (fwd1 from bar t close)
    out["fwd1_by_hour"] = df.groupby("hour")["ex1"].apply(tt).unstack()
    # volume rel by hour
    out["vrel_by_hour"] = df.groupby("hour")["vrel"].median()
    # 2 trend-signed next-hour return: -sign(ret24)*ex1, by hour
    df["against"] = -np.sign(df["ret24"]) * df["ex1"]
    out["against_trend_next_hour_by_hour"] = df.groupby("hour")["against"].apply(tt).unstack()
    # 3 24h fwd after z1 deciles, grid 24
    g = df[df.pos % 24 == 0].dropna(subset=["ex24","z1"]).copy()
    g["z1d"] = pd.qcut(g["z1"], 10, labels=False)
    out["ex24_by_z1_decile"] = g.groupby("z1d")["ex24"].apply(tt).unstack()
    g["z24d"] = pd.qcut(g["z24"], 10, labels=False)
    out["ex24_by_z24_decile"] = g.groupby("z24d")["ex24"].apply(tt).unstack()
    g["vrd"] = pd.qcut(g["volratio"], 5, labels=False)
    out["ex24_by_volratio_quint"] = g.groupby("vrd")["ex24"].apply(tt).unstack()
    # weekday daily
    d = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"]=coin; x["w"]=w; d.append(x)
    dd = pd.concat(d, ignore_index=True)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    dd["ex"] = dd["coin_return"] - dd["coin"].map(dd.groupby("coin")["coin_return"].mean())
    out["coin_day_ex_by_weekday"] = dd.groupby("wd")["ex"].apply(tt).unstack()
    out["book_by_weekday"] = dd.groupby("wd")["book_return"].apply(tt).unstack()
    # book: book return vs coin return beta and share of days
    x = dd.dropna(subset=["book_return","coin_return"])
    sl = stats.linregress(x["coin_return"], x["book_return"])
    out["book_on_coin"] = pd.Series({"slope": sl.slope, "intercept_bp": sl.intercept*1e4, "r2": sl.rvalue**2, "n": len(x)})
    out["mean_alloc"] = df.groupby("coin")["postRebalance_current_allocation"].mean()
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean 5-bar return over all windows (grid)
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.extend(list(c[idx + H] / c[idx] - 1))
        mu = np.nanmean(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            vol90 = r1.rolling(90, min_periods=40).std()
            hi90 = b["high"].rolling(90, min_periods=30).max()
            near = c / hi90 - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                fr = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year,
                                 wd=ts.iloc[i].dayofweek,
                                 f=b["forecast"].iloc[i], fr=fr, ex=fr - mu,
                                 r1=r1.iloc[i], r5=r5p.iloc[i], r20=r20p.iloc[i],
                                 vr=vol20.iloc[i] / vol90.iloc[i] if vol90.iloc[i] else np.nan,
                                 r1z=r1.iloc[i] / vol20.iloc[i] if vol20.iloc[i] else np.nan,
                                 near=near.iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    d = pd.DataFrame(rows)
    out = {}
    def grp(col, q=5):
        x = d.dropna(subset=[col, "ex"]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("q")["ex"].agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        sp = stats.spearmanr(x[col], x["ex"])
        g["spearman_all"] = sp.correlation
        return g
    for col in ["f", "r1z", "r5", "r20", "vr", "near"]:
        out["quint_" + col] = grp(col)
    # per coin rank corr for key ones
    pc = []
    for coin, x in d.groupby("coin"):
        rr = {"coin": coin, "n": len(x)}
        for col in ["f", "r1z", "r5", "r20", "vr", "near"]:
            y = x.dropna(subset=[col, "ex"])
            rr[col] = stats.spearmanr(y[col], y["ex"]).correlation
        pc.append(rr)
    out["per_coin_spearman"] = pd.DataFrame(pc)
    # forecast-signed gain by year
    d["g"] = d["f"] / 10 * d["ex"]
    gy = d.groupby("year")["g"].agg(["mean", "std", "count"])
    gy["t"] = gy["mean"] / (gy["std"] / np.sqrt(gy["count"]))
    out["fgain_by_year"] = gy
    gc = d.groupby("coin")["g"].agg(["mean", "std", "count"])
    gc["t"] = gc["mean"] / (gc["std"] / np.sqrt(gc["count"]))
    out["fgain_by_coin"] = gc
    # book daily: by weekday, long vs short contribution
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w
            dd.append(x)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    g = D.groupby("wd")[["book_return", "coin_return"]].mean()
    out["daily_by_weekday"] = g
    bw = D.groupby("win")[["book_return", "coin_return"]].mean()
    out["daily_by_window"] = bw
    return out

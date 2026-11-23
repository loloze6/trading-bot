def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    hourly = []
    for coin, ws in bars.items():
        # drift: mean non-overlapping 24-bar return over all windows
        d24 = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            d24.extend(c[idx + 24] / c[idx] - 1)
        drift = np.nanmean(d24)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r2 = c / c.shift(2) - 1
            sc = r2 / r2.abs().rolling(720, min_periods=120).mean()
            r24 = c.shift(-24) / c - 1 - drift
            r24b = c.shift(-48) / c.shift(-24) - 1 - drift
            r4 = c.shift(-4) / c - 1
            closeh = (pd.to_datetime(b["timestamp"]).dt.hour + 1) % 24
            r1 = c.pct_change()
            vol = b["volume"]
            relv = vol / vol.rolling(168, min_periods=24).median()
            r24past = c / c.shift(24) - 1
            vol24 = r1.rolling(168, min_periods=48).std()
            df = pd.DataFrame({"coin": coin, "w": w, "h": closeh, "sc": sc, "r24": r24,
                               "r24b": r24b, "r4": r4, "r1": r1, "relv": relv,
                               "past24": r24past / (vol24 * np.sqrt(24)), "vol": vol24,
                               "pos": b["postRebalance_current_allocation"],
                               "fc": b["forecast"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # slope of 24h fwd on -sc per closing hour (all cases; each hour once per day -> nonoverlap)
    res = []
    for h in range(24):
        s = A[A.h == h].dropna(subset=["sc", "r24"])
        x = -s["sc"].clip(-10, 10); y = s["r24"]
        lr = stats.linregress(x, y)
        s2 = s.dropna(subset=["r24b"])
        lr2 = stats.linregress(-s2["sc"].clip(-10, 10), s2["r24b"])
        s4 = s.dropna(subset=["r4"])
        lr4 = stats.linregress(-s4["sc"].clip(-10, 10), s4["r4"])
        res.append({"close_hour": h, "n": len(s), "t_24h": lr.slope / lr.stderr,
                    "t_day2": lr2.slope / lr2.stderr, "t_4h": lr4.slope / lr4.stderr,
                    "mean_r1_bp": A.loc[A.h == h, "r1"].mean() * 1e4,
                    "t_r1": stats.ttest_1samp(A.loc[A.h == h, "r1"].dropna(), 0).statistic,
                    "med_relvol": A.loc[A.h == h, "relv"].median()})
    out["by_close_hour"] = pd.DataFrame(res).round(3)
    # 24h past-trend scaled vs 24h fwd, nonoverlap at hour 0, by vol tercile
    s = A[A.h == 0].dropna(subset=["past24", "r24", "vol"]).copy()
    s["vq"] = s.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    r = []
    for q, g in s.groupby("vq"):
        lr = stats.linregress(g["past24"].clip(-6, 6), g["r24"])
        r.append({"vol_tercile": q, "n": len(g), "slope_bp": lr.slope * 1e4, "t": lr.slope / lr.stderr})
    out["past24_vs_fwd24_by_vol"] = pd.DataFrame(r).round(3)
    # weekday of daily coin return
    D = []
    for coin, ws in days.items():
        for w, d in ws.items():
            dd = d.copy(); dd["coin"] = coin; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["weekday"] = D.groupby("wd").agg(coin_bp=("coin_return", lambda x: x.mean() * 1e4),
                                         book_bp=("book_return", lambda x: x.mean() * 1e4),
                                         n=("coin_return", "count")).round(2)
    # by year: book vs coin
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["year"] = D.groupby("yr").agg(coin_bp=("coin_return", lambda x: x.mean() * 1e4),
                                      book_bp=("book_return", lambda x: x.mean() * 1e4)).round(2)
    return out

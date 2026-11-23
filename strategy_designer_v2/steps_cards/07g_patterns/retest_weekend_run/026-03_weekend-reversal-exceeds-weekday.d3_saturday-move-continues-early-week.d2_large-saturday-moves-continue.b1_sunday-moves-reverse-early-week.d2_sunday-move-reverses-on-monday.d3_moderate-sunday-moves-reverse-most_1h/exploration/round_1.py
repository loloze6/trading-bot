def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []      # per weekday-end cases
    hr = []        # hourly returns
    grid = []      # 24h grid for large-move / vol angle
    for coin, wins in data["bars"].items():
        # drift of 48h on grid
        d48 = []
        for w, b in wins.items():
            c = b["close"].values
            d48 += list(c[48::48] / c[:-48:48][:len(c[48::48])] - 1)
        drift48 = np.nanmean(d48)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            r1 = c.pct_change()
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=360).mean()
            vol = r1.rolling(720, min_periods=360).std()
            f24 = c.shift(-24) / c - 1
            f48 = c.shift(-48) / c - 1
            f24b = c.shift(-48) / c.shift(-24) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "wd": ts.dt.dayofweek, "h": ts.dt.hour,
                               "s": (r24 / mabs).clip(-2, 2), "sraw": r24 / mabs, "vol": vol,
                               "f24": f24, "f48": f48 - drift48, "f24b": f24b, "fc": b["forecast"]})
            hr.append(pd.DataFrame({"coin": coin, "h": ts.dt.hour, "wd": ts.dt.dayofweek, "r": r1.shift(-1)}))
            last = df[df["h"] == 23]
            rows.append(last)
            grid.append(df.iloc[::24])
    R = pd.concat(rows).dropna(subset=["s", "f48", "f24b", "f24"])
    res = []
    for wd, g in R.groupby("wd"):
        o = {"wd": wd, "n": len(g)}
        for y in ["f24", "f24b", "f48"]:
            lr = stats.linregress(g["s"], g[y])
            o["slope_" + y] = lr.slope; o["t_" + y] = lr.slope / lr.stderr
        res.append(o)
    out["reversal_by_weekday_end(s=scaled 24h ret capped)"] = pd.DataFrame(res)
    # Sunday by scaled bins
    S = R[R.wd == 6].copy()
    S["bin"] = pd.qcut(S["sraw"], 5, labels=False)
    out["sunday_quintiles"] = S.groupby("bin").agg(n=("f48", "size"), s=("sraw", "mean"), f24=("f24", "mean"), f24b=("f24b", "mean"), f48=("f48", "mean"))
    # Sunday by vol tercile within coin
    S["vt"] = S.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    tt = []
    for v, g in S.groupby("vt"):
        lr = stats.linregress(g["s"], g["f48"]); tt.append({"vt": v, "n": len(g), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["sunday_by_vol_tercile"] = pd.DataFrame(tt)
    # Saturday+Sunday 48h weekend move
    # hour of day
    H = pd.concat(hr).dropna()
    hh = H.groupby("h")["r"].agg(["mean", "std", "count"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["hour_mean_ret(bps)"] = (hh.assign(mean=hh["mean"] * 1e4))[["mean", "t", "count"]]
    ww = H.groupby("wd")["r"].agg(["mean", "std", "count"]); ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["count"]))
    out["weekday_hourly_mean(bps)"] = (ww.assign(mean=ww["mean"] * 1e4))[["mean", "t", "count"]]
    # general 24h reversal at 00 UTC by vol tercile
    G = pd.concat(grid).dropna(subset=["s", "f24", "vol"])
    G["vt"] = G.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    gg = []
    for v, g in G.groupby("vt"):
        lr = stats.linregress(g["s"], g["f24"]); gg.append({"vt": v, "n": len(g), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["all_days_24h_reversal_by_vol"] = pd.DataFrame(gg)
    # coin-level Sunday slope
    cc = []
    for co, g in S.groupby("coin"):
        lr = stats.linregress(g["s"], g["f48"]); cc.append({"coin": co, "n": len(g), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["sunday_by_coin"] = pd.DataFrame(cc)
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    bw = D.groupby("wd")["book_return"].agg(["mean", "std", "count"]); bw["t"] = bw["mean"] / (bw["std"] / np.sqrt(bw["count"]))
    out["book_by_weekday"] = bw
    q = D["book_return"].quantile([0.01, 0.99])
    out["extreme_book_days_weekday"] = pd.DataFrame({"worst1pct": D[D.book_return <= q.iloc[0]].groupby("wd").size(),
                                                    "best1pct": D[D.book_return >= q.iloc[1]].groupby("wd").size()})
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("year")["book_return"].agg(["mean", "count"])
    return out

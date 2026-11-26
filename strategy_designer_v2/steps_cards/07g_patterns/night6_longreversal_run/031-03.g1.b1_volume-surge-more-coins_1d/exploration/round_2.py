def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = s.pct_change()
            vol20 = r1.shift(1).rolling(20, min_periods=10).std()
            hi60 = b["high"].astype(float).rolling(60, min_periods=30).max()
            df = pd.DataFrame(dict(coin=coin, w=w, day=ts.dt.normalize(), wd=ts.dt.weekday, year=ts.dt.year,
                                   r1=r1, z=r1 / vol20, vol=vol20,
                                   n1=s.shift(-1) / s - 1, n3=s.shift(-3) / s - 1, n7=s.shift(-7) / s - 1,
                                   dhi=s / hi60 - 1, pos=np.arange(len(b))))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for c in ["r1", "n1", "n3", "n7"]:
        d[c + "x"] = d[c] - d.groupby("coin")[c].transform("mean")
    def ct(x, day):
        m = x.notna(); x = x[m]; day = day[m]
        dd = (x - x.mean()).groupby(day).sum(); D = len(dd)
        se = np.sqrt((dd ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series(dict(mean=x.mean(), t=x.mean() / se, n=len(x), days=D))
    res = {}
    # weekday, clustered by day, excess of coin mean, and by year half
    res["weekday_r1x_clustered"] = d.groupby("wd").apply(lambda x: ct(x["r1x"], x["day"])).round(5)
    d["era"] = np.where(d["year"] <= 2021, "2018-21", "2022-25")
    res["saturday_by_era"] = d[d.wd == 5].groupby("era").apply(lambda x: ct(x["r1x"], x["day"])).round(5)
    res["wednesday_by_era"] = d[d.wd == 2].groupby("era").apply(lambda x: ct(x["r1x"], x["day"])).round(5)
    # z-move deciles, next 1/3/7 day excess, non-overlapping grids, clustered
    dz = d.dropna(subset=["z"]).copy()
    dz["q"] = pd.qcut(dz["z"].rank(method="first"), 10, labels=False)
    out = {}
    for h, c in [(1, "n1x"), (3, "n3x"), (7, "n7x")]:
        sub = dz[dz["pos"] % h == 0]
        out[h] = sub.groupby("q").apply(lambda x: ct(x[c], x["day"]))
    res["z_decile_next1x"] = out[1].round(5)
    res["z_decile_next3x_grid"] = out[3].round(5)
    res["z_decile_next7x_grid"] = out[7].round(5)
    # down-day reversal by era and by vol level
    low = dz[dz.q <= 1]
    res["bigdown_next1x_by_era"] = low.groupby("era").apply(lambda x: ct(x["n1x"], x["day"])).round(5)
    # graded: z vs next day excess, slope on z<0 side
    neg = dz[dz.z < 0]
    neg = neg.assign(zb=pd.qcut(neg["z"], 4, labels=False))
    res["neg_z_quartile_next1x"] = neg.groupby("zb").apply(lambda x: pd.concat([pd.Series(dict(zmean=x["z"].mean())), ct(x["n1x"], x["day"])])).round(5)
    # distance from 60-day high, 7-day grid
    dh = d.dropna(subset=["dhi"]); dh = dh[dh["pos"] % 7 == 0].copy()
    dh["q"] = pd.qcut(dh["dhi"].rank(method="first"), 5, labels=False)
    res["dhi60_quint_next7x"] = dh.groupby("q").apply(lambda x: pd.concat([pd.Series(dict(lo=x["dhi"].min())), ct(x["n7x"], x["day"])])).round(5)
    res["dhi60_q4_by_era"] = dh[dh.q == 4].groupby("era").apply(lambda x: ct(x["n7x"], x["day"])).round(5)
    return res

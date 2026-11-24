import numpy as np, pandas as pd

def explore(data):
    res = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame(dict(coin=coin, win=w, day=ts.dt.floor("D"), wd=ts.dt.weekday, yr=ts.dt.year,
                                  r=r1, z=r1 / vol20.shift(1), nxt=r1.shift(-1),
                                  r3=c / c.shift(3) - 1, vol=vol20))
            d["z3"] = d["r3"] / (d["vol"].shift(3) * np.sqrt(3))
            d["nxt3"] = c.shift(-3) / c - 1
            d["pos"] = np.arange(len(d))
            rows.append(d)
    dd = pd.concat(rows)
    dd["cm"] = dd.groupby("coin")["r"].transform("mean")
    dd["ex"] = dd["r"] - dd["cm"]

    def clus(s, val):
        ds = s.groupby("day")[val].mean()
        return pd.Series(dict(n=len(s), days=len(ds), mean=ds.mean(), t=ds.mean() / (ds.std() / np.sqrt(len(ds)))))

    # weekday, clustered by day (mean across coins per day)
    res["wd_clustered"] = dd.dropna(subset=["ex"]).groupby("wd").apply(lambda s: clus(s, "ex"))
    sat = dd[(dd["wd"] == 5)].dropna(subset=["ex"])
    res["sat_by_year"] = sat.groupby("yr").apply(lambda s: clus(s, "ex"))
    wed = dd[(dd["wd"] == 2)].dropna(subset=["ex"])
    res["wed_by_year"] = wed.groupby("yr").apply(lambda s: clus(s, "ex"))
    res["sat_by_coin"] = sat.groupby("coin")["ex"].agg(["count", "mean"]).assign(
        t=lambda x: x["mean"] / (sat.groupby("coin")["ex"].std() / np.sqrt(x["count"])))

    # next-day reversal, clustered by day, and graded slope
    e = dd.dropna(subset=["z", "nxt"]).copy()
    e["nex"] = e["nxt"] - e["cm"]
    e["zq"] = pd.cut(e["z"], [-99, -2, -1, 0, 1, 2, 99])
    res["nextday_z_clustered"] = e.groupby("zq", observed=True).apply(lambda s: clus(s, "nex"))
    e["half"] = np.where(e["yr"] <= 2021, "2018-2021", "2022-2025")
    e["zn"] = np.where(e["z"] < -1, "dn", np.where(e["z"] > 1, "up", "mid"))
    res["nextday_z_by_half"] = e.groupby(["half", "zn"]).apply(lambda s: clus(s, "nex"))
    # 3-day: non-overlapping grid
    g3 = dd[(dd["pos"] % 3 == 0)].dropna(subset=["z3", "nxt3"]).copy()
    g3["cm3"] = g3.groupby("coin")["nxt3"].transform("mean")
    g3["ex3"] = g3["nxt3"] - g3["cm3"]
    g3["q"] = pd.qcut(g3["z3"], 5, labels=False)
    res["3d_after_3d_z_q5"] = g3.groupby("q").apply(lambda s: clus(s, "ex3"))

    # book: largest gains/losses days, what came before
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["prev"] = d["coin_return"].shift(1); bk.append(d)
    bk = pd.concat(bk).dropna(subset=["book_return"])
    bd = bk.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    bd["q"] = pd.qcut(bd["book"], 10, labels=False, duplicates="drop")
    res["book_deciles"] = bd.groupby("q")[["book", "coin"]].mean()
    bd["wd"] = pd.to_datetime(bd.index).weekday
    res["book_by_wd"] = bd.groupby("wd")["book"].agg(["count", "mean"]).assign(
        t=lambda x: x["mean"] / (bd.groupby("wd")["book"].std() / np.sqrt(x["count"])))
    return res

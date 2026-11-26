def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol60 = r1.rolling(60, min_periods=20).std()
            vol10 = r1.rolling(10, min_periods=8).std()
            z = r1 / vol60
            sgn = np.sign(r1.fillna(0))
            streak = []
            s = 0
            for v in sgn:
                if v == 0: s = 0
                elif s * v > 0: s += v
                else: s = v
                streak.append(s)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "z": z, "streak": streak,
                "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "vr": vol10 / vol60, "vol60": vol60,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = d["ts"].dt.floor("D")
    d["wd"] = d["ts"].dt.weekday
    out = {}
    for h, col in [(1, "f1"), (2, "f2"), (5, "f5")]:
        drift = d[d["pos"] % h == 0].groupby("coin")[col].mean()
        d["x%d" % h] = d[col] - d["coin"].map(drift)
    def tab(g, h, key):
        x = "x%d" % h
        s = g[(g["pos"] % h == 0)].dropna(subset=[x, key])
        res = []
        for k, gg in s.groupby(key):
            pd_ = gg.groupby("day")[x].sum()
            n = len(gg)
            m = gg[x].mean()
            t = pd_.mean() / (pd_.std(ddof=1) / np.sqrt(len(pd_))) if len(pd_) > 2 else np.nan
            res.append((k, n, round(m * 100, 3), round(t, 2)))
        return pd.DataFrame(res, columns=[key, "n", "mean_excess_%", "t_dayclust"]).set_index(key)
    d["zq"] = pd.cut(d["z"], [-np.inf, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, np.inf])
    out["z bucket fwd2"] = tab(d, 2, "zq")
    out["z bucket fwd5"] = tab(d, 5, "zq")
    d["stk"] = d["streak"].clip(-5, 5)
    out["streak fwd2"] = tab(d, 2, "stk")
    out["streak fwd5"] = tab(d, 5, "stk")
    d["r20q"] = pd.qcut(d["r20p"], 5, labels=False)
    out["20d return quintile fwd5"] = tab(d, 5, "r20q")
    d["vrq"] = pd.qcut(d["vr"], 4, labels=False)
    out["vol ratio 10/60 quartile fwd5"] = tab(d, 5, "vrq")
    # down-z conditioned by vol ratio
    dz = d[d["z"] < -1.5].copy()
    out["big falls by vol-ratio quartile fwd2"] = tab(dz, 2, "vrq")
    out["big falls by 20d return quintile fwd2"] = tab(dz, 2, "r20q")
    out["weekday next-day excess"] = tab(d, 1, "wd")
    d["year"] = d["ts"].dt.year
    out["big falls by year fwd2"] = tab(dz.assign(year=dz["ts"].dt.year), 2, "year")
    out["big falls by coin fwd2"] = tab(dz, 2, "coin")
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            bd.append(t.assign(coin=coin, win=w))
    bd = pd.concat(bd)
    book = bd.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    q = book["book_return"].quantile([0.02, 0.98])
    out["book worst 2% days: mean book, mean coin"] = book[book.book_return <= q.iloc[0]].mean()
    out["book best 2% days: mean book, mean coin"] = book[book.book_return >= q.iloc[1]].mean()
    out["book-coin daily corr"] = float(book.corr().iloc[0, 1])
    return out

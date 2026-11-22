import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 6, 42, 84]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            r24 = c / c.shift(6) - 1
            rng = (hi.rolling(6).max() - lo.rolling(6).min()) / c
            rm = rng / rng.rolling(180, min_periods=60).mean()
            vol = r1.rolling(180, min_periods=60).std()
            volrank = vol / vol.rolling(540, min_periods=120).mean()
            r7d = c / c.shift(42) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "r24z": r24 / (vol * np.sqrt(6)), "rm": rm, "volrank": volrank,
                               "r7dz": r7d / (vol * np.sqrt(42)),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "hour": ts.dt.hour, "wd": ts.dt.weekday})
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon on grid
    for h in H:
        g = A[A.pos % h == 0]
        d = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A.coin.map(d)

    def summ(sub, h, by):
        s = sub[sub.pos % h == 0].dropna(subset=[f"x{h}", by] if isinstance(by, str) else [f"x{h}"])
        gg = s.groupby(by)[f"x{h}"]
        out = pd.DataFrame({"mean%": gg.mean() * 100, "n": gg.count()})
        out["t"] = gg.mean() / (gg.std() / np.sqrt(gg.count()))
        return out.round(3)

    A["r24q"] = pd.qcut(A.r24z, 10, labels=False, duplicates="drop")
    A["rmq"] = pd.qcut(A.rm, 5, labels=False, duplicates="drop")
    A["volq"] = pd.qcut(A.volrank, 5, labels=False, duplicates="drop")
    A["r7q"] = pd.qcut(A.r7dz, 5, labels=False, duplicates="drop")
    A["fcq"] = np.where(A.fc > 0, pd.qcut(A.fc.where(A.fc > 0), 4, labels=False, duplicates="drop"), -1)
    res = {}
    res["r24 decile -> next 24h"] = summ(A, 6, "r24q")
    res["r24 decile -> next 7d"] = summ(A, 42, "r24q")
    res["r24 decile -> next 14d"] = summ(A, 84, "r24q")
    A["sgn"] = np.sign(A.r24z)
    res["range mult q x sign -> 24h"] = summ(A, 6, ["sgn", "rmq"])
    res["range mult q x sign -> 7d"] = summ(A, 42, ["sgn", "rmq"])
    res["vol level q -> 24h"] = summ(A, 6, "volq")
    res["vol level q -> 7d"] = summ(A, 42, "volq")
    res["7d ret quintile -> 7d"] = summ(A, 42, "r7q")
    res["7d ret quintile -> 24h"] = summ(A, 6, "r7q")
    res["forecast q -> 24h"] = summ(A, 6, "fcq")
    res["forecast q -> 7d"] = summ(A, 42, "fcq")
    res["hour -> next 4h"] = summ(A, 1, "hour")
    res["weekday -> next 4h"] = summ(A, 1, "wd")
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["yr"] = pd.to_datetime(bk.index.get_level_values("day")).year
    res["book vs hold by year"] = bk.groupby("yr").agg(book_mean=("book_return", "mean"),
                                                       hold_mean=("coin_return", "mean"),
                                                       n=("book_return", "count")).round(5)
    q = bk.book_return.quantile([0.02, 0.98])
    bk["cls"] = np.where(bk.book_return <= q.iloc[0], "worst2%", np.where(bk.book_return >= q.iloc[1], "best2%", "mid"))
    res["book extreme days, coin ret same day"] = bk.groupby("cls").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count")).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["dur_d"] = T.duration_minutes / 1440
    T["durq"] = pd.qcut(T.dur_d, 4, duplicates="drop")
    res["trades by duration"] = T.groupby("durq").agg(n=("net_profit_loss_percent", "count"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean")).round(3)
    res["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "count"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean")).round(3)
    res["mean |alloc| when fc>0 vs 0"] = A.groupby(A.fc > 0).alloc.agg(["mean", "count"]).round(3)
    return res

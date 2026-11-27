def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            rng = (h - l) / c.shift(1)
            w20 = rng / rng.rolling(20, min_periods=10).mean()
            clv = (c - l) / (h - l).replace(0, np.nan)
            ret5 = c / c.shift(5) - 1
            gap = o / c.shift(1) - 1
            vol20 = r.rolling(20, min_periods=10).std()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"], "r": r, "nxt": nxt, "nxt2": nxt2,
                               "w20": w20, "clv": clv, "ret5": ret5, "vol20": vol20,
                               "regime": b["regime"], "fc": b["forecast"],
                               "pos": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["wd"] = pd.to_datetime(d["ts"]).dt.weekday
    drift = d.groupby("coin")["r"].mean()
    d["drift"] = d["coin"].map(drift)
    d["u1"] = d["nxt"] - d["drift"]
    d["u2"] = d["nxt2"] - 2 * d["drift"]
    d["falling"] = d["regime"].isin(["trending", "unknown"])
    d["up"] = d["r"] > 0
    d = d.dropna(subset=["r", "w20"])

    def ct(s, days):
        x = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna()
        g = x.groupby("d")["v"].sum(); G = len(g)
        if G < 3: return np.nan
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return s.mean() / se

    def summ(sub, col="u1"):
        sub = sub.dropna(subset=[col])
        return pd.Series({"n": len(sub), "days": sub["day"].nunique(), "mean%": 100 * sub[col].mean(),
                          "t_day": ct(sub[col], sub["day"])})

    out = {}
    # 1: by profile x up/down x width quintile, next-day unusual (long direction)
    d["wq"] = d.groupby("coin")["w20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    t = d.groupby(["falling", "up", "wq"]).apply(summ).reset_index()
    out["next1_by_prof_up_widthQ"] = t
    # 2: two-day
    out["next2_by_prof_up_widthQ"] = d.groupby(["falling", "up", "wq"]).apply(lambda s: summ(s, "u2")).reset_index()
    # 3: close location on falling days
    d["cq"] = pd.cut(d["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=False)
    out["next1_falling_by_closeloc"] = d[d["falling"]].groupby("cq").apply(summ).reset_index()
    out["next1_notfalling_by_closeloc"] = d[~d["falling"]].groupby("cq").apply(summ).reset_index()
    # 4: weekday
    out["next1_all_by_weekday"] = d.groupby("wd").apply(summ).reset_index()
    out["next1_falling_by_weekday"] = d[d["falling"]].groupby("wd").apply(summ).reset_index()
    # 5: today's return quintile (sign of move) in falling vs not
    d["rq"] = d.groupby("coin")["r"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["next1_by_prof_retQ"] = d.groupby(["falling", "rq"]).apply(summ).reset_index()
    # 6: volatility level
    d["vq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["next1_falling_up_by_volT"] = d[d["falling"] & d["up"]].groupby("vq").apply(summ).reset_index()
    # 7: book day returns, largest days
    br = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            br.append(x.assign(coin=coin, win=w))
    br = pd.concat(br)
    book = br.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = book["book_return"].quantile([0.02, 0.98])
    out["book_by_window"] = br.groupby("win").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    out["book_extremes_coin_ret"] = pd.Series({
        "best2pct_n": int((book["book_return"] >= q.iloc[1]).sum()),
        "best2pct_coin_ret%": 100 * book.loc[book["book_return"] >= q.iloc[1], "coin_return"].mean(),
        "worst2pct_coin_ret%": 100 * book.loc[book["book_return"] <= q.iloc[0], "coin_return"].mean(),
        "corr_book_coin": book.corr().iloc[0, 1]})
    return out

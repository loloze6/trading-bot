def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            c = b["close"]
            b["ret1"] = c / c.shift(1) - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd3"] = c.shift(-3) / c - 1
            b["sd30"] = b["ret1"].rolling(30, min_periods=20).std()
            b["rng"] = (b["high"] - b["low"]) / c / b["sd30"]
            b["retz"] = b["ret1"] / b["sd30"]
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"]) / hl
            b["ret5"] = c / c.shift(5) - 1
            b["ret60"] = c / c.shift(60) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["fwd1"]
            b["coin"] = coin; b["win"] = w
            b["wd"] = b["ts"].dt.dayofweek
            b["year"] = b["ts"].dt.year
            b["day"] = b["ts"].dt.floor("D")
            b["i"] = np.arange(len(b))
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["fwd1"].mean()
    d["ex1"] = d["fwd1"] - d["coin"].map(drift)
    drift3 = d[d["i"] % 3 == 0].groupby("coin")["fwd3"].mean()
    d["ex3"] = d["fwd3"] - d["coin"].map(drift3)

    def summ(g, col="ex1"):
        x = g.dropna(subset=[col])
        if len(x) < 10: return pd.Series({"n": len(x)})
        s = x.groupby("day")[col].sum()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s)))
        return pd.Series({"n": len(x), "days": len(s), "mean%": 100 * x[col].mean(), "t_day": t})

    out = {}
    d["up"] = np.where(d["ret1"] > 0, "up", "down")
    d["rq"] = d.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["side x range quintile, next-day excess"] = d.groupby(["up", "rq"]).apply(summ)
    d["zq"] = d.groupby("coin")["retz"].transform(lambda s: pd.qcut(s, 7, labels=False, duplicates="drop"))
    out["retz septile, next-day excess"] = d.groupby("zq").apply(summ)
    d["cq"] = pd.cut(d["clv"], [0, .2, .4, .6, .8, 1.0], include_lowest=True, labels=False)
    out["close location in range quintile, next-day"] = d.groupby("cq").apply(summ)
    out["close location, wide days (rq>=3)"] = d[d["rq"] >= 3].groupby("cq").apply(summ)
    out["close location, 3-day excess (grid)"] = d[d["i"] % 3 == 0].groupby("cq").apply(lambda g: summ(g, "ex3"))
    d["tr"] = pd.cut(d["ret60"], [-10, -.1, .1, 100], labels=["falling", "choppy", "rising"])
    out["trend x side, next-day excess"] = d.groupby(["tr", "up"]).apply(summ)
    out["weekday next-day excess"] = d.groupby("wd").apply(summ)
    d["q5"] = d.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["5-day return quintile, next-day excess"] = d.groupby("q5").apply(summ)
    out["by coin, up days: excess (short dir neg = fade works)"] = d[d["up"] == "up"].groupby("coin").apply(summ)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["day"] = pd.to_datetime(dd["day"])
    bk = dd.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    bk["wd"] = bk.index.dayofweek
    out["book by weekday"] = bk.groupby("wd")["br"].agg(["count", "mean", "std"])
    bk["cq"] = pd.qcut(bk["cr"], 5, labels=False)
    out["book by coin-return quintile"] = bk.groupby("cq")[["br", "cr"]].mean()
    out["book corr with coins"] = float(bk["br"].corr(bk["cr"]))
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series({"n": len(tr), "mean pl%": tr["profit_loss_percent"].mean(), "mean net%": tr["net_profit_loss_percent"].mean(), "mean dur h": tr["duration_minutes"].mean() / 60})
    return out

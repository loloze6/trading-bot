def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w})
            d["pos"] = np.arange(len(b))
            d["r1"] = c.pct_change()
            d["r3"] = c / c.shift(3) - 1
            d["r20"] = c / c.shift(20) - 1
            d["r60"] = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]).astype(float)
            d["clv"] = ((c - b["low"]) / rng.replace(0, np.nan))
            d["vol30"] = d["r1"].rolling(30).std()
            d["f5"] = c.shift(-5) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"] = b["postRebalance_current_allocation"].values
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift5 = df[df.pos % 5 == 0].groupby("coin")["f5"].mean()
    sd5 = df[df.pos % 5 == 0].groupby("coin")["f5"].std()
    df["u5"] = df["f5"] - df["coin"].map(drift5)
    df["s5"] = df["u5"] / df["coin"].map(sd5)
    vmed = df.groupby("coin")["vol30"].median()
    df["agit"] = df["vol30"] > df["coin"].map(vmed)
    df["trend"] = np.where(df.r60 > .1, "rising", np.where(df.r60 < -.1, "falling", "choppy"))
    df.loc[df.r60.isna(), "trend"] = np.nan
    g = df[(df.pos % 5 == 0) & df.u5.notna()].copy()

    def summ(x, col="u5"):
        x = x.dropna(subset=[col])
        if len(x) < 3:
            return pd.Series({"n": len(x)})
        dd = x.groupby("day")[col].sum()
        nd = len(dd)
        t = dd.mean() / (dd.std() / np.sqrt(nd)) if nd > 2 else np.nan
        return pd.Series({"n": len(x), "days": nd, "mean_u5": x[col].mean(),
                          "strength": x["s5"].mean(), "t_day": t})

    out = {}
    g["r20b"] = pd.cut(g.r20, [-1, -.3, -.2, -.15, -.1, -.05, 0, .05, .1, .2, .3, 10])
    out["choppy by r20 bin (u5, long side)"] = g[g.trend == "choppy"].groupby("r20b").apply(summ)
    out["all trends by r20 bin"] = g.groupby("r20b").apply(summ)
    out["trend x deep fall (r20<=-10%)"] = g[g.r20 <= -.1].groupby(["trend", "agit"]).apply(summ)
    g["clvb"] = pd.cut(g.clv, [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["choppy agit by clv"] = g[(g.trend == "choppy") & g.agit].groupby("clvb").apply(summ)
    out["all by clv x trend"] = g.groupby(["trend", "clvb"]).apply(summ)
    g["r1b"] = pd.qcut(g.r1 / g.vol30, 5)
    out["by scaled 1d move quintile x agit"] = g.groupby(["agit", "r1b"]).apply(summ)
    g["r3b"] = pd.qcut(g.r3 / g.vol30, 5)
    out["choppy by scaled 3d move quintile"] = g[g.trend == "choppy"].groupby("r3b").apply(summ)
    out["by weekday"] = g.groupby("wd").apply(summ)
    out["by window"] = g.groupby("win").apply(summ)
    # book daily: biggest gains/losses
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; dl.append(x)
    D = pd.concat(dl)
    act = D[D.book_return.abs() > 1e-9]
    out["book active coin-days"] = pd.Series({"n": len(act), "mean_book": act.book_return.mean(),
                                              "mean_coin": act.coin_return.mean(),
                                              "corr": act.book_return.corr(act.coin_return)})
    out["book by coin"] = act.groupby("coin")["book_return"].agg(["count", "mean", "sum"])
    out["book by window"] = act.groupby("win")["book_return"].agg(["count", "mean", "sum"])
    return out

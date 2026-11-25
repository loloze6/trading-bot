def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    dayrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": b["postRebalance_current_allocation"].astype(float),
                              "fc": b["forecast"].astype(float), "regime": b["regime"].astype(str)})
            d["r1"] = c.pct_change()
            d["fwd"] = c.shift(-1) / c - 1
            d["ret60"] = c / c.shift(60) - 1
            d["ret7"] = c / c.shift(7) - 1
            d["ret3"] = c / c.shift(3) - 1
            sd30 = d["r1"].rolling(30).std()
            d["z"] = d["r1"] / sd30
            d["gain"] = d["pos"] * d["fwd"]
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["i"] = np.arange(len(d))
            rows.append(d)
        for w, dd in data["days"][coin].items():
            x = dd[["day", "book_return", "coin_return"]].copy()
            x["coin"] = coin; x["win"] = w
            dayrows.append(x)
    A = pd.concat(rows, ignore_index=True)
    D = pd.concat(dayrows, ignore_index=True)
    D["wn"] = D["win"].str[1:].astype(int)
    book = D.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "day"])
    v = (1 + book["book_return"]).cumprod()
    dd_ = v / v.cummax() - 1
    book["dd"] = dd_.values
    out["book by window"] = book.groupby("wn").agg(mean=("book_return", "mean"), sd=("book_return", "std"),
                                                     tot=("book_return", lambda s: (1 + s).prod() - 1),
                                                     worst_day=("book_return", "min"), mindd=("dd", "min"))
    out["deepest dd"] = float(dd_.min())
    # worst book days
    wd = book.nsmallest(15, "book_return")
    out["worst 15 days: window counts"] = wd["wn"].value_counts()
    out["worst 15 days mean"] = float(wd["book_return"].mean())
    # trend profile
    A["trend"] = np.where(A["ret60"].isna(), "na", np.where(A["ret60"] > 0.10, "rising", np.where(A["ret60"] < -0.10, "falling", "choppy")))
    held = A[A["pos"] > 0]
    mean_all = A.groupby("coin")["r1"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(mean_all)
    held = A[A["pos"] > 0]
    def agg(g):
        return pd.Series({"n": len(g), "gain_mean": g["gain"].mean(), "gain_sum": g["gain"].sum(),
                          "fwd_mean": g["fwd"].mean(), "fwd_t": g["fwd"].mean() / g["fwd"].std() * np.sqrt(len(g)),
                          "gain_min": g["gain"].min(), "pos_mean": g["pos"].mean()})
    out["held by trend"] = held.groupby("trend").apply(agg)
    held = held.copy()
    held["r7b"] = pd.cut(held["ret7"], [-9, -0.2, -0.1, -0.03, 0.03, 9])
    out["held by prior 7d return"] = held.groupby("r7b").apply(agg)
    held["zb"] = pd.cut(held["z"], [-99, -2.5, -1.5, -1, -0.5, 0, 99])
    out["held by z of day"] = held.groupby("zb").apply(agg)
    held["fcb"] = pd.qcut(held["fc"].rank(method="first"), 4, labels=False)
    out["held by forecast quartile"] = held.groupby("fcb").apply(agg)
    out["held by year"] = held.groupby("year").apply(agg)
    # agitated profile bars (regime != chop), down vs up days
    ag = A[(A["regime"] != "chop") & A["fwd"].notna() & A["r1"].notna()]
    ag = ag.assign(down=ag["r1"] < 0)
    out["agitated: down vs up next-day ex"] = ag.groupby(["trend", "down"])["ex"].agg(["count", "mean", "std"])
    # pos size and big losses
    out["pos dist"] = held["pos"].describe()
    out["share gain loss tail"] = float(held.loc[held["gain"] < held["gain"].quantile(0.02), "gain"].sum() / held["gain"].sum())
    return out

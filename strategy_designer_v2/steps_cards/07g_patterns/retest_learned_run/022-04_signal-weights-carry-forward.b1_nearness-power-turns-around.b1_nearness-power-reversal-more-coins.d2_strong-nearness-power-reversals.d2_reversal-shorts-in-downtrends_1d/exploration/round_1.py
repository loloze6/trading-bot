def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            hi30 = c.rolling(30, min_periods=30).max()
            near = c / hi30 - 1
            rng = (b["high"] - b["low"]) / c
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            fc = b["forecast"].astype(float)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c.iloc[i + H] / c.iloc[i] - 1,
                                 r1=r1.iloc[i], r5=ret5.iloc[i], r20=ret20.iloc[i],
                                 vol=vol20.iloc[i], near=near.iloc[i], rng=rng.iloc[i],
                                 wd=wd.iloc[i], fc=fc.iloc[i], wi=int(w[1:])))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    # vol relative to coin's own median vol
    df["volrel"] = df["vol"] / df.groupby("coin")["vol"].transform("median")

    def tab(col, q=5, data_=None):
        d = (data_ if data_ is not None else df).dropna(subset=[col, "ex"]).copy()
        d["b"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        g = d.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                               mean_ex=("ex", "mean"), sd=("ex", "std"))
        g["t"] = g["mean_ex"] / (g["sd"] / np.sqrt(g["n"]))
        return g.drop(columns="sd").round(4)

    out = {}
    out["by_r1"] = tab("r1")
    out["by_r5"] = tab("r5")
    out["by_r20"] = tab("r20")
    out["by_volrel"] = tab("volrel")
    out["by_near30"] = tab("near")
    out["by_range"] = tab("rng")
    neg = df[df["r20"] < 0]
    out["r20neg_by_r5"] = tab("r5", data_=neg)
    out["r20neg_by_volrel"] = tab("volrel", data_=neg)
    pos = df[df["r20"] >= 0]
    out["r20pos_by_r5"] = tab("r5", data_=pos)
    g = df.groupby("wd")["ex"].agg(["size", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["by_weekday"] = g.round(4)
    # forecast buckets
    f = df.dropna(subset=["fc"]).copy()
    f["fb"] = pd.cut(f["fc"], [-21, -6, -4, -2, -1e-9, 1e-9, 21], labels=["<=-6", "-6..-4", "-4..-2", "-2..0", "0", ">0"])
    g = f.groupby("fb", observed=True)["ex"].agg(["size", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["by_forecast_ex(long sign)"] = g.round(4)
    act = f[f["fc"] < 0].copy()
    act["short_ex"] = -act["ex"]
    out["active_short_by_volrel"] = tab("volrel", 4, act.assign(ex=act["short_ex"]))
    out["active_short_by_r5"] = tab("r5", 4, act.assign(ex=act["short_ex"]))
    out["active_short_by_r20"] = tab("r20", 4, act.assign(ex=act["short_ex"]))
    # by year-ish: window group
    act["wg"] = pd.cut(act["wi"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    g = act.groupby("wg", observed=True)["short_ex"].agg(["size", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["active_short_by_windowgroup"] = g.round(4)
    # book daily
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = coin; dd["w"] = w
            dl.append(dd)
    D = pd.concat(dl).dropna()
    bk = D.groupby(["w", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.weekday
    out["book_by_weekday"] = bk.groupby("wd")["book"].agg(["size", "mean"]).round(5)
    q = bk["book"].quantile([0.02, 0.98]).values
    out["coin_ret_on_book_worst2%"] = float(bk.loc[bk["book"] <= q[0], "coin"].mean())
    out["coin_ret_on_book_best2%"] = float(bk.loc[bk["book"] >= q[1], "coin"].mean())
    out["corr_book_coin"] = float(bk["book"].corr(bk["coin"]))
    out["n_grid_cases"] = len(df)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 120
    rows = []
    hrows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mad = r24.abs().rolling(720, min_periods=500).mean()
            z24 = r24 / mad
            r168 = c / c.shift(168) - 1
            z168 = r168 / (mad * np.sqrt(7))
            prox = c / c.rolling(720, min_periods=500).max() - 1
            low = c / c.rolling(720, min_periods=500).min() - 1
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=500).std()
            r720 = c / c.shift(720) - 1
            fwd = c.shift(-H) / c - 1
            fwd24 = c.shift(-24) / c - 1
            idx = np.arange(0, len(c), H)
            d = pd.DataFrame({"z24": z24, "z168": z168, "prox": prox, "low": low, "vol": vol,
                              "r720": r720, "fwd": fwd, "fc": b["forecast"].reset_index(drop=True)}).iloc[idx]
            d["w"] = w
            recs.append(d)
            # hourly: next-bar return
            nx = r1.shift(-1)
            z1 = r1 / vol
            hh = pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "nx": nx, "z1": z1,
                               "f24": fwd24, "coin": coin})
            hrows.append(hh)
        dd = pd.concat(recs)
        g = dd["fwd"].dropna()
        dd["u"] = (dd["fwd"] - g.mean()) / g.std()
        dd["ub"] = dd["fwd"] - g.mean()
        dd["volr"] = dd["vol"].rank(pct=True)
        dd["coin"] = coin
        rows.append(dd)
    D = pd.concat(rows).dropna(subset=["u", "z24", "prox", "vol"])
    out = {}
    def tab(col, q=5):
        x = D.copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        r = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("u", "size"),
                                 strength=("u", "mean"), unusual=("ub", "mean"),
                                 sd=("u", "std"))
        r["t"] = r["strength"] / (r["sd"] / np.sqrt(r["n"]))
        return r.drop(columns="sd")
    for col in ["z24", "z168", "prox", "low", "volr", "r720"]:
        out["fwd120 by " + col] = tab(col)
    # interaction prox x z168
    x = D.copy()
    x["pb"] = pd.qcut(x["prox"], 3, labels=False); x["zb"] = pd.qcut(x["z168"], 3, labels=False)
    out["strength prox3 x z168_3"] = x.pivot_table(index="pb", columns="zb", values="u", aggfunc="mean")
    out["n prox3 x z168_3"] = x.pivot_table(index="pb", columns="zb", values="u", aggfunc="size")
    # by coin, by window-year-ish: by window
    out["strength by coin, prox top quintile minus bottom"] = D.groupby("coin").apply(
        lambda y: y.loc[y.prox >= y.prox.quantile(.8), "u"].mean() - y.loc[y.prox <= y.prox.quantile(.2), "u"].mean())
    Hh = pd.concat(hrows).dropna()
    Hh["nxs"] = Hh.groupby("coin")["nx"].transform(lambda s: s - s.mean())
    hr = Hh.groupby("hour")["nxs"].agg(["mean", "std", "size"])
    hr["t"] = hr["mean"] / (hr["std"] / np.sqrt(hr["size"])); hr["mean_bps"] = hr["mean"] * 1e4
    out["next1h by hour"] = hr[["mean_bps", "t", "size"]]
    wd = Hh.groupby("wd")["nxs"].agg(["mean", "std", "size"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"])); wd["mean_bps"] = wd["mean"] * 1e4
    out["next1h by weekday"] = wd[["mean_bps", "t", "size"]]
    # after large 1h moves: next 24h, on 24h grid
    G = Hh.iloc[::24].copy()
    G["f24s"] = G.groupby("coin")["f24"].transform(lambda s: s - s.mean())
    G["b"] = pd.qcut(G["z1"], 7, labels=False, duplicates="drop")
    t1 = G.groupby("b").agg(lo=("z1", "min"), hi=("z1", "max"), n=("f24s", "size"), m=("f24s", "mean"), sd=("f24s", "std"))
    t1["t"] = t1["m"] / (t1["sd"] / np.sqrt(t1["n"])); t1["m_bps"] = t1["m"] * 1e4
    out["next24h by 1h move z"] = t1[["lo", "hi", "n", "m_bps", "t"]]
    # book: daily returns, largest days and coin prior returns
    ds = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            x = dy.copy(); x["coin"] = coin; x["w"] = w
            x["prev5"] = (1 + x["coin_return"]).rolling(5).apply(np.prod, raw=True).shift(1) - 1
            ds.append(x)
    Dy = pd.concat(ds).dropna(subset=["book_return"])
    Dy["active"] = Dy["book_return"].abs() > 1e-9
    out["book: share active days, mean book ret active"] = pd.Series({
        "share_active": Dy["active"].mean(),
        "mean_book_active": Dy.loc[Dy.active, "book_return"].mean(),
        "mean_coin_active": Dy.loc[Dy.active, "coin_return"].mean(),
        "mean_coin_all": Dy["coin_return"].mean()})
    A = Dy[Dy.active].copy()
    A["q"] = pd.qcut(A["book_return"], 10, labels=False)
    out["book decile: prev5 coin ret, coin ret"] = A.groupby("q").agg(book=("book_return", "mean"), prev5=("prev5", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            x = t.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T)
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry fc quartile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), fc=("entry_forecast", "mean"), net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda s: s.mean() / 60))
    T["hr"] = pd.to_datetime(T["entry_time"]).dt.hour
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    return out

def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float).reset_index(drop=True)
            d = pd.DataFrame(index=range(len(b)))
            d["coin"] = coin; d["win"] = w
            d["r1"] = c.pct_change()
            d["std30"] = d["r1"].rolling(30, min_periods=20).std()
            d["z"] = d["r1"] / d["std30"]
            d["r5p"] = c / c.shift(5) - 1
            d["z5"] = d["r5p"] / (d["std30"] * np.sqrt(5))
            d["fwd5"] = c.shift(-5) / c - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["ret60"] = c / c.shift(60) - 1
            d["dist20"] = c / c.rolling(20, min_periods=10).max() - 1
            hi = b["high"].astype(float).values; lo = b["low"].astype(float).values
            rng = hi - lo
            d["clv"] = np.where(rng > 0, (c.values - lo) / np.where(rng > 0, rng, 1), np.nan)
            d["calmchop"] = (b["regime"] == "unknown").values
            d["fc"] = b["forecast"].astype(float).values
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year.values
            d["grid"] = (np.arange(len(b)) % 5) == 0
            d["grid1"] = True
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    cm = D[D["grid"]].groupby("coin")["fwd5"].mean()
    D["ex5"] = D["fwd5"] - D["coin"].map(cm)
    cm1 = D.groupby("coin")["fwd1"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(cm1)
    g = D[D["grid"]].dropna(subset=["ex5"]).copy()
    out = {}
    def summ(x):
        x = pd.Series(x).dropna(); n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 and x.std() > 0 else np.nan
        return pd.Series({"n": float(n), "mean": x.mean(), "t": t})
    def tab(df, keys, col):
        r = {}
        for k, s in df.groupby(keys, observed=True):
            r[k if not isinstance(k, tuple) else " | ".join(map(str, k))] = summ(s[col])
        return pd.DataFrame(r).T
    def slope(df, x, y):
        s = df.dropna(subset=[x, y])
        if len(s) < 10: return (np.nan, np.nan, len(s))
        sl = stats.linregress(s[x], s[y]); return (sl.slope, sl.slope / sl.stderr, len(s))
    def sec(name, f):
        try: out[name] = f()
        except Exception as e: out[name] = "err: " + str(e)[:80]
    gz = g.dropna(subset=["z"]).copy()
    gz["zb"] = pd.cut(gz["z"], [-99, -2, -1, 0, 1, 2, 99]).astype(str)
    gz["tr"] = pd.cut(gz["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"]).astype(str)
    sec("A_ex5_by_z_calmchop", lambda: tab(gz, ["calmchop", "zb"], "ex5"))
    sec("B_slope_ex5_on_z", lambda: pd.DataFrame({**{f"calmchop={k}": slope(s, "z", "ex5") for k, s in gz.groupby("calmchop")},
                                                     **{f"tr={k}": slope(s, "z", "ex5") for k, s in gz.groupby("tr")}}, index=["slope", "t", "n"]).T)
    sec("C_ex5_by_z_trend", lambda: tab(gz, ["tr", "zb"], "ex5"))
    g5 = gz.dropna(subset=["z5"]).copy()
    g5["z5b"] = pd.cut(g5["z5"], [-99, -1.5, -0.5, 0.5, 1.5, 99]).astype(str)
    sec("D_ex5_by_past5z_trend", lambda: tab(g5, ["tr", "z5b"], "ex5"))
    sec("D2_ex5_by_past5z_calmchop", lambda: tab(g5[g5["calmchop"]], ["z5b"], "ex5"))
    gz["volt"] = gz.groupby("coin")["std30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    sec("E_ex5_by_vol_tercile", lambda: tab(gz, ["volt"], "ex5"))
    gd = g.dropna(subset=["dist20"]).copy()
    gd["db"] = pd.cut(gd["dist20"], [-9, -0.2, -0.1, -0.05, -0.0001, 0.01]).astype(str)
    sec("F_ex5_by_dist20", lambda: tab(gd, ["db"], "ex5"))
    sec("F2_ex5_by_dist20_trend", lambda: tab(gd.assign(tr=pd.cut(gd["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"]).astype(str)), ["tr", "db"], "ex5"))
    gc = g.dropna(subset=["clv"]).copy()
    gc["cb"] = pd.cut(gc["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01]).astype(str)
    sec("J_ex5_by_closeloc", lambda: tab(gc, ["cb"], "ex5"))
    sec("G_ex1_by_weekday", lambda: tab(D.dropna(subset=["ex1"]), ["wd"], "ex1"))
    gf = g[(g["calmchop"]) & (g["fc"] > 0)].copy()
    sec("H_ex5_by_forecast_q", lambda: tab(gf.assign(fq=pd.qcut(gf["fc"].rank(method="first"), 4, labels=False)), ["fq"], "ex5"))
    sec("H2_calmchop_fc0", lambda: summ(g[(g["calmchop"]) & (g["fc"] <= 0)]["ex5"]))
    sec("H3_calmchop_by_year", lambda: tab(g[g["calmchop"]], ["year"], "ex5"))
    sec("K_ex5_by_year_all", lambda: tab(g, ["year"], "ex5"))
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dl.append(t)
    B = pd.concat(dl, ignore_index=True)
    B["day"] = pd.to_datetime(B["day"])
    bk = B.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().reset_index()
    def bookstats():
        q = bk["br"].quantile([0.02, 0.98])
        top = bk[bk["br"] >= q.iloc[1]]; bot = bk[bk["br"] <= q.iloc[0]]
        return pd.DataFrame({"n": [len(top), len(bot), len(bk)], "book": [top.br.mean(), bot.br.mean(), bk.br.mean()],
                             "coin_same_day": [top.cr.mean(), bot.cr.mean(), bk.cr.mean()]}, index=["top2%", "bot2%", "all"])
    sec("L_book_extremes", bookstats)
    sec("L2_book_by_window", lambda: bk.groupby("win").agg(mean=("br", "mean"), sd=("br", "std"), n=("br", "size"), coin=("cr", "mean")))
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tl.append(t.assign(coin=coin))
    if tl:
        T = pd.concat(tl, ignore_index=True)
        sec("I_trades_by_entry_fc", lambda: tab(T.assign(fq=pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)), ["fq"], "net_profit_loss_percent"))
        sec("I2_trades_by_coin", lambda: tab(T, ["coin"], "net_profit_loss_percent"))
    return out

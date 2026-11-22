def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    trades = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min()
            ret30 = c / c.shift(30) - 1
            chop = (c - c.shift(30)).abs() / (hh - ll)
            pos = (c - (hh + ll) / 2) / (hh - ll)
            ret5p = c / c.shift(5) - 1
            ret1p = r1
            vol20 = r1.rolling(20).std()
            hh60 = hi.rolling(60).max(); ll60 = lo.rolling(60).min()
            pos60 = (c - (hh60 + ll60) / 2) / (hh60 - ll60)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "fwd": fwd, "ret30": ret30,
                               "chop": chop, "pos": pos, "pos60": pos60, "ret5p": ret5p, "ret1p": ret1p, "vol20": vol20,
                               "fc": b["forecast"].astype(float), "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "next1": r1.shift(-1)})
            df["vol_rel"] = vol20 / vol20.rolling(60, min_periods=20).mean()
            rows.append(df)
            d = data["days"][coin][w]
            dd = pd.DataFrame({"coin": coin, "w": w, "book": d["book_return"].astype(float).values,
                               "cr": d["coin_return"].astype(float).values})
            dd["yr"] = pd.to_datetime(d["day"]).dt.year.values
            daily.append(dd)
            t = data["trades"][coin][w]
            if len(t):
                tt = t.copy(); tt["coin"] = coin; trades.append(tt)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["i"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = G.groupby("coin")["fwd"].mean(); sd = G.groupby("coin")["fwd"].std()
    G["u"] = G["fwd"] - G["coin"].map(drift)
    G["s"] = G["u"] / G["coin"].map(sd)
    def tab(df, col, q=5):
        x = df.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        r = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("u", "size"), u=("u", "mean"),
                               s=("s", "mean"), sd_=("u", "std"))
        r["t"] = r["u"] / (r["sd_"] / np.sqrt(r["n"]))
        return r.drop(columns="sd_").round(4)
    out = {}
    act = G[G["fc"] < 0]; fall = G[G["ret30"] < 0]; rise = G[G["ret30"] >= 0]
    out["active_by_forecast"] = tab(act, "fc")
    out["fall_by_chop"] = tab(fall, "chop")
    out["rise_by_chop"] = tab(rise, "chop")
    out["all_by_ret30"] = tab(G, "ret30")
    out["all_by_pos30"] = tab(G, "pos")
    out["lowchop_by_pos30"] = tab(G[G["chop"] < G["chop"].median()], "pos")
    out["all_by_pos60"] = tab(G, "pos60")
    out["all_by_ret5p"] = tab(G, "ret5p")
    out["all_by_ret1p"] = tab(G, "ret1p")
    out["all_by_volrel"] = tab(G, "vol_rel")
    wd = G.groupby("wd").agg(n=("u", "size"), u=("u", "mean"), sd_=("u", "std"))
    wd["t"] = wd["u"] / (wd["sd_"] / np.sqrt(wd["n"])); out["grid_by_weekday"] = wd.drop(columns="sd_").round(4)
    yr = G.groupby("yr").agg(n=("u", "size"), u=("u", "mean"), sd_=("u", "std"))
    yr["t"] = yr["u"] / (yr["sd_"] / np.sqrt(yr["n"])); out["grid_by_year"] = yr.drop(columns="sd_").round(4)
    # book
    D = pd.concat(daily, ignore_index=True)
    out["book_by_year"] = D.groupby("yr").agg(n=("book", "size"), book=("book", "mean"), coin=("cr", "mean")).round(5)
    A["gain"] = A["alloc"] * A["next1"]
    cm = A.groupby("coin")["next1"].mean()
    A["mkt"] = A["alloc"] * A["coin"].map(cm)
    a2 = A.dropna(subset=["gain"])
    out["gain_split"] = pd.Series({"mean_gain": a2["gain"].mean(), "market_part": a2["mkt"].mean(),
                                   "timing": a2["gain"].mean() - a2["mkt"].mean(),
                                   "share_bars_short": (a2["alloc"] < 0).mean(), "mean_alloc_short": a2.loc[a2["alloc"] < 0, "alloc"].mean()})
    # gain by days into position: daily next1 conditional on position age
    if trades:
        T = pd.concat(trades, ignore_index=True)
        T["dur_d"] = T["duration_minutes"] / 1440
        T["db"] = pd.cut(T["dur_d"], [0, 5.5, 10, 20, 60, 1000])
        out["trades_by_duration"] = T.groupby("db", observed=True).agg(n=("net_profit_loss_percent", "size"),
            gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean")).round(3)
        out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
            gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median")).round(3)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7b = c / c.shift(7) - 1
            f7 = c.shift(-7) / c - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "reg": b["regime"].astype(str), "fc": b["forecast"].astype(float),
                "s7": r7b / (sd30 * np.sqrt(7)), "s1": r1 / sd30,
                "r7b": r7b, "f7": f7, "f3": f3, "f1": f1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "rng": (b["high"] - b["low"]) / c / sd30,
                "clo": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["inprof"] = D["reg"].isin(["trending", "unknown"])
    g7 = D[D["pos"] % 7 == 0].dropna(subset=["f7"]).copy()
    cm = g7.groupby("coin")["f7"].mean()
    g7["x7"] = g7["f7"] - g7["coin"].map(cm)
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["regime_counts"] = D["reg"].value_counts()
    # 1 forecast buckets
    a = g7[g7["fc"] > 0].copy()
    a["q"] = pd.qcut(a["fc"], 4, labels=False, duplicates="drop")
    out["fc_quartile_x7"] = a.groupby("q")["x7"].apply(summ).unstack()
    # 2 current scaled 7d return in vs out of profile
    for name, sub in [("in", g7[g7["inprof"]]), ("out", g7[~g7["inprof"]])]:
        s = sub.dropna(subset=["s7"]).copy()
        s["q"] = pd.cut(s["s7"], [-99, -1.5, -0.75, -0.25, 0.25, 0.75, 1.5, 99])
        out[f"s7_bins_x7_{name}prof"] = s.groupby("q", observed=True)["x7"].apply(summ).unstack()
        sl = stats.linregress(s["s7"], s["x7"])
        out[f"s7_slope_{name}"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(s)}"
    # 3 daily scaled move next 1/3 days, grid 3
    g3 = D[D["pos"] % 3 == 0].dropna(subset=["f3", "s1"]).copy()
    cm3 = g3.groupby("coin")["f3"].mean()
    g3["x3"] = g3["f3"] - g3["coin"].map(cm3)
    g3["q"] = pd.cut(g3["s1"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["s1_bins_x3_all"] = g3.groupby("q", observed=True)["x3"].apply(summ).unstack()
    out["s1_bins_x3_inprof"] = g3[g3["inprof"]].groupby("q", observed=True)["x3"].apply(summ).unstack()
    # range and close location in profile
    g3["rq"] = pd.qcut(g3["rng"], 4, labels=False, duplicates="drop")
    g3["cq"] = pd.cut(g3["clo"], [0, 0.25, 0.75, 1.0], include_lowest=True)
    out["range_closeloc_x3_inprof"] = g3[g3["inprof"]].groupby(["rq", "cq"], observed=True)["x3"].apply(summ).unstack()
    # 4 weekday
    D1 = D.dropna(subset=["f1"])
    out["weekday_f1"] = D1.groupby("wd")["f1"].apply(summ).unstack()
    out["weekday_f1_inprof"] = D1[D1["inprof"]].groupby("wd")["f1"].apply(summ).unstack()
    # 5 trades
    T = []
    for coin, ws in trades.items():
        for w, t in ws.items():
            if len(t): T.append(t.assign(coin=coin, w=w))
    T = pd.concat(T, ignore_index=True)
    T["q"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades_by_entryfc"] = T.groupby("q")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_window"] = T.groupby("w")["net_profit_loss_percent"].agg(["count", "mean"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    # 6 book days
    BD = []
    for coin, ws in days.items():
        for w, d in ws.items():
            BD.append(d.assign(coin=coin, w=w))
    BD = pd.concat(BD, ignore_index=True)
    bd = BD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bd.groupby("w").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "size"))
    top = bd["book_return"].quantile([0.02, 0.98])
    out["coin_ret_on_extreme_book_days"] = pd.Series({
        "worst2%_book": bd.loc[bd.book_return <= top.iloc[0], "book_return"].mean(),
        "worst2%_coin": bd.loc[bd.book_return <= top.iloc[0], "coin_return"].mean(),
        "best2%_book": bd.loc[bd.book_return >= top.iloc[1], "book_return"].mean(),
        "best2%_coin": bd.loc[bd.book_return >= top.iloc[1], "coin_return"].mean()})
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "r28": c / c.shift(28) - 1,
                "r5": c / c.shift(5) - 1,
                "r1": r1,
                "vol20": r1.rolling(20).std(),
                "vol_ratio": r1.rolling(5).std() / r1.rolling(60).std(),
                "near60": c / c.rolling(60).max(),
                "range1": (b["high"] - b["low"]) / c,
                "volu": b["volume"] / b["volume"].rolling(20).mean(),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            df = df.iloc[::H]
            rows.append(df)
    g = pd.concat(rows)
    g = g.dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}

    def qtab(col, q=5):
        s = g.dropna(subset=[col]).copy()
        s["q"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = s.groupby("q")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        top = s[s.q == q - 1]["ex"]; bot = s[s.q == 0]["ex"]
        t.loc["top-bot", "mean"] = top.mean() - bot.mean()
        t.loc["top-bot", "t"] = stats.ttest_ind(top, bot, equal_var=False).statistic
        return t.round(4)

    for col in ["r28", "r5", "r1", "vol20", "vol_ratio", "near60", "range1", "volu"]:
        out["q_" + col] = qtab(col)
    # r5 within positive vs negative r28
    for side, m in [("r28pos", g.r28 > 0), ("r28neg", g.r28 <= 0)]:
        s = g[m].dropna(subset=["r5"]).copy()
        s["q"] = pd.qcut(s["r5"].rank(method="first"), 5, labels=False)
        out["r5_in_" + side] = s.groupby("q")["ex"].agg(["mean", "count"]).round(4)
    # forecast zero vs positive, abs size of moves
    g["absfwd"] = g["fwd"].abs()
    s = g.dropna(subset=["vol20"]).copy()
    s["q"] = s.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["vol_next_absmove"] = s.groupby("q")["absfwd"].mean().round(4)
    # weekday, daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["year"] = pd.to_datetime(D["day"]).dt.year
    t = D.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["weekday_daily"] = t.round(5)
    out["year_book_vs_coin"] = D.groupby("year")[["book_return", "coin_return"]].mean().round(5)
    out["coin_book"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"]).round(5)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["dur_d"] = tr["duration_minutes"] / 1440
    tr["dq"] = pd.qcut(tr["dur_d"].rank(method="first"), 5, labels=False)
    out["trades_by_dur"] = tr.groupby("dq")[["dur_d", "net_profit_loss_percent"]].agg(["mean", "count"]).round(3)
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entryfc"] = tr.groupby("fq")[["entry_forecast", "net_profit_loss_percent"]].mean().round(3)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            absd = c.diff().abs()
            er = (c - c.shift(30)).abs() / absd.rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            sd30 = r1.rolling(30).std()
            z = r7 / (sd30 * np.sqrt(7))
            vol_rank = sd30
            f7 = c.shift(-7) / c - 1
            f1 = r1.shift(-1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "r7": r7, "r30": r30,
                               "z": z, "sd30": sd30, "f7": f7, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "year": ts.dt.year, "wd": ts.dt.weekday, "r1": r1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 7 == 0)].dropna(subset=["f7", "z", "er"]).copy()
    drift = G.groupby("coin")["f7"].mean()
    usual = G.groupby("coin")["f7"].std()
    G["drift"] = G["coin"].map(drift)
    G["usual"] = G["coin"].map(usual)
    G["dir"] = np.sign(G["r7"])
    G["un"] = (G["f7"] - G["drift"]) * G["dir"]  # unusual move in direction of past week
    G["agree"] = np.sign(G["r7"]) == np.sign(G["r30"])
    G["chop"] = G["er"] <= 0.3
    G["cell"] = np.where(G["chop"], "chop", "trend") + "_" + np.where(G["agree"], "agree", "disagree")
    def summ(g):
        x = g["un"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by_cell"] = G.groupby("cell").apply(summ)
    G["azq"] = G.groupby("cell")["z"].transform(lambda s: pd.qcut(s.abs(), 3, labels=False, duplicates="drop"))
    out["by_cell_absz_tercile"] = G.groupby(["cell", "azq"]).apply(summ)
    G["volq"] = G.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_cell_vol_tercile"] = G.groupby(["cell", "volq"]).apply(summ)
    G["erq"] = pd.qcut(G["er"], 5, labels=False)
    out["by_er_quintile_all"] = G.groupby("erq").apply(summ)
    out["by_year_chop_agree"] = G[G["cell"] == "chop_agree"].groupby("year").apply(summ)
    # raw forward 7d (not signed) by sign of r30 inside chop
    G["r30sign"] = np.sign(G["r30"])
    G["raw"] = G["f7"] - G["drift"]
    out["raw_fwd_by_r30sign_chop"] = G.groupby(["chop", "r30sign"])["raw"].agg(["count", "mean"])
    # 30d return graded continuation
    G["dir30"] = np.sign(G["r30"])
    G["un30"] = (G["f7"] - G["drift"]) * G["dir30"]
    G["z30"] = G["r30"] / (G["sd30"] * np.sqrt(30))
    G["z30q"] = pd.qcut(G["z30"].abs(), 4, labels=False)
    out["by_abs_z30_quartile_signed30"] = G.groupby("z30q")["un30"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby("w").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "size"))
    # weekday of book
    bk2 = bk.reset_index(); bk2["wd"] = pd.to_datetime(bk2["day"]).dt.weekday
    out["book_by_weekday"] = bk2.groupby("wd")["book_return"].agg(["count", "mean"])
    # largest gains/losses: coin return on those days
    q = bk["book_return"].quantile([0.02, 0.98])
    out["extreme_days"] = pd.DataFrame({
        "worst2pct_book": [bk[bk.book_return <= q.iloc[0]]["book_return"].mean(), bk[bk.book_return <= q.iloc[0]]["coin_return"].mean()],
        "best2pct_book": [bk[bk.book_return >= q.iloc[1]]["book_return"].mean(), bk[bk.book_return >= q.iloc[1]]["coin_return"].mean()]},
        index=["book", "coin"])
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["days"], 4, labels=False, duplicates="drop")
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_duration_q"] = T.groupby("dq").agg(n=("days", "size"), days=("days", "mean"), pnl=("net_profit_loss_percent", "mean"))
    T["afq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=False, duplicates="drop")
    out["trades_by_absfc"] = T.groupby("afq")["net_profit_loss_percent"].agg(["count", "mean"])
    return out

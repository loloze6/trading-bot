def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    H = 7
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            b["ret1"] = r1
            b["ret7p"] = c / c.shift(7) - 1
            b["ret14p"] = c / c.shift(14) - 1
            b["ret28p"] = c / c.shift(28) - 1
            b["vol14"] = r1.rolling(14).std()
            b["vol60"] = r1.rolling(60, min_periods=20).std()
            b["volratio"] = b["vol14"] / b["vol60"]
            b["fwd7"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["share"] = b["debug_info.components.rsi_share.last_history_value"]
            b["rng"] = (b["high"] - b["low"]) / b["close"]
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"] = coin; b["win"] = w
            b["grid"] = (np.arange(len(b)) % H) == 0
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    cm = df[df.grid].groupby("coin")["fwd7"].mean()
    df["fwd7x"] = df["fwd7"] - df["coin"].map(cm)
    g = df[df.grid].dropna(subset=["fwd7x"])
    out["n_grid_by_coin"] = g.groupby("coin").size()

    def bucket(col, q=5):
        s = g.dropna(subset=[col]).copy()
        s["b"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = s.groupby("b")["fwd7x"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "count", "t"]]
    for col in ["share", "forecast", "ret1", "ret7p", "ret14p", "ret28p", "vol14", "volratio", "rng"]:
        out["fwd7x_by_q_" + col] = bucket(col)
    # correlation per coin for share and ret28p
    cc = []
    for coin, s in g.groupby("coin"):
        for col in ["share", "ret7p", "ret14p", "ret28p", "volratio"]:
            x = s.dropna(subset=[col])
            r, p = stats.spearmanr(x[col], x["fwd7x"])
            cc.append((coin, col, r, p, len(x)))
    out["spearman_by_coin"] = pd.DataFrame(cc, columns=["coin", "col", "rho", "p", "n"])
    # weekday daily returns
    d1 = df.dropna(subset=["fwd1"])
    wd = d1.groupby("wd")["fwd1"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["fwd1_by_weekday_of_bar"] = wd[["mean", "count", "t"]]
    # book days
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_mean_std"] = pd.Series({"book_mean": bk.book_return.mean(), "book_std": bk.book_return.std(),
                                      "hold_mean": bk.coin_return.mean(), "n": len(bk),
                                      "corr_book_coin": bk.corr().iloc[0, 1]})
    bw = bk.groupby("win")[["book_return", "coin_return"]].sum()
    out["book_sum_by_window"] = bw
    # allocation sign gain
    df["gain"] = df["postRebalance_current_allocation"] * df["fwd1"]
    df["side"] = np.sign(df["postRebalance_current_allocation"]).fillna(0)
    sg = df.dropna(subset=["gain"]).groupby(["coin", "side"])["gain"].agg(["mean", "count", "sum"])
    out["gain_by_side"] = sg
    return out

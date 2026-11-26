def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            dist = (c / hi - 1) / sd
            lo = c.shift(1).rolling(20).min()
            distlo = (c / lo - 1) / sd
            r5p = c / c.shift(5) - 1
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            volpct = sd.rolling(60, min_periods=30).rank(pct=True)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "inprof": (b["regime"] == "unknown").values,
                "fc": b["forecast"].values, "dist": dist.values, "distlo": distlo.values,
                "z1": (r / sd).values, "r5pz": (r5p / (sd * np.sqrt(5))).values,
                "fwd5": fwd5.values, "fwd1": fwd1.values, "volpct": volpct.values,
                "alloc": b["postRebalance_current_allocation"].values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "sd": sd.values})
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["win"] = w
            daily.append(dd)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    out = {}
    def tab(df, col, q=5, name=None):
        d = df.dropna(subset=[col]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex5", "size"),
                               mean_ex5=("ex5", "mean"), sd=("ex5", "std"))
        g["t"] = g["mean_ex5"] / (g["sd"] / np.sqrt(g["n"]))
        return g.drop(columns="sd").round(4)
    for prof, sub in [("in", G[G.inprof]), ("out", G[~G.inprof])]:
        out[f"dist_high_{prof}"] = tab(sub, "dist")
        out[f"dist_low_{prof}"] = tab(sub, "distlo")
        out[f"z1_{prof}"] = tab(sub, "z1")
        out[f"r5pz_{prof}"] = tab(sub, "r5pz")
        out[f"volpct_{prof}"] = tab(sub, "volpct")
    out["fc_in"] = tab(G[G.inprof], "fc")
    # weekday on daily coin returns
    A1 = A.dropna(subset=["fwd1"])
    wd = A1.groupby("wd")["fwd1"].agg(["mean", "std", "size"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday_next_day_ret"] = wd.round(5)
    D = pd.concat(daily, ignore_index=True).dropna(subset=["book_return"])
    bk = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).reset_index()
    out["book_by_window"] = bk.groupby("win").agg(mean=("book", "mean"), sd=("book", "std"), n=("book", "size"),
                                                 hold=("coin", "mean")).round(5)
    q = bk["book"].quantile([0.02, 0.98])
    out["book_tail_share"] = pd.Series({
        "share_gain_top2pct_days": bk.loc[bk.book >= q.iloc[1], "book"].sum() / bk["book"].sum(),
        "share_gain_bottom2pct_days": bk.loc[bk.book <= q.iloc[0], "book"].sum() / bk["book"].sum(),
        "corr_book_hold": bk["book"].corr(bk["coin"])}).round(3)
    return out

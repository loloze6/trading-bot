def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64")})
            d["pos"] = np.arange(len(b))
            vol = r1.rolling(20, min_periods=15).std()
            d["vol"] = vol
            d["dist"] = (c / c.rolling(20).mean() - 1) / (vol * np.sqrt(20))
            d["r1s"] = r1 / vol
            d["r5s"] = (c / c.shift(5) - 1) / (vol * np.sqrt(5))
            d["r20s"] = (c / c.shift(20) - 1) / (vol * np.sqrt(20))
            hl = (b["high"] - b["low"]).astype(float)
            d["clpos"] = ((c - b["low"]) / hl.replace(0, np.nan)) - 0.5
            d["rng"] = (hl / c) / vol
            v = np.log(b["volume"].astype(float).replace(0, np.nan))
            d["volz"] = (v - v.rolling(20).mean()) / v.rolling(20).std()
            d["ret60"] = c / c.shift(60) - 1
            d["choppy"] = (b["regime"] == "unknown").astype(int)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            for h in (1, 3, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # vol level rank per coin (exploratory)
    D["volrk"] = D.groupby("coin")["vol"].rank(pct=True) - 0.5

    def clus(df, x, y):
        df = df[[x, y, "ts"]].dropna()
        if len(df) < 50: return (np.nan, np.nan, len(df), 0)
        X = df[x].values; X = (X - X.mean()) / X.std()
        Y = df[y].values
        A = np.column_stack([np.ones(len(X)), X])
        beta, *_ = np.linalg.lstsq(A, Y, rcond=None)
        e = Y - A @ beta
        inv = np.linalg.inv(A.T @ A)
        g = pd.DataFrame(A * e[:, None]).groupby(df["ts"].values).sum().values
        G = len(g)
        V = inv @ (g.T @ g) @ inv * G / (G - 1)
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(df), G)

    out = {}
    feats = ["dist", "r1s", "r5s", "r20s", "clpos", "rng", "volz", "volrk"]
    res = []
    for h in (1, 3, 10):
        G = D[D["pos"] % h == 0].copy()
        drift = G.groupby("coin")[f"f{h}"].transform("mean")
        G["ex"] = G[f"f{h}"] - drift
        G["tr"] = np.where(G["ret60"] > 0.10, "rising", np.where(G["ret60"] < -0.10, "falling", np.where(G["ret60"].notna(), "choppy", "na")))
        for f in feats:
            for sub, S in [("all", G), ("choppyReg", G[G.choppy == 1]), ("notChoppyReg", G[G.choppy == 0]),
                           ("rising", G[G.tr == "rising"]), ("falling", G[G.tr == "falling"])]:
                s, t, n, g = clus(S, f, "ex")
                res.append({"h": h, "feat": f, "sub": sub, "slope_per_sd_%": s * 100, "t": t, "n": n, "days": g})
    R = pd.DataFrame(res)
    out["strong_slopes_|t|>2"] = R[R.t.abs() > 2].round(3).sort_values("t")
    out["all_slopes_h10_choppy"] = R[(R.h == 10) & (R["sub"].isin(["all", "choppyReg"]))].round(3)
    # weekday next-day
    G1 = D.dropna(subset=["f1"])
    wd = G1.groupby("wd")["f1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_next_day"] = wd.round(5)
    # book
    dd = []
    for coin, wins in days.items():
        for w, t in wins.items():
            x = t[["day", "book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin; dd.append(x)
    DD = pd.concat(dd)
    B = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = B["book_return"].quantile([0.05, 0.95])
    out["book_by_window"] = B.groupby(level=0).agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean")).round(5)
    out["book_tails"] = pd.DataFrame({
        "bottom5%_book": B[B.book_return <= q[0.05]].mean(),
        "top5%_book": B[B.book_return >= q[0.95]].mean(),
        "share_of_total_top5": [B[B.book_return >= q[0.95]].book_return.sum() / B.book_return.sum(), np.nan],
    }).round(5)
    out["corr_book_coin"] = float(B.corr().iloc[0, 1])
    return out

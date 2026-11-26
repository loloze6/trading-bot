def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            b["fwd5"] = c.shift(-5) / c - 1
            b["ret5"] = c / c.shift(5) - 1
            b["ret20"] = c / c.shift(20) - 1
            b["vr30"] = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            b["falling"] = (b["regime"] != "chop").astype(int)
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["alloc"] = b["postRebalance_current_allocation"]
            rows.append(b[["coin","win","pos","day","yr","fwd5","ret5","ret20","vr30","falling","regime","alloc","forecast"]])
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 5 == 0) & A["fwd5"].notna()].copy()
    G["ex"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")

    def stat(df, col="ex"):
        x = df[col].dropna(); d = df.loc[x.index]; n = len(x)
        if n < 5: return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "days": 0})
        m = x.mean(); S = (x - m).groupby(d["day"]).sum()
        se = np.sqrt((S**2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se if se > 0 else np.nan, "days": d["day"].nunique()})

    out = {}
    F = G[(G["falling"] == 1) & G["vr30"].notna()].copy()
    F["vq"] = pd.qcut(F["vr30"].rank(method="first"), 4, labels=False)
    out["falling_vr30_q4"] = F.groupby("vq").apply(stat)
    F["neg5"] = (F["ret5"] < 0).astype(int)
    F["dry"] = (F["vr30"] < 0).astype(int)
    out["falling_dry_x_neg5"] = F.groupby(["dry", "neg5"]).apply(stat)
    out["falling_dry_by_year"] = F[F["dry"] == 1].groupby("yr").apply(stat)
    out["falling_grow_by_year"] = F[F["dry"] == 0].groupby("yr").apply(stat)
    N = G[(G["falling"] == 0) & G["ret20"].notna()].copy()
    N["q"] = N.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["notfalling_ret20_by_year_q1"] = N[N["q"] == 1].groupby("yr").apply(stat)
    out["notfalling_ret20_by_year_q3"] = N[N["q"] == 3].groupby("yr").apply(stat)
    # Book extremes
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["rk"] = pd.qcut(bk["book_return"].rank(method="first"), 20, labels=False)
    out["book_extremes"] = bk.groupby("rk")[["book_return", "coin_return"]].mean().iloc[[0, 1, 18, 19]]
    out["book_share_top5pct_of_total"] = float(bk.loc[bk["rk"] == 19, "book_return"].sum() / bk["book_return"].sum())
    return out

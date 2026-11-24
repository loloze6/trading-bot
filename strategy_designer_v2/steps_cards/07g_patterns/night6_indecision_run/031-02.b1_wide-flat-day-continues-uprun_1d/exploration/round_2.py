def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 40: continue
            c, o, hi, lo = b["close"], b["open"], b["high"], b["low"]
            rng = hi - lo
            r = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            r["pos"] = np.arange(len(b))
            r["ret1"] = c / c.shift(1) - 1
            r["vol20"] = np.log(c).diff().rolling(20).std().shift(1)
            r["width"] = rng / rng.rolling(20).mean()
            r["body"] = (c - o) / rng.replace(0, np.nan)
            r["ret5"] = c / c.shift(6) - 1
            for H in [3, 5, 10]:
                r[f"fwd{H}"] = c.shift(-H) / c - 1
                r[f"cell{H}"] = r["pos"] // H
            r["fwd1"] = c.shift(-1) / c - 1
            rows.append(r)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["z1"] = A["ret1"] / A["vol20"]
    A["yr"] = A["ts"].dt.year

    def prep(H):
        g = A[(A["pos"] % H == 0) & A[f"fwd{H}"].notna()]
        dr = g.groupby("coin")[f"fwd{H}"].mean(); us = g.groupby("coin")[f"fwd{H}"].std()
        A[f"ex{H}"] = A[f"fwd{H}"] - A["coin"].map(dr)
        A[f"st{H}"] = A[f"ex{H}"] / A["coin"].map(us)
    for H in [3, 5, 10]: prep(H)

    def pooled(df, col):
        df = df.dropna(subset=[col]); n = len(df)
        if n < 8: return pd.Series({"n": n, "mean": df[col].mean() if n else np.nan, "t": np.nan, "days": n})
        m = df[col].mean(); d = (df[col] - m).groupby(df["day"]).sum(); D = len(d)
        se = np.sqrt(D / (D - 1) * (d ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se, "days": D})

    def fpc(mask, H):
        s = A[mask & A[f"fwd{H}"].notna()]
        return s.groupby(["coin", "win", f"cell{H}"]).head(1)

    out = {}
    zb = pd.cut(A["z1"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    for H in [3, 5, 10]:
        s = fpc(A["z1"].notna(), H).copy(); s["zb"] = zb.loc[s.index]
        out[f"z1_bins_fwd{H}"] = s.groupby("zb").apply(lambda x: pooled(x, f"ex{H}"))
    s = fpc(A["z1"] > 1.5, 10)
    out["bigup_by_year"] = s.groupby("yr").apply(lambda x: pooled(x, "ex10"))
    out["bigup_by_coin"] = s.groupby("coin").apply(lambda x: pooled(x, "ex10"))
    # graded slope of ex10 on z1 for z1>0, day-pooled residual t
    s = fpc(A["z1"] > 0, 10).dropna(subset=["ex10", "z1"])
    x = s["z1"] - s["z1"].mean(); y = s["ex10"]
    beta = (x * y).sum() / (x ** 2).sum()
    res = y - y.mean() - beta * x
    dd = (x * res).groupby(s["day"]).sum(); D = len(dd)
    se = np.sqrt(D / (D - 1) * (dd ** 2).sum()) / (x ** 2).sum()
    out["slope_ex10_on_z1_upside"] = pd.Series({"beta": beta, "t": beta / se, "n": len(s), "days": D})
    s = fpc(A["z1"] < 0, 10).dropna(subset=["ex10", "z1"])
    x = s["z1"] - s["z1"].mean(); y = s["ex10"]
    beta = (x * y).sum() / (x ** 2).sum(); res = y - y.mean() - beta * x
    dd = (x * res).groupby(s["day"]).sum(); D = len(dd)
    se = np.sqrt(D / (D - 1) * (dd ** 2).sum()) / (x ** 2).sum()
    out["slope_ex10_on_z1_downside"] = pd.Series({"beta": beta, "t": beta / se, "n": len(s), "days": D})
    # wide up big-body by width bins
    s = fpc((A["body"] > 0.5) & A["width"].notna(), 10).copy()
    s["wb"] = pd.cut(s["width"], [0, 1, 1.5, 2, 99])
    out["upbody_by_width"] = s.groupby("wb").apply(lambda x: pooled(x, "ex10"))
    # weekday next-day, day-pooled
    d1 = A.dropna(subset=["fwd1"]).copy(); d1["wd"] = d1["ts"].dt.weekday
    out["weekday_next_day_pooled"] = d1.groupby("wd").apply(lambda x: pooled(x, "fwd1"))
    # book: largest gains/losses days, what precedes
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dl.append(d.assign(coin=coin, win=w))
    Dd = pd.concat(dl, ignore_index=True).dropna(subset=["book_return"])
    bk = Dd.groupby("day")["book_return"].mean()
    out["book_top_bottom"] = pd.Series({"top5_mean": bk.nlargest(10).mean(), "bot10_mean": bk.nsmallest(10).mean(),
                                        "share_gain_top10": bk.nlargest(10).sum() / bk.sum(), "ndays": len(bk)})
    return out

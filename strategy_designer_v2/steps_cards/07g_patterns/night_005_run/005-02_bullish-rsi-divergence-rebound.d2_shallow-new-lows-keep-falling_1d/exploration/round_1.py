def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": r1,
                "r5p": c / c.shift(5) - 1,
                "r30p": c / c.shift(30) - 1,
                "vol20": r1.rolling(20).std(),
                "dist_hi30": c / c.rolling(30).max() - 1,
                "newlow": c < c.shift(1).rolling(30, min_periods=5).min(),
                "newhigh": c > c.shift(1).rolling(30, min_periods=5).max(),
                "f1": c.shift(-1) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "f10": c.shift(-10) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def grid(h):
        g = A[(A["pos"] % h == 0)].dropna(subset=[f"f{h}"])
        return g

    def qtab(feat, h, q=5):
        g = grid(h).dropna(subset=[feat]).copy()
        res = []
        for coin, gg in g.groupby("coin"):
            gg = gg.copy()
            gg["q"] = pd.qcut(gg[feat], q, labels=False, duplicates="drop")
            m = gg[f"f{h}"].mean()
            for qq, x in gg.groupby("q"):
                e = x[f"f{h}"] - m
                res.append({"coin": coin, "q": qq, "n": len(x), "mean_ex": e.mean(),
                            "t": e.mean() / (e.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                            "hit": (x[f"f{h}"] > 0).mean()})
        return pd.DataFrame(res)

    out["r1_q_f1"] = qtab("r1", 1)
    out["r5p_q_f5"] = qtab("r5p", 5)
    out["r30p_q_f10"] = qtab("r30p", 10)
    out["vol20_q_f10"] = qtab("vol20", 10)
    out["disthi_q_f10"] = qtab("dist_hi30", 10)

    # new lows / highs, 10-day, non-overlapping grid
    g = grid(10)
    res = []
    for coin, gg in g.groupby("coin"):
        m = gg["f10"].mean()
        for lab, mask in [("newlow", gg["newlow"]), ("newhigh", gg["newhigh"]), ("other", ~(gg["newlow"] | gg["newhigh"]))]:
            x = gg.loc[mask, "f10"] - m
            res.append({"coin": coin, "set": lab, "n": len(x), "mean_ex": x.mean(),
                        "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["newext_f10"] = pd.DataFrame(res)

    # weekday daily returns
    wdt = A.dropna(subset=["r1"]).groupby(["coin", "wd"])["r1"].agg(["count", "mean", "std"])
    wdt["t"] = wdt["mean"] / (wdt["std"] / np.sqrt(wdt["count"]))
    out["weekday"] = wdt

    # year coin mean daily
    out["year"] = A.dropna(subset=["r1"]).groupby(["coin", "yr"])["r1"].agg(["count", "mean"])

    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            bk.append(d)
    D = pd.concat(bk, ignore_index=True)
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["book_by_win"] = D.groupby("win")["book_return"].agg(["mean", "count"])
    # active share
    out["active_share"] = A.groupby("coin").apply(lambda x: (x["alloc"].abs() > 1e-6).mean())
    return out

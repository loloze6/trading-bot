def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            if n < 40: continue
            ret1 = c.pct_change()
            hh20 = h.shift(1).rolling(20).max()
            vol20 = ret1.rolling(20).std()
            exc = (c / hh20 - 1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "exc": exc, "excv": exc / vol20, "vol20": vol20,
                "wd": ts.dt.weekday, "yr": ts.dt.year,
                "fwd5": c.shift(-5) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "fwd2": c.shift(-2) / c - 1, "fwd10": c.shift(-10) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    g = A[(A["pos"] % 5 == 0)].dropna(subset=["fwd5"]).copy()
    st = g.groupby("coin")["fwd5"].agg(["mean", "std"])
    g["un"] = g["fwd5"] - g["coin"].map(st["mean"])
    g["str"] = g["un"] / g["coin"].map(st["std"])
    def summ(gr, col="un"):
        x = gr[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    b = g[g["exc"] > 0].copy()
    b["half"] = np.where(b["yr"] <= 2021, "<=2021", ">=2022")
    out["brk_by_half"] = b.groupby("half").apply(summ)
    b["eq"] = pd.qcut(b["excv"].rank(method="first"), 3, labels=False)
    out["brk_by_excess_over_vol_tercile"] = b.groupby("eq").apply(summ)
    out["brk_spearman_excv_un"] = pd.Series({"rho": stats.spearmanr(b["excv"], b["un"], nan_policy="omit")[0], "p": stats.spearmanr(b["excv"], b["un"], nan_policy="omit")[1], "n": len(b)})
    out["brk_by_vol_tercile"] = b.assign(vq=g.loc[b.index, "vol20"].rank(pct=True).pipe(lambda s: pd.cut(s, 3, labels=False))).groupby("vq").apply(summ)
    # share of coins with positive breakout mean
    pc = b.groupby("coin")["un"].mean()
    out["brk_coins_positive_share"] = pd.Series({"coins": len(pc), "positive": (pc > 0).sum()})
    # 10-day horizon breakout on 10-grid
    g10 = A[(A["pos"] % 10 == 0)].dropna(subset=["fwd10"]).copy()
    g10["un"] = g10["fwd10"] - g10["coin"].map(g10.groupby("coin")["fwd10"].mean())
    out["brk_10d"] = g10[g10["exc"] > 0].pipe(summ)
    # weekday robustness: 1-day returns of the next day, every bar (non-overlapping at h=1)
    a1 = A.dropna(subset=["fwd1"]).copy()
    a1["un1"] = a1["fwd1"] - a1["coin"].map(a1.groupby("coin")["fwd1"].mean())
    a1["half"] = np.where(a1["yr"] <= 2021, "<=2021", ">=2022")
    out["wd_next_day_by_half"] = a1.groupby(["half", "wd"]).apply(lambda x: summ(x, "un1")).unstack(0)
    g["half"] = np.where(g["yr"] <= 2021, "<=2021", ">=2022")
    out["wd_5d_by_half"] = g.groupby(["half", "wd"]).apply(summ).unstack(0)
    # book: largest gains/losses days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    act = D[D["book_return"] != 0]
    out["book_active_days"] = pd.Series({"active_coin_days": len(act), "mean_book": act["book_return"].mean(), "mean_coin": act["coin_return"].mean(), "corr_book_coin": act["book_return"].corr(act["coin_return"])})
    return out

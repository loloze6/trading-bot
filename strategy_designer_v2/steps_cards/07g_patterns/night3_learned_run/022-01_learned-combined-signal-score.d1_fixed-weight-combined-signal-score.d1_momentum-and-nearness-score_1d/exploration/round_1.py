def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets.extend(list(c[idx + H] / c[idx] - 1))
        drift[coin] = np.mean(rets)
        usual[coin] = np.std(rets)
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            vol_rank = vol20.rolling(120, min_periods=40).rank(pct=True)
            ret28 = c / c.shift(28) - 1
            ret5p = c / c.shift(5) - 1
            hi90 = c.rolling(90, min_periods=30).max()
            dist = c / hi90 - 1
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, f=b["forecast"].iloc[i],
                    mom=b.get("debug_info.components.mom28.post_pipeline_value", pd.Series(np.nan, index=b.index)).iloc[i],
                    hi=b.get("debug_info.components.high90.post_pipeline_value", pd.Series(np.nan, index=b.index)).iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i],
                    r1z=r1.iloc[i] / vol20.iloc[i] if vol20.iloc[i] > 0 else np.nan,
                    r5p=ret5p.iloc[i] / (vol20.iloc[i] * np.sqrt(5)) if vol20.iloc[i] > 0 else np.nan,
                    volr=vol_rank.iloc[i], ret28=ret28.iloc[i], dist=dist.iloc[i],
                    wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                    y=(fwd.iloc[i] - drift[coin]), ys=(fwd.iloc[i] - drift[coin]) / usual[coin]))
    g = pd.DataFrame(rows).dropna(subset=["y"])
    out["n_cases"] = len(g)

    def slope(df, x, y="ys"):
        d = df[[x, y]].dropna()
        if len(d) < 30:
            return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        r = stats.linregress(d[x], d[y])
        return pd.Series(dict(n=len(d), slope=r.slope, t=r.slope / r.stderr))

    # forecast quintiles
    g["fq"] = pd.qcut(g["f"], 5, labels=False, duplicates="drop")
    out["fq"] = g.groupby("fq").agg(n=("y", "size"), fmean=("f", "mean"), y=("y", "mean"), ys=("ys", "mean"),
                                    t=("y", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    # components separately and jointly
    comp = {}
    for x in ["f", "mom", "hi", "ret28", "dist", "r1z", "r5p", "volr"]:
        comp[x] = slope(g, x)
    out["slopes_all"] = pd.DataFrame(comp).T
    # joint regression mom + hi
    d = g[["mom", "hi", "ys"]].dropna()
    X = np.column_stack([np.ones(len(d)), d["mom"], d["hi"]])
    beta, *_ = np.linalg.lstsq(X, d["ys"].values, rcond=None)
    res = d["ys"].values - X @ beta
    s2 = res @ res / (len(d) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint_mom_hi"] = pd.DataFrame(dict(beta=beta, t=beta / se), index=["c", "mom", "hi"])
    # long vs short side
    g["side"] = np.sign(g["f"])
    out["side"] = g.groupby("side").agg(n=("y", "size"), y=("y", "mean"),
                                        t=("y", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    # by vol tercile: mean and idea slope
    g["vt"] = pd.cut(g["volr"], [0, 1/3, 2/3, 1.0001], labels=["lo", "mid", "hi"])
    out["by_vol"] = pd.concat([g.groupby("vt")["y"].agg(["size", "mean"]),
                               g.groupby("vt").apply(lambda df: slope(df, "f"))], axis=1)
    # after large past 5-day moves (standardised)
    g["r5q"] = pd.qcut(g["r5p"], 5, labels=False, duplicates="drop")
    out["by_past5"] = g.groupby("r5q").agg(n=("y", "size"), r5=("r5p", "mean"), y=("y", "mean"),
                                           t=("y", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    # forecast slope by year and by coin
    out["slope_by_year"] = g.groupby("yr").apply(lambda df: slope(df, "f"))
    out["slope_by_coin"] = g.groupby("coin").apply(lambda df: slope(df, "f"))
    # daily weekday effect on coin returns
    dd = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            t = dy.copy(); t["coin"] = coin; t["win"] = w
            dd.append(t)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["weekday_coin"] = D.groupby("wd")["coin_return"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    out["weekday_book"] = D.groupby("wd")["book_return"].agg(["mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # book: per-coin Sharpe and per-window-ish summary
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                bsd=("book_return", "std"))
    # trades by side
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    out["trades_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
                                               net=("net_profit_loss_percent", "mean"),
                                               gross=("profit_loss_percent", "mean"),
                                               dur_days=("duration_minutes", lambda s: s.mean() / 1440))
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            dlt = c.diff()
            up = dlt.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-dlt.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100 / (1 + up / dn)
            dd60 = c / c.rolling(60, min_periods=30).max() - 1
            ret30 = c / c.shift(30) - 1
            ret14 = c / c.shift(14) - 1
            vol20 = c.pct_change().rolling(20).std()
            age = -b["debug_info.components.below_age.last_history_value"]
            fwd14 = c.shift(-14) / c - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            df = pd.DataFrame({"coin": coin, "w": w, "rsi": rsi, "dd60": dd60, "ret30": ret30, "ret14": ret14,
                               "vol20": vol20, "age": age, "fwd14": fwd14, "pos": pos,
                               "i": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows)
    grid = d[d["i"] % 14 == 0].copy()
    grid["ex"] = grid["fwd14"] - grid["coin"].map(grid.groupby("coin")["fwd14"].mean())
    g = grid[grid["age"] > 0].dropna(subset=["ex", "rsi", "dd60", "ret30", "vol20", "age"])
    res = {}
    for k in ["age", "rsi", "dd60", "ret30", "ret14", "vol20"]:
        s = g.dropna(subset=[k])
        sl = stats.linregress(s[k], s["ex"])
        res[k] = {"n": len(s), "slope": sl.slope, "t": sl.slope / sl.stderr, "r": sl.rvalue}
    out["grid_below_univariate"] = pd.DataFrame(res).T
    for k in ["dd60", "ret30", "vol20", "rsi"]:
        q = pd.qcut(g[k], 3, labels=["q1", "q2", "q3"])
        out["grid_below_by_" + k] = g.groupby(q).agg(n=("ex", "size"), ex=("ex", "mean"),
                                                   t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # age effect split by drawdown depth
    g["ddb"] = np.where(g["dd60"] < g["dd60"].median(), "deep", "shallow")
    res = {}
    for k, s in g.groupby("ddb"):
        sl = stats.linregress(s["age"], s["ex"])
        res[k] = {"n": len(s), "mean_ex": s["ex"].mean(), "slope": sl.slope, "t": sl.slope / sl.stderr}
    out["age_slope_by_dd"] = pd.DataFrame(res)
    # book daily
    dr = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dr.append(dd.assign(coin=coin, w=w, year=pd.to_datetime(dd["day"]).dt.year))
    D = pd.concat(dr)
    out["book_daily_by_coin"] = D.groupby("coin").agg(mean=("book_return", "mean"), sd=("book_return", "std"),
                                                   hold=("coin_return", "mean"))
    out["book_daily_by_year"] = D.groupby("year").agg(mean=("book_return", "mean"), hold=("coin_return", "mean"))
    # worst 20 book days: coin state
    m = D.dropna(subset=["book_return"]).nsmallest(30, "book_return")
    out["worst30_days"] = pd.Series({"mean_book": m["book_return"].mean(), "mean_coin": m["coin_return"].mean(),
                                     "share_of_total_loss": m["book_return"].sum() / D["book_return"].sum()})
    return out

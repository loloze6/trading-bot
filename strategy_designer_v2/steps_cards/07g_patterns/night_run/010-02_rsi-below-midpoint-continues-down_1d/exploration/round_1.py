def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    raw_col = "debug_info.components.rsi_below_share.last_history_value"
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            ret7p = c / c.shift(7) - 1
            ret3p = c / c.shift(3) - 1
            ret1p = r1
            ret30p = c / c.shift(30) - 1
            f7 = c.shift(-7) / c - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n, 7):
                rows.append(dict(coin=coin, win=w, pos=i, f7=f7.iloc[i], raw=b[raw_col].iloc[i] if raw_col in b else np.nan,
                                 fc=b["forecast"].iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i],
                                 p7=ret7p.iloc[i], p30=ret30p.iloc[i], p1=ret1p.iloc[i], vol=vol20.iloc[i],
                                 wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year, grid=7))
    df = pd.DataFrame(rows).dropna(subset=["f7"])
    df["ex7"] = df["f7"] - df.groupby("coin")["f7"].transform("mean")
    out["n_cases"] = len(df)
    df["rawq"] = df["raw"].round(3)
    out["ex7_by_raw_share"] = df.groupby(pd.cut(df["raw"], [-0.51, -0.3, -0.1, 0.1, 0.3, 0.51])).ex7.agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    def tq(g, col, q=5):
        d = g.dropna(subset=[col, "ex7"])
        d = d.assign(b=pd.qcut(d[col], q, labels=False, duplicates="drop"))
        return d.groupby("b").agg(mean_ex7=("ex7", "mean"), n=("ex7", "size"), lo=(col, "min"), hi=(col, "max"))
    out["ex7_by_past7_quint"] = tq(df, "p7")
    out["ex7_by_past30_quint"] = tq(df, "p30")
    out["ex7_by_vol_quint"] = tq(df, "vol")
    out["ex7_by_coin_raw_corr"] = df.groupby("coin").apply(lambda g: pd.Series(dict(
        corr_raw=g[["raw", "ex7"]].corr().iloc[0, 1], corr_p7=g[["p7", "ex7"]].corr().iloc[0, 1],
        corr_p30=g[["p30", "ex7"]].corr().iloc[0, 1], n=len(g))))
    # slopes with t
    res = {}
    for col in ["raw", "p7", "p30", "fc"]:
        d = df.dropna(subset=[col, "ex7"])
        s = stats.linregress(d[col], d["ex7"])
        res[col] = [s.slope, s.slope / s.stderr, len(d)]
    out["slopes_t"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # interaction: raw within vol tercile
    d = df.dropna(subset=["raw", "vol"]).copy()
    d["vt"] = pd.qcut(d["vol"], 3, labels=["lowvol", "mid", "hivol"])
    out["raw_slope_by_vol"] = d.groupby("vt").apply(lambda g: pd.Series(dict(
        t=stats.linregress(g["raw"], g["ex7"]).slope / stats.linregress(g["raw"], g["ex7"]).stderr, n=len(g))))
    # daily-level: book and coin
    dd = []
    for coin, wins in data["days"].items():
        for w, g in wins.items():
            g = g.copy(); g["coin"] = coin; g["win"] = w
            g["wd"] = pd.to_datetime(g["day"]).dt.weekday
            g["yr"] = pd.to_datetime(g["day"]).dt.year
            g["prev"] = g["coin_return"].shift(1)
            g["next"] = g["coin_return"].shift(-1)
            dd.append(g)
    dd = pd.concat(dd)
    out["coin_ret_by_weekday"] = dd.groupby("wd").coin_return.agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["book_by_weekday"] = dd.groupby("wd").book_return.agg(["mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["book_by_year"] = dd.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    x = dd.dropna(subset=["prev", "coin_return"]).copy()
    x["pq"] = pd.qcut(x["prev"], 10, labels=False)
    out["next_day_by_prevday_decile"] = x.groupby("pq").coin_return.agg(["mean", "count"])
    return out

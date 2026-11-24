def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for coin, wd in bars.items():
        for w, df in wd.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            raw = df.get("debug_info.components.low_prox.last_history_value")
            raw = raw.astype(float).values if raw is not None else np.full(n, np.nan)
            fc = df["forecast"].astype(float).values
            lr = np.log(c)
            r1 = np.r_[np.nan, np.diff(lr)]
            s = pd.Series(r1)
            vol20 = s.rolling(20, min_periods=15).std().values
            ret20p = np.r_[np.full(20, np.nan), c[20:] / c[:-20] - 1] if n > 20 else np.full(n, np.nan)
            ret5p = np.r_[np.full(5, np.nan), c[5:] / c[:-5] - 1] if n > 5 else np.full(n, np.nan)
            low20 = pd.Series(c).rolling(20, min_periods=20).min().shift(1).values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 20):
                if i + 20 >= n: break
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), wd=ts.iloc[i].dayofweek,
                                 year=ts.iloc[i].year, raw=raw[i], fc=fc[i], vol20=vol20[i],
                                 r1=r1[i], z1=r1[i] / vol20[i] if vol20[i] > 0 else np.nan,
                                 p20=ret20p[i], p5=ret5p[i],
                                 brk20=(c[i] / low20[i] - 1) if low20[i] == low20[i] else np.nan,
                                 f20=c[i + 20] / c[i] - 1, f5=c[i + 5] / c[i] - 1 if i + 5 < n else np.nan))
    g = pd.DataFrame(rows)
    g["ex20"] = g["f20"] - g.groupby("coin")["f20"].transform("mean")
    g["ex5"] = g["f5"] - g.groupby("coin")["f5"].transform("mean")
    out["n_grid"] = len(g)
    out["raw_describe"] = g["raw"].describe()

    def qtab(col, target="ex20", q=5):
        d = g.dropna(subset=[col, target]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        t = d.groupby("q").agg(n=(target, "size"), mean=(target, "mean"), sd=(target, "std"),
                               xmin=(col, "min"), xmax=(col, "max"))
        t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")

    out["ex20_by_raw_prox_q"] = qtab("raw")
    out["ex20_by_forecast_q"] = qtab("fc")
    out["ex20_by_past20_q"] = qtab("p20")
    out["ex20_by_past5_q"] = qtab("p5")
    out["ex20_by_vol20_q"] = qtab("vol20")
    out["ex20_by_z1_q"] = qtab("z1")
    out["ex5_by_z1_q"] = qtab("z1", "ex5")
    out["ex20_by_break20low_q"] = qtab("brk20")
    out["ex20_by_year"] = g.groupby("year")["ex20"].agg(["size", "mean"])
    # very near low: raw >= 0.95
    near = g[g["raw"] >= 0.95]
    out["near_low_raw95"] = pd.Series({"n": len(near), "mean_ex20": near["ex20"].mean(),
                                       "t": stats.ttest_1samp(near["ex20"].dropna(), 0).statistic if len(near) > 2 else np.nan})
    # spearman, date-pooled
    for col in ["raw", "p20", "p5", "vol20", "z1", "brk20"]:
        d = g.dropna(subset=[col, "ex20"])
        dd = d.groupby("day")[[col, "ex20"]].mean()
        out["spearman_daypooled_" + col] = pd.Series({"rho": stats.spearmanr(dd[col], dd["ex20"]).correlation,
                                                       "ndays": len(dd)})
    # weekday of daily returns (all bars)
    dr = []
    for coin, wd in data["days"].items():
        for w, df in wd.items():
            x = df[["day", "coin_return", "book_return"]].copy()
            x["coin"] = coin; x["w"] = w
            dr.append(x)
    D = pd.concat(dr)
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.dayofweek
    t = D.groupby("wd")["coin_return"].agg(["size", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["size"]))
    out["coin_ret_by_weekday"] = t
    # book by window
    bk = D.groupby("day")["book_return"].mean()
    out["book_daily_mean_std"] = pd.Series({"mean": bk.mean(), "std": bk.std(), "n": len(bk)})
    D["year"] = D["day"].dt.year
    out["book_by_year"] = D.groupby(["year", "day"])["book_return"].mean().groupby("year").agg(["size", "mean"])
    return out

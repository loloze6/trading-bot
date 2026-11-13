def explore(data):
    import pandas as pd, numpy as np
    H = 20
    rows = []
    for coin, wins in data["bars"].items():
        dr = pd.concat([d["coin_return"] for d in data["days"][coin].values()]).dropna()
        mu = dr.mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            f = b["forecast"].astype(float)
            dist = b["debug_info.components.above_ma.last_history_value"].astype(float)
            fwd = c.shift(-H) / c - 1
            exc = fwd - H * mu
            above = (dist > 0).astype(int)
            grp = (above != above.shift()).cumsum()
            age = above.groupby(grp).cumcount() + 1
            sma = c / (1 + dist / 100)
            slope = sma / sma.shift(20) - 1
            mom20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "f": f, "dist": dist,
                                      "exc": exc, "above": above, "age": age, "slope": slope,
                                      "mom20": mom20, "i": np.arange(len(b)), "n": len(b)}))
    d = pd.concat(rows).dropna(subset=["exc"])
    s = d[d["i"] % H == 0]
    def st(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(),
                          "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean(), "std": x.std()})
    out = {}
    out["bars_per_window"] = d.groupby(["coin", "w"])["n"].first().describe()
    a = s[s["f"] > 0].copy()
    out["active_overall"] = st(a["exc"])
    out["active_trim_top5pct"] = st(a["exc"][a["exc"] < a["exc"].quantile(0.95)])
    out["active_skew"] = pd.Series({"skew": a["exc"].skew(), "share_of_sum_top10": a["exc"].nlargest(10).sum() / a["exc"].sum()})
    a["sl"] = np.where(a["slope"] > 0, "up", "down_or_na")
    a["fb"] = np.where(a["f"] > 10, "f>10", "f<=10")
    out["slope_x_f"] = a.groupby(["sl", "fb"])["exc"].apply(st).unstack()
    a["slq"] = pd.qcut(a["slope"], 4, duplicates="drop")
    out["by_slope_q"] = a.groupby("slq")["exc"].apply(st).unstack()
    up = a[a["slope"] > 0]
    out["slope_up_by_coin"] = up.groupby("coin")["exc"].apply(st).unstack()
    out["slope_up_by_year"] = up.groupby("year")["exc"].apply(st).unstack()
    out["slope_up_f10_by_year"] = up[up["f"] > 10].groupby("year")["exc"].apply(st).unstack()
    out["by_rawdist_q"] = a.groupby(pd.qcut(a["dist"], 4))["exc"].apply(st).unstack()
    out["mom_x_slope"] = a.groupby([np.where(a["mom20"] > 0.0663, "mom_hi", "mom_lo"), "sl"])["exc"].apply(st).unstack()
    return out

def explore(data):
    import pandas as pd, numpy as np
    H = 20
    rows = []
    for coin, wins in data["bars"].items():
        # pooled mean daily return
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
            # bars since last upward cross (within window)
            grp = (above != above.shift()).cumsum()
            age = above.groupby(grp).cumcount() + 1
            sma = c / (1 + dist) if dist.abs().max() < 5 else c / (1 + dist / 100)
            slope = sma / sma.shift(20) - 1
            mom20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "f": f, "dist": dist,
                               "exc": exc, "fwd": fwd, "above": above, "age": age,
                               "slope": slope, "mom20": mom20, "i": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["exc"])
    d["sub"] = (d["i"] % H == 0)
    s = d[d["sub"]]
    def st(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan, "hit": (x > 0).mean()})
    out = {}
    out["dist_scale"] = pd.Series({"dist_median_abs": d["dist"].abs().median(), "dist_max": d["dist"].max()})
    out["by_above"] = s.groupby("above")["exc"].apply(st).unstack()
    a = s[s["f"] > 0].copy()
    out["active_by_coin"] = a.groupby("coin")["exc"].apply(st).unstack()
    out["active_by_year"] = a.groupby("year")["exc"].apply(st).unstack()
    out["active_by_fbucket"] = a.groupby(pd.cut(a["f"], [0, 5, 10, 15, 20.01]))["exc"].apply(st).unstack()
    out["active_by_age"] = a.groupby(pd.cut(a["age"], [0, 20, 60, 150, 10000]))["exc"].apply(st).unstack()
    out["above_by_age_all"] = s[s["above"] == 1].groupby(pd.cut(s.loc[s["above"] == 1, "age"], [0, 20, 60, 150, 10000]))["exc"].apply(st).unstack()
    out["above_by_slope_sign"] = s[s["above"] == 1].groupby(np.sign(s.loc[s["above"] == 1, "slope"]))["exc"].apply(st).unstack()
    out["above_by_mom20_q"] = s[s["above"] == 1].groupby(pd.qcut(s.loc[s["above"] == 1, "mom20"], 4))["exc"].apply(st).unstack()
    out["active_weighted_by_coin"] = a.assign(we=a["f"] * a["exc"]).groupby("coin")["we"].apply(st).unstack()
    out["active_by_window_mean"] = a.groupby("w")["exc"].mean().describe()
    return out

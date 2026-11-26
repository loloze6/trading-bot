def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            hi14 = c.rolling(14, min_periods=10).max()
            depth = (c - hi14) / hi14 / vol30
            ret1s = r1 / vol30
            tr60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "depth": depth, "ret1s": ret1s, "tr60": tr60, "fwd": fwd, "fwd1": fwd1,
                "calm": (b["regime"] == "unknown"), "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "gain": b["postRebalance_current_allocation"] * fwd1, "year": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean(); usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift); g["exs"] = g["ex"] / g["coin"].map(usual)
    g["trend"] = np.where(g["tr60"] > 0.1, "rising", np.where(g["tr60"] < -0.1, "falling", np.where(g["tr60"].notna(), "choppy", "na")))
    c = g[g.calm].dropna(subset=["depth"])
    out = {}
    def sl(d, x):
        d = d.dropna(subset=[x, "exs"])
        if len(d) < 25: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d[x], d["exs"])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr, "ex": d["ex"].mean()})
    out["calm_depth_by_year"] = c.groupby("year").apply(lambda d: sl(d, "depth")).round(4)
    out["calm_depth_by_coin"] = c.groupby("coin").apply(lambda d: sl(d, "depth")).round(4)
    out["calm_ret1s_by_year"] = c.groupby("year").apply(lambda d: sl(d, "ret1s")).round(4)
    out["calm_fc_vs_depth"] = pd.Series({"corr_fc_depth": c[["fc", "depth"]].corr().iloc[0, 1],
        "slope_t_fc": sl(c, "fc")["t"], "slope_t_depth": sl(c, "depth")["t"]}).round(4)
    fc_ = c[c.trend == "falling"].copy()
    fc_["q"] = pd.qcut(fc_["depth"].rank(method="first"), 3, labels=False)
    t = fc_.groupby("q").agg(n=("ex", "size"), depth=("depth", "mean"), ex=("ex", "mean"))
    t["t"] = fc_.groupby("q")["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["falling_calm_depth_terciles"] = t.round(4)
    out["falling_calm_by_year"] = fc_.groupby("year").apply(lambda d: sl(d, "depth")).round(4)
    # day-level t for depth slope in calm: residual sum per day
    a = A.dropna(subset=["gain"])
    a["trend"] = np.where(a["tr60"] > 0.1, "rising", np.where(a["tr60"] < -0.1, "falling", "choppy"))
    bp = a[a.alloc != 0].groupby("trend").agg(n=("gain", "size"), gain=("gain", "mean"), alloc=("alloc", "mean"))
    out["book_by_trend_inpos"] = bp.round(5)
    return out

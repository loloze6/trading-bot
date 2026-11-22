import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(r1).fillna(0)
            grp = (sgn != sgn.shift()).cumsum()
            run = sgn.groupby(grp).cumcount() + 1
            run = run * sgn
            raw = b.get("debug_info.components.rise30d.last_history_value")
            r30 = c / c.shift(180) - 1
            if raw is not None:
                r30 = r30.fillna(pd.to_numeric(raw, errors="coerce"))
            vol30 = r1.rolling(180, min_periods=60).std()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "fwd": c.shift(-H) / c - 1,
                "fwd1": r1.shift(-1),
                "r30": r30,
                "r30z": r30 / (vol30 * np.sqrt(180)),
                "r7": c / c.shift(42) - 1,
                "r1d": c / c.shift(6) - 1,
                "r1dz": (c / c.shift(6) - 1) / (vol30 * np.sqrt(6)),
                "r7z": (c / c.shift(42) - 1) / (vol30 * np.sqrt(42)),
                "run": run,
                "vratio": v.rolling(6).mean() / v.rolling(60).mean(),
                "vol30": vol30,
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            hourly.append(df[["coin","hour","wd","fwd1","alloc"]])
            rows.append(df.iloc[::H])
    g = pd.concat(rows, ignore_index=True)
    g = g.dropna(subset=["fwd"])
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["usual"] = g.groupby("coin")["fwd"].transform("std")
    out = {}
    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["rk"] = d.groupby("coin")[col].rank(pct=True)
        d["bin"] = np.minimum((d["rk"] * q).astype(int), q - 1)
        t = d.groupby("bin")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["feat_mean"] = d.groupby("bin")[col].mean()
        sl = stats.linregress(d["rk"], d["ex"])
        t["slope_rank_t"] = sl.slope / sl.stderr
        return t.round(5)
    for col in ["r30", "r30z", "r7", "r7z", "r1d", "r1dz", "run", "vratio", "vol30"]:
        out["ex_by_" + col] = tab(col)
    # r30 negative side only: continuation down?
    neg = g[(g["r30"] < 0)].dropna(subset=["r30"])
    sl = stats.linregress(neg["r30"], neg["ex"])
    out["neg_r30_slope"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(neg)} mean_ex {neg['ex'].mean():.4f}"
    # r1dz inside strong r30 (pullback in uptrend)
    up = g[g["r30"] > 0].dropna(subset=["r1dz"])
    sl = stats.linregress(up["r1dz"], up["ex"])
    out["r1dz_slope_in_r30pos"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(up)}"
    dn = g[g["r30"] < 0].dropna(subset=["r1dz"])
    sl = stats.linregress(dn["r1dz"], dn["ex"])
    out["r1dz_slope_in_r30neg"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(dn)}"
    # by coin and year for r30 slope
    def slope_t(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 30: return np.nan
        s = stats.linregress(d[x], d["ex"]); return s.slope / s.stderr
    out["r30z_slope_t_by_coin"] = g.groupby("coin").apply(lambda d: pd.Series({"r30z_t": slope_t(d, "r30z"), "r30_t": slope_t(d, "r30"), "r7z_t": slope_t(d,"r7z"), "r1dz_t": slope_t(d,"r1dz"), "n": len(d)}))
    out["r30z_slope_t_by_year"] = g.groupby("year").apply(lambda d: pd.Series({"r30z_t": slope_t(d, "r30z"), "r1dz_t": slope_t(d,"r1dz"), "n": len(d)}))
    # hours/weekday on 1-bar returns
    hb = pd.concat(hourly).dropna(subset=["fwd1"])
    hb["ex1"] = hb["fwd1"] - hb.groupby("coin")["fwd1"].transform("mean")
    def agg(d):
        return pd.Series({"mean": d.mean(), "n": len(d), "t": d.mean() / (d.std() / np.sqrt(len(d)))})
    out["ex1_by_hour_of_next_bar_start"] = hb.groupby("hour")["ex1"].apply(agg).unstack().round(6)
    out["ex1_by_weekday"] = hb.groupby("wd")["ex1"].apply(agg).unstack().round(6)
    # book: market vs timing
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    D["cm"] = D.groupby("coin")["coin_return"].transform("mean")
    D["beta_dd"] = D["book_return"]
    q = D["book_return"].quantile([0.02, 0.98])
    out["book_extreme_days"] = pd.DataFrame({
        "top2pct_coin_ret": [D[D.book_return >= q.iloc[1]]["coin_return"].mean()],
        "bot2pct_coin_ret": [D[D.book_return <= q.iloc[0]]["coin_return"].mean()],
        "share_gain_top2pct": [D[D.book_return >= q.iloc[1]]["book_return"].sum() / D["book_return"].sum()],
        "corr_book_coin": [D["book_return"].corr(D["coin_return"])],
    })
    return out

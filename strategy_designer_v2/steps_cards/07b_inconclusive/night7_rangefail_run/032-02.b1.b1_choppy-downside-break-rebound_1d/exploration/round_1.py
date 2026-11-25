def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    coin_mean = {}
    for coin, wd in bars.items():
        rs = []
        for w, df in wd.items():
            c = df["close"].values
            rs.append(pd.Series(c[1:]/c[:-1]-1))
        coin_mean[coin] = pd.concat(rs).mean() if rs else np.nan
    for coin, wd in bars.items():
        for w, df in wd.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            r = pd.Series(c).pct_change()
            vol30 = r.rolling(30).std()
            ret60 = pd.Series(c)/pd.Series(c).shift(60)-1
            for i in np.where(df["regime"].values == "mean_reversion")[0]:
                d = {"coin": coin, "window": w, "year": ts[i].year, "day": ts[i].normalize(),
                     "depth": -df["debug_info.components.depth.last_history_value"].iloc[i],
                     "ret60": ret60.iloc[i], "vol30": vol30.iloc[i],
                     "r0": r.iloc[i]}
                for h in [1, 2, 3, 5, 10]:
                    d[f"x{h}"] = (c[i+h]/c[i]-1 - h*coin_mean[coin]) if i+h < n else np.nan
                rows.append(d)
    t = pd.DataFrame(rows)
    out = {}
    def summ(g, col="x1"):
        s = g.groupby("day")[col].sum()
        return pd.Series({"cases": g[col].notna().sum(), "days": s.size, "mean_case": g[col].mean(),
                          "median_case": g[col].median(), "share_pos": (g[col] > 0).mean(),
                          "t_day": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["horizons"] = pd.DataFrame({h: summ(t, f"x{h}") for h in ["x1", "x2", "x3", "x5", "x10"]}).T
    out["by_coin"] = t.groupby("coin").apply(summ)
    out["by_window"] = t.groupby("window").apply(summ)
    out["by_year"] = t.groupby("year").apply(summ)
    t["dq"] = pd.qcut(t["depth"], 3, labels=["shallow", "mid", "deep"])
    out["by_depth"] = t.groupby("dq").apply(summ)
    out["depth_q_x3"] = t.groupby("dq").apply(lambda g: summ(g, "x3"))
    t["volq"] = pd.qcut(t["vol30"], 2, labels=["lowvol", "highvol"])
    out["by_vol"] = t.groupby("volq").apply(summ)
    t["r0q"] = pd.qcut(t["r0"], 3, labels=["r0_low", "r0_mid", "r0_high"])
    out["by_dayret"] = t.groupby("r0q").apply(summ)
    out["trim_top5"] = summ(t[t["x1"] < t["x1"].quantile(0.95)])
    out["depth_stats"] = t["depth"].describe()
    return out

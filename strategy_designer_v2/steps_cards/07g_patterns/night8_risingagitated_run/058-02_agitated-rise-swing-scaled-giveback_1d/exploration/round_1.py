def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = 5
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            stretch = (c / sma - 1) / sd
            ret60 = c / c.shift(60) - 1
            r1 = r
            r5past = c / c.shift(5) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), H):
                rows.append(dict(coin=coin, w=w, i=i, stretch=stretch.iloc[i], ret60=ret60.iloc[i],
                                 r1=r1.iloc[i], r5p=r5past.iloc[i], sd=sd.iloc[i], fwd=fwd.iloc[i],
                                 regime=df["regime"].iloc[i], wd=ts.iloc[i].dayofweek,
                                 year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].transform("mean")
    usual = g.groupby("coin")["fwd"].transform("std")
    g["ex"] = g["fwd"] - drift
    g["exn"] = g["ex"] / usual
    g["ra"] = np.where(g["regime"] == "unknown", "rising_agit", "other")
    g["trend"] = np.where(g["ret60"] > 0.10, "rising", np.where(g["ret60"] < -0.10, "falling", np.where(g["ret60"].isna(), "na", "choppy")))
    g["prof"] = np.where(g["ra"] == "rising_agit", "rising_agit", g["trend"] + "_notRA")
    def summ(x):
        n = len(x)
        m = x["ex"].mean(); s = x["ex"].std()
        return pd.Series(dict(n=n, mean_ex=m, t=m / (s / np.sqrt(n)) if n > 2 else np.nan, strength=x["exn"].mean()))
    out = {}
    gg = g.dropna(subset=["stretch"]).copy()
    gg["sq"] = pd.qcut(gg["stretch"], 5, labels=False)
    out["stretch_quintile_by_prof"] = gg.groupby(["prof", "sq"]).apply(summ)
    def slope(x):
        if len(x) < 20: return pd.Series(dict(n=len(x), corr=np.nan, t=np.nan))
        rr = stats.pearsonr(x["stretch"], x["exn"])
        n = len(x); t = rr[0] * np.sqrt((n - 2) / (1 - rr[0] ** 2))
        return pd.Series(dict(n=n, corr=rr[0], t=t))
    out["stretch_slope_by_prof"] = gg.groupby("prof").apply(slope)
    gg2 = g.dropna(subset=["r5p"]).copy()
    gg2["pz"] = gg2["r5p"] / (gg2["sd"] * np.sqrt(5))
    gg2["pq"] = pd.qcut(gg2["pz"], 5, labels=False)
    out["past5_quintile_by_prof"] = gg2.groupby(["prof", "pq"]).apply(summ)
    out["weekday"] = g.groupby("wd").apply(summ)
    out["year_prof_counts"] = g.groupby(["year", "prof"]).size().unstack()
    # book
    d = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d.append(df.assign(coin=coin, w=w))
    D = pd.concat(d)
    out["book_by_window"] = D.groupby("w")[["book_return", "coin_return"]].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=coin, w=w))
    T = pd.concat(tr)
    T["ef"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades_by_entry_forecast"] = T.groupby(["side", "ef"])["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out

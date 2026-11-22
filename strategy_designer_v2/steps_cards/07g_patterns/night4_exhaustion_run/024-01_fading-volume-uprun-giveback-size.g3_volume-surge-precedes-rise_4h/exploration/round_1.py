def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            fwd = c.shift(-H) / c - 1
            past = c / c.shift(H) - 1
            past6 = c / c.shift(36) - 1
            r1 = c.pct_change()
            vr = v / v.rolling(180, min_periods=45).mean()
            vtrend = v.rolling(6).mean() / v.rolling(18).mean()  # volume of last day vs last 3 days
            sgn = np.sign(r1)
            # run length of consecutive same-sign bars
            run = sgn.groupby((sgn != sgn.shift()).cumsum()).cumcount() + 1
            run = run * sgn
            vol = r1.rolling(180, min_periods=45).std()
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.iloc[idx].values, "past": past.iloc[idx].values,
                "past6": past6.iloc[idx].values, "vr": vr.iloc[idx].values, "vtrend": vtrend.iloc[idx].values,
                "run": run.iloc[idx].values, "vol": vol.iloc[idx].values,
                "fc": b["forecast"].iloc[idx].values, "pos": b["postRebalance_current_allocation"].iloc[idx].values,
                "hour": ts.iloc[idx].dt.hour.values, "wd": ts.iloc[idx].dt.weekday.values,
                "year": ts.iloc[idx].dt.year.values})
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd"])
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    sd = D.groupby("coin")["fwd"].transform("std")
    D["z"] = D["ex"] / sd
    D["pastz"] = D["past"] / sd
    D["past6z"] = D["past6"] / (sd * np.sqrt(2))
    def tab(g):
        return g["z"].agg(n="count", mean="mean", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out = {}
    out["by_past3d_quintile"] = D.dropna(subset=["pastz"]).groupby(pd.qcut(D["pastz"], 5, labels=False)).apply(tab)
    out["by_past6d_quintile"] = D.dropna(subset=["past6z"]).groupby(pd.qcut(D["past6z"], 5, labels=False)).apply(tab)
    out["by_vr_quintile"] = D.dropna(subset=["vr"]).groupby(pd.qcut(D["vr"], 5, labels=False)).apply(tab)
    out["by_vol_quintile"] = D.dropna(subset=["vol"]).groupby(D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 5, labels=False))).apply(tab)
    E = D.dropna(subset=["pastz", "vtrend"]).copy()
    E["pq"] = pd.qcut(E["pastz"], 3, labels=["down", "mid", "up"])
    E["vq"] = pd.qcut(E["vtrend"], 3, labels=["fade", "mid", "rise"])
    out["past_x_voltrend"] = E.groupby(["pq", "vq"]).apply(tab)
    out["by_runlen"] = D.groupby(D["run"].clip(-5, 5)).apply(tab)
    out["by_hour"] = D.groupby("hour").apply(tab)
    out["by_weekday"] = D.groupby("wd").apply(tab)
    out["by_year"] = D.groupby("year").apply(tab)
    out["by_coin"] = D.groupby("coin").apply(tab)
    out["by_forecast_band"] = D.groupby(pd.cut(D["fc"], [-0.1, 0.01, 2, 8, 20.1])).apply(tab)
    out["spearman_pastz_z"] = stats.spearmanr(E["pastz"], E["z"])[0]
    # book days: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    q = DD["book_return"].quantile([0.01, 0.99])
    DD["bucket"] = np.where(DD["book_return"] <= q.iloc[0], "worst1%", np.where(DD["book_return"] >= q.iloc[1], "best1%", "other"))
    out["book_tails"] = DD.groupby("bucket").agg(n=("book_return", "count"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out

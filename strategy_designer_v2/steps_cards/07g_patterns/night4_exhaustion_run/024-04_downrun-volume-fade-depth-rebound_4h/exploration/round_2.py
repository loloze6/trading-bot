def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    hb = []; rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values; v = df["volume"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]  # return of bar i itself (its own start hour)
            vol30 = pd.Series(r).rolling(180, min_periods=60).std().values
            vrel = pd.Series(v).rolling(6).sum().values / pd.Series(v).rolling(180, min_periods=60).sum().values * 30
            ret18 = pd.Series(c).pct_change(18).values
            ret6 = pd.Series(c).pct_change(6).values
            for i in range(1, n):
                hb.append((coin, w, ts.iloc[i].hour, ts.iloc[i].dayofweek, ts.iloc[i].year, r[i], r[i] / vol30[i] if vol30[i] else np.nan))
            for i in range(0, n - H, H):
                z18 = ret18[i] / (vol30[i] * np.sqrt(18)) if vol30[i] else np.nan
                z6 = ret6[i] / (vol30[i] * np.sqrt(6)) if vol30[i] else np.nan
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, fwd=c[i+H]/c[i]-1, vrel=vrel[i], z18=z18, z6=z6))
    h = pd.DataFrame(hb, columns=["coin", "w", "hour", "wd", "year", "r", "rz"]).dropna(subset=["r"])
    def tt(x):
        return pd.Series({"mean": x.mean(), "n": len(x), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out = {}
    out["own_hour_all"] = h.groupby("hour")["r"].apply(tt).unstack()
    h20 = h[h.hour == 20]; h0 = h[h.hour == 0]
    out["hour20_by_coin"] = h20.groupby("coin")["r"].apply(tt).unstack()
    out["hour20_by_year"] = h20.groupby("year")["r"].apply(tt).unstack()
    out["hour0_by_coin"] = h0.groupby("coin")["r"].apply(tt).unstack()
    out["hour20_minus_other_by_coin_welch"] = h.groupby("coin").apply(lambda x: pd.Series(dict(diff=x[x.hour == 20].r.mean() - x[x.hour != 20].r.mean(), t=stats.ttest_ind(x[x.hour == 20].r, x[x.hour != 20].r, equal_var=False).statistic)))
    # equal-weight cross-coin per timestamp to remove cross-coin dependence
    hh = h.copy(); hh["key"] = hh["w"] + "_" + hh.groupby(["coin", "w"]).cumcount().astype(str)
    out["own_wd_all"] = h.groupby("wd")["r"].apply(tt).unstack()
    out["wd_hour20"] = h20.groupby("wd")["r"].apply(tt).unstack()
    out["fri_by_coin"] = h[h.wd == 4].groupby("coin")["r"].apply(tt).unstack()
    out["fri_by_year"] = h[h.wd == 4].groupby("year")["r"].apply(tt).unstack()
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    for col in ["vrel", "z18"]:
        d = g.dropna(subset=[col])
        out["spearman_" + col + "_by_coin"] = d.groupby("coin").apply(lambda x: pd.Series(dict(rho=stats.spearmanr(x[col], x.ex).correlation, n=len(x))))
        out["spearman_" + col + "_by_year"] = d.groupby("year").apply(lambda x: stats.spearmanr(x[col], x.ex).correlation)
    d = g.dropna(subset=["vrel", "z6"])
    d["vq"] = d.groupby("coin")["vrel"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    d["mq"] = d.groupby("coin")["z6"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["ex_by_vrel_x_z6"] = d.pivot_table(index="vq", columns="mq", values="ex", aggfunc="mean")
    out["n_by_vrel_x_z6"] = d.pivot_table(index="vq", columns="mq", values="ex", aggfunc="count")
    return out

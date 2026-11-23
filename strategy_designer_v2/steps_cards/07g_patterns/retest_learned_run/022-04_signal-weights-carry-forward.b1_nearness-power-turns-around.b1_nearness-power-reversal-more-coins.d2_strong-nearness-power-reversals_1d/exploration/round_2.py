def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    res = {}
    # 1) daily coin returns by weekday, averaged across coins per day, t over days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.dayofweek
    D["year"] = D["day"].dt.year
    D["cdrift"] = D.groupby("coin")["coin_return"].transform("mean")
    D["cex"] = D["coin_return"] - D["cdrift"]
    per_day = D.groupby(["day", "wd", "year"])[["cex", "book_return"]].mean().reset_index()
    def tt(s):
        s = s.dropna()
        return pd.Series(dict(mean=s.mean(), n=len(s), t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan))
    res["coin_daily_ex_by_weekday_dayclustered"] = per_day.groupby("wd")["cex"].apply(tt).unstack().round(5)
    per_day["half"] = np.where(per_day["year"] <= 2021, "y2018_21", "y2022_25")
    x = per_day.groupby(["half", "wd"])["cex"].apply(tt).unstack()
    res["coin_daily_ex_by_weekday_half"] = x.round(5)
    # 2) 5-day forward excess by start weekday, every bar of that weekday (7 apart, no overlap), clustered by date
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            r1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(r1).rolling(20).std().values
            vz = (pd.Series(np.log(v + 1)) - pd.Series(np.log(v + 1)).rolling(30).mean()) / pd.Series(np.log(v + 1)).rolling(30).std()
            al = b["postRebalance_current_allocation"].astype(float).values
            for i in range(n - H):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year,
                                 fwd=c[i+H]/c[i]-1, r1z=r1[i]/vol20[i] if vol20[i] > 0 else np.nan,
                                 vz=vz.iloc[i], al=al[i], pos=i))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    pdd = g.groupby(["day", "wd"])["ex"].mean().reset_index()
    res["fwd5_ex_by_start_weekday_dayclustered"] = pdd.groupby("wd")["ex"].apply(tt).unstack().round(5)
    # 3) shock-size reversal: next-5d excess by |r1z| sign buckets, grid only, clustered by date
    gg = g[g["pos"] % H == 0].dropna(subset=["r1z"]).copy()
    gg["b"] = pd.cut(gg["r1z"], [-99, -2, -1, 0, 1, 2, 99])
    gb = gg.groupby(["day", "b"], observed=True)["ex"].mean().reset_index()
    res["fwd5_ex_by_r1z_bucket_dayclustered"] = gb.groupby("b", observed=True)["ex"].apply(tt).unstack().round(5)
    gg2 = gg.dropna(subset=["vz"]).copy()
    gg2["b"] = pd.cut(gg2["vz"], [-99, -1, 0, 1, 2, 99])
    gb = gg2.groupby(["day", "b"], observed=True)["ex"].mean().reset_index()
    res["fwd5_ex_by_volume_z_dayclustered"] = gb.groupby("b", observed=True)["ex"].apply(tt).unstack().round(5)
    # signed: return-direction x abnormal volume
    gg2["sgn_ex"] = np.sign(gg2["r1z"]) * gg2["ex"]
    gb = gg2.groupby(["day", "b"], observed=True)["sgn_ex"].mean().reset_index()
    res["fwd5_ex_in_day_direction_by_volume_z"] = gb.groupby("b", observed=True)["sgn_ex"].apply(tt).unstack().round(5)
    # 4) book: largest days, what preceded
    pdb = per_day.dropna(subset=["book_return"]).sort_values("book_return")
    k = max(1, int(len(pdb) * 0.05))
    res["book_worst5pct_vs_best5pct"] = pd.DataFrame({
        "worst_book": [pdb.head(k)["book_return"].mean()], "worst_coin_ex": [pdb.head(k)["cex"].mean()],
        "best_book": [pdb.tail(k)["book_return"].mean()], "best_coin_ex": [pdb.tail(k)["cex"].mean()], "k": [k]}).round(5)
    # position side share and gross gain by side
    g["nxt"] = g.groupby(["coin", "w"])["fwd"].shift(0)
    res["alloc_side_share"] = pd.Series(dict(long=(g["al"] > 0).mean(), short=(g["al"] < 0).mean(), flat=(g["al"] == 0).mean())).round(4)
    return res

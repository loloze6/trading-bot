def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt3 = c.shift(-3) / c - 1
            hi20 = c.rolling(20).max()
            sd20 = r.rolling(20).std()
            depth = (c - hi20) / hi20 / sd20
            ret60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            pos = np.arange(len(b))
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "dayid": ts.dt.floor("D").astype("int64"),
                "yr": ts.dt.year, "r": r, "nxt": nxt, "nxt3": nxt3, "grid3": pos % 3 == 0,
                "depth": depth, "ret60": ret60, "rz": r / sd20, "nbars": len(b),
                "alloc": b["postRebalance_current_allocation"].astype(float)}))
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    drift3 = d[d["grid3"]].groupby("coin")["nxt3"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["ex3"] = d["nxt3"] - d["coin"].map(drift3)
    res = {"bars_per_window": d.groupby("win")["nbars"].first().describe()}
    d = d.dropna(subset=["ex", "depth", "ret60"])
    d["trend"] = np.where(d["ret60"] > 0.10, "rising", np.where(d["ret60"] < -0.10, "falling", "choppy"))
    d["up"] = np.where(d["r"] > 0, "up", "down")

    def tday(s, dd):
        g = s.groupby(dd.loc[s.index, "dayid"]).sum()
        n = len(g)
        return (g.mean() / (g.std(ddof=1) / np.sqrt(n))) if n > 4 else np.nan

    ch = d[d["trend"] == "choppy"].copy()
    ch["dq5"] = pd.qcut(ch["depth"].rank(method="first"), 5, labels=False)
    out = []
    for k, g in ch.groupby("dq5"):
        out.append(dict(q=k, n=len(g), depth_mean=g["depth"].mean(), ex_pct=100*g["ex"].mean(), t=tday(g["ex"], d),
                        ex_up=100*g.loc[g.up=="up","ex"].mean(), ex_down=100*g.loc[g.up=="down","ex"].mean()))
    res["choppy_depth_quintiles"] = pd.DataFrame(out)
    # graded regression within choppy, all days: ex on depth
    sl = stats.linregress(ch["depth"], ch["ex"])
    res["choppy_slope_ex_on_depth"] = pd.Series(dict(slope_pct_per_unit=100*sl.slope, t=sl.slope/sl.stderr, n=len(ch)))
    # deepest tercile choppy (all days) by window, coin, year
    deep = ch[ch["dq5"] <= 1]
    res["choppy_deep40_by_win"] = deep.groupby("win")["ex"].agg(["count", "mean"])
    res["choppy_deep40_by_coin"] = deep.groupby("coin")["ex"].agg(["count", "mean"])
    res["choppy_deep40_by_year"] = deep.groupby("yr")["ex"].agg(["count", "mean"])
    # 3-day horizon on grid
    g3 = ch[ch["grid3"]].dropna(subset=["ex3"])
    sl3 = stats.linregress(g3["depth"], g3["ex3"])
    res["choppy_3d_slope"] = pd.Series(dict(slope_pct=100*sl3.slope, t=sl3.slope/sl3.stderr, n=len(g3)))
    # falling: up-day size graded
    fa = d[(d["trend"] == "falling")]
    s1 = stats.linregress(fa["rz"].clip(-4, 4), fa["ex"])
    res["falling_slope_ex_on_rz"] = pd.Series(dict(slope_pct=100*s1.slope, t=s1.slope/s1.stderr, n=len(fa)))
    sa = stats.linregress(d["depth"], d["ex"])
    res["all_slope_ex_on_depth"] = pd.Series(dict(slope_pct=100*sa.slope, t=sa.slope/sa.stderr, n=len(d)))
    # book: concentration of gains
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, win=w))
    bk = pd.concat(bk)
    br = bk.groupby(["win", "day"])["book_return"].mean().dropna()
    srt = br.sort_values()
    res["book_days"] = pd.Series(dict(n=len(br), mean=br.mean(), sum=br.sum(),
        top10_sum=srt.tail(10).sum(), bottom10_sum=srt.head(10).sum(), nonzero=(br.abs() > 1e-12).sum()))
    return res

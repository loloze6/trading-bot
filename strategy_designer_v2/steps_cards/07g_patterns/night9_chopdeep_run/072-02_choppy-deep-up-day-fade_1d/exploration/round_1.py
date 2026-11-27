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
            hi20 = c.rolling(20).max()
            sd20 = r.rolling(20).std()
            depth = (c - hi20) / hi20 / sd20
            lo20 = c.rolling(20).min()
            height = (c - lo20) / lo20 / sd20
            ret60 = c / c.shift(60) - 1
            sd30 = r.rolling(30).std()
            volpct = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ret5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "dayid": ts.dt.floor("D").astype("int64"),
                "wd": ts.dt.weekday, "r": r, "nxt": nxt, "depth": depth, "height": height,
                "ret60": ret60, "volpct": volpct, "rz": r / sd20, "ret5z": ret5 / (sd20 * np.sqrt(5)),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d = d.dropna(subset=["ex", "depth", "ret60"])
    d["trend"] = np.where(d["ret60"] > 0.10, "rising", np.where(d["ret60"] < -0.10, "falling", "choppy"))
    d["agit"] = np.where(d["volpct"] > 0.5, "agitated", "calm")
    d["up"] = np.where(d["r"] > 0, "up", "down")

    def tday(s):
        g = s.groupby(d.loc[s.index, "dayid"]).sum()
        n = len(g)
        if n < 5: return np.nan
        return g.mean() / (g.std(ddof=1) / np.sqrt(n))

    def summ(grp_cols, sub):
        out = []
        for k, g in sub.groupby(grp_cols):
            out.append(dict(key=str(k), n=len(g), mean_ex_pct=100 * g["ex"].mean(), t=tday(g["ex"])))
        return pd.DataFrame(out)

    # depth terciles within each trend x up/down
    d["dq"] = d.groupby(["trend", "up"])["depth"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=["deep", "mid", "shallow"]))
    res = {}
    res["by_trend_up_depthq"] = summ(["trend", "up", "dq"], d)
    # graded correlation depth vs ex by trend x agit
    out = []
    for k, g in d.groupby(["trend", "agit"]):
        rho, p = stats.spearmanr(g["depth"], g["ex"])
        out.append(dict(key=str(k), n=len(g), rho_depth=rho, p=p,
                        rho_rz=stats.spearmanr(g["rz"], g["ex"])[0],
                        rho_ret5z=stats.spearmanr(g["ret5z"], g["ex"])[0],
                        rho_height=stats.spearmanr(g["height"], g["ex"])[0]))
    res["rank_corr_by_profile"] = pd.DataFrame(out)
    # day move z quintiles by trend
    d["rzq"] = d.groupby("trend")["rz"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    res["by_trend_rzq"] = summ(["trend", "rzq"], d)
    res["by_weekday"] = summ(["wd"], d)
    res["by_profile"] = summ(["trend", "agit"], d)
    # book: positions
    pos = d[d["alloc"].abs() > 1e-9]
    res["book_pos_by_window"] = pos.assign(g=-pos["alloc"].abs() * pos["nxt"]).groupby("win")["g"].agg(["count", "mean"]) 
    return res

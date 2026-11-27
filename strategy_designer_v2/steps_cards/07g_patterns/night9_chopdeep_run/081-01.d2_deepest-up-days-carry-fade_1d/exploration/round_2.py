def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c / c.shift(1) - 1
            sd = r1.rolling(20, min_periods=15).std()
            hi = c.rolling(20, min_periods=15).max()
            hi60 = c.rolling(60, min_periods=40).max()
            sd60 = r1.rolling(60, min_periods=40).std()
            up = (r1 > 0).astype(int)
            run = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            vol = b["volume"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "sd": sd, "depth": (c / hi - 1) / sd,
                "depth60": (c / hi60 - 1) / sd60,
                "r5": c / c.shift(5) - 1,
                "run": run,
                "vrel": vol / vol.rolling(20, min_periods=15).mean(),
                "sdrel": sd / r1.rolling(120, min_periods=60).std(),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "pos": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["day"] = D["ts"].dt.floor("D")
    D["up"] = D["r1"] > 0

    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series({"n": len(g), "mean": np.nan, "t": np.nan})
        s = g.groupby("day")[col].sum()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(s), "mean": g[col].mean(), "t": t})

    out = {}
    v = D.dropna(subset=["depth", "x1"]).copy()
    u = v[v.up].copy()
    u["dq"] = pd.qcut(u["depth"].rank(method="first"), 5, labels=["deep", "q2", "q3", "q4", "shallow"])
    # agitation split
    u["agit"] = np.where(u["sdrel"] > 1, "agit", np.where(u["sdrel"].notna(), "calm", "na"))
    out["up_depth_x_agit_mean"] = u.groupby(["dq", "agit"])["x1"].mean().unstack()
    out["up_deep_by_agit"] = u[u.dq == "deep"].groupby("agit").apply(summ)
    # 60-day depth
    u6 = u.dropna(subset=["depth60"]).copy()
    u6["d6q"] = pd.qcut(u6["depth60"].rank(method="first"), 5, labels=["deep", "q2", "q3", "q4", "shallow"])
    out["up_by_depth60"] = u6.groupby("d6q").apply(summ)
    # 5-day return before (bounce size) among deep
    dd = u[u.dq.isin(["deep", "q2"])].dropna(subset=["r5"]).copy()
    dd["r5q"] = pd.qcut(dd["r5"].rank(method="first"), 3, labels=["fell5", "mid5", "rose5"])
    out["deepish_up_by_r5"] = dd.groupby("r5q").apply(summ)
    out["deepish_up_by_run"] = dd.groupby(dd["run"].clip(upper=3)).apply(summ)
    dv = dd.dropna(subset=["vrel"]).copy()
    dv["vq"] = pd.qcut(dv["vrel"].rank(method="first"), 3, labels=["lowvol", "midvol", "highvol"])
    out["deepish_up_by_volume"] = dv.groupby("vq").apply(summ)
    # 2-day check deep up
    out["deep_up_f2_minus_f1"] = pd.Series({"f1": u[u.dq == "deep"]["f1"].mean(), "f2": u[u.dq == "deep"]["f2"].mean()})
    # deep down days by depth: rebound grading
    dn = v[~v.up].copy()
    dn["dq"] = pd.qcut(dn["depth"].rank(method="first"), 5, labels=["deep", "q2", "q3", "q4", "shallow"])
    dn["agit"] = np.where(dn["sdrel"] > 1, "agit", "calm")
    out["down_deep_by_agit"] = dn[dn.dq == "deep"].groupby("agit").apply(summ)
    # book: daily returns, worst/best days
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            bd.append(t.assign(coin=coin, w=w))
    B = pd.concat(bd)
    bk = B.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book_extreme_days"] = pd.DataFrame({
        "n": [ (bk.book_return <= q.iloc[0]).sum(), (bk.book_return >= q.iloc[1]).sum()],
        "book_mean": [bk.book_return[bk.book_return <= q.iloc[0]].mean(), bk.book_return[bk.book_return >= q.iloc[1]].mean()],
        "coin_mean": [bk.coin_return[bk.book_return <= q.iloc[0]].mean(), bk.coin_return[bk.book_return >= q.iloc[1]].mean()],
        "share_of_total": [bk.book_return[bk.book_return <= q.iloc[0]].sum() / bk.book_return.sum(), bk.book_return[bk.book_return >= q.iloc[1]].sum() / bk.book_return.sum()],
    }, index=["worst2pct", "best2pct"])
    out["book_by_window"] = bk.groupby("w")["book_return"].agg(["mean", "count"])
    return out

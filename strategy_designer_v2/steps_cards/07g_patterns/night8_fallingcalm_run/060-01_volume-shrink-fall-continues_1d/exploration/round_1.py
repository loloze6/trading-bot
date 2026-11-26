def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["r1"] = c / c.shift(1) - 1
            b["r5"] = c / c.shift(5) - 1
            b["r20"] = c / c.shift(20) - 1
            b["tr60"] = c / c.shift(60) - 1
            b["vr"] = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            b["vr5"] = np.log(v.rolling(5).mean() / v.shift(5).rolling(25).mean())
            b["vol20"] = b["r1"].rolling(20).std()
            b["rng"] = (b["high"] - b["low"]) / c
            b["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["falling"] = b["regime"] == "unknown"
            b["pos"] = b["postRebalance_current_allocation"]
            b["grid"] = (np.arange(len(b)) % H == 0)
            b["coin"] = coin; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    g = B[B["grid"] & B["fwd"].notna()].copy()
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    sd = g.groupby("coin")["fwd"].transform("std")
    g["z"] = g["ex"] / sd

    def ct(sub, col="ex"):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s))
        m = s[col].mean()
        d = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((d ** 2).sum()) / len(s)
        return (m, m / se if se > 0 else np.nan, len(s))

    def tab(sub, key, col="ex", q=None):
        s = sub.dropna(subset=[key, col]).copy()
        if q: s["k"] = pd.qcut(s[key], q, labels=False, duplicates="drop")
        else: s["k"] = s[key]
        out = {}
        for k, x in s.groupby("k"):
            m, t, n = ct(x, col); out[k] = {"mean": m, "t": t, "n": n, "key_mean": x[key].mean() if q else k}
        return pd.DataFrame(out).T

    res = {}
    f = g[g["falling"]]
    nf = g[~g["falling"]].copy()
    nf["trend"] = np.where(nf["tr60"] > 0.10, "rising", np.where(nf["tr60"].notna(), "choppy", "na"))
    res["falling_vr_quintile_ex5"] = tab(f, "vr", q=5)
    res["rising_vr_quintile_ex5"] = tab(nf[nf["trend"] == "rising"], "vr", q=5)
    res["choppy_vr_quintile_ex5"] = tab(nf[nf["trend"] == "choppy"], "vr", q=5)
    res["falling_r5_quintile_ex5"] = tab(f, "r5", q=5)
    res["falling_r20_quintile_ex5"] = tab(f, "r20", q=5)
    res["all_r5_quintile_ex5"] = tab(g, "r5", q=5)
    res["all_vol20_quintile_ex5"] = tab(g, "vol20", q=5)
    res["all_vr5_quintile_ex5"] = tab(g, "vr5", q=5)
    res["all_rng_quintile_ex5"] = tab(g, "rng", q=5)
    res["all_clpos_quintile_ex5"] = tab(g, "clpos", q=5)
    # falling: vr by coin
    res["falling_vr_corr_by_coin"] = f.groupby("coin").apply(lambda x: pd.Series({"rho": stats.spearmanr(x["vr"], x["ex"], nan_policy="omit")[0], "n": x["vr"].notna().sum()}))
    res["falling_by_year_vr_corr"] = f.groupby("yr").apply(lambda x: pd.Series({"rho": stats.spearmanr(x["vr"], x["ex"], nan_policy="omit")[0], "n": x["vr"].notna().sum(), "mean_ex": x["ex"].mean()}))
    # weekday next-day return
    d1 = B.dropna(subset=["fwd1"]).copy()
    d1["ex1"] = d1["fwd1"] - d1.groupby("coin")["fwd1"].transform("mean")
    res["weekday_next1d"] = tab(d1, "wd", col="ex1")
    # book: largest gains/losses days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    bk["wy"] = bk.index.get_level_values("win")
    res["book_by_window"] = bk.groupby("wy").agg(mean_br=("br", "mean"), sum_br=("br", "sum"), mean_cr=("cr", "mean"), n=("br", "size"))
    q = bk["br"].quantile([0.02, 0.98])
    res["book_tail_days"] = pd.DataFrame({"worst2pct_coin_ret": [bk[bk.br <= q.iloc[0]]["cr"].mean()], "best2pct_coin_ret": [bk[bk.br >= q.iloc[1]]["cr"].mean()],
                                          "worst_sum": [bk[bk.br <= q.iloc[0]]["br"].sum()], "best_sum": [bk[bk.br >= q.iloc[1]]["br"].sum()], "total": [bk["br"].sum()]})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    res["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), hit=("net_profit_loss_percent", lambda x: (x > 0).mean()), mean_days=("duration_minutes", lambda x: x.mean() / 1440))
    return res

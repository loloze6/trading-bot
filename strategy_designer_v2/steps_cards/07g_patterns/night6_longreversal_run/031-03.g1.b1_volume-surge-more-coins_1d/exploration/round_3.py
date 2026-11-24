def explore(data):
    import pandas as pd, numpy as np
    H = 14
    grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float); v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            ret14 = s / s.shift(14) - 1
            ret28 = s / s.shift(28) - 1
            r1 = s.pct_change(); vol = r1.rolling(30, min_periods=15).std()
            for i in range(0, len(b) - H, H):
                grid.append(dict(coin=coin, day=ts[i].normalize(), year=ts[i].year,
                                 fwd=s[i+H]/s[i]-1, vr=vr[i], ret14=ret14[i], ret28=ret28[i],
                                 z14=ret14[i] / (vol[i] * np.sqrt(14)) if vol[i] else np.nan))
    g = pd.DataFrame(grid)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g = g.dropna(subset=["vr", "ret14", "ex", "z14"])
    g["era"] = np.where(g["year"] <= 2021, "early", "late")
    def ct(x, day):
        dd = (x - x.mean()).groupby(day).sum(); D = len(dd)
        se = np.sqrt((dd ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series(dict(mean=x.mean(), t=x.mean() / se, n=len(x), days=D))
    res = {}
    # graded vr within rising and falling 14-day price
    for side, sub in [("up", g[g.ret14 > 0]), ("down", g[g.ret14 <= 0])]:
        sub = sub.copy(); sub["q"] = pd.qcut(sub["vr"].rank(method="first"), 4, labels=False)
        res["vr_quart_within_" + side] = sub.groupby("q").apply(lambda x: pd.concat(
            [pd.Series(dict(vr_mean=x["vr"].mean())), ct(x["ex"], x["day"])])).round(4)
    # interaction: vr signed by price direction, as a long-short signal on price direction
    g["inter"] = g["vr"] * np.sign(g["ret14"])
    g["q"] = pd.qcut(g["inter"].rank(method="first"), 5, labels=False)
    g["dex"] = np.sign(g["ret14"]) * g["ex"]
    res["inter_quint_dir_ex(with_price_dir)"] = g.groupby("q").apply(lambda x: pd.concat(
        [pd.Series(dict(lo=x["inter"].min())), ct(x["dex"], x["day"])])).round(4)
    res["inter_quint_by_era_top_minus"] = g[g.q.isin([0, 4])].groupby(["era", "q"]).apply(
        lambda x: ct(x["dex"], x["day"])).round(4)
    # plain vr signal on up vs down subsets
    g["vsig"] = np.sign(g["vr"]) * g["ex"]
    res["vr_sign_signal_by_price_dir"] = g.groupby(g.ret14 > 0).apply(lambda x: ct(x["vsig"], x["day"])).round(4)
    # graded: z14 size within high-vr vs low-vr, direction of price
    g["vhi"] = g["vr"] > 0
    g["zq"] = pd.qcut(g["z14"].abs().rank(method="first"), 3, labels=False)
    res["dir_ex_by_vr_sign_and_move_size"] = g.groupby(["vhi", "zq"]).apply(lambda x: ct(x["dex"], x["day"])).round(4)
    return res

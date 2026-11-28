def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            d = {"coin": coin, "win": w, "pos": np.arange(n),
                 "s7": r7 / (sd30 * np.sqrt(7)),
                 "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                 "infc": (b["regime"] == "unknown").values,
                 "fc": b["forecast"].astype(float)}
            for L in [10, 20, 40]:
                lo = l.rolling(L, min_periods=L // 2).min(); hi = h.rolling(L, min_periods=L // 2).max()
                d["pos%d" % L] = (c - lo) / (hi - lo).replace(0, np.nan)
            # distance above 20-day low in swing units
            lo20 = l.rolling(20, min_periods=10).min()
            d["up_from_low20"] = np.log(c / lo20) / sd30
            hi20 = h.rolling(20, min_periods=10).max()
            d["dn_from_hi20"] = np.log(hi20 / c) / sd30
            for H in [1, 3, 5]:
                d["f%d" % H] = c.shift(-H) / c - 1
            rows.append(pd.DataFrame(d))
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def daily_t(x, col):
        s = x.groupby("day")[col].sum(); k = x.groupby("day")[col].size()
        m = x[col].mean(); n = len(x)
        # se with day-clusters
        se = np.sqrt(((s - k * m) ** 2).sum()) / n
        return m, m / se, n, len(s)
    res = {}
    for H in [1, 3, 5]:
        G = D[(D["pos"] % H == 0) & D["f%d" % H].notna()].copy()
        drift = G.groupby("coin")["f%d" % H].mean()
        G["u"] = G["f%d" % H] - G["coin"].map(drift)
        F = G[G["infc"]].copy()
        for col in ["pos10", "pos20", "pos40", "up_from_low20", "dn_from_hi20", "s7"]:
            x = F.dropna(subset=[col]).copy()
            x["b"] = pd.qcut(x[col].rank(method="first"), 3, labels=False)
            top = x[x["b"] == 2]; bot = x[x["b"] == 0]
            m, t, n, nd = daily_t(top, "u")
            rho = x[[col, "u"]].corr(method="spearman").iloc[0, 1]
            res[(H, col)] = {"top_mean": m, "top_t_day": t, "n": n, "days": nd,
                             "bot_mean": bot["u"].mean(), "spearman": rho}
        if H == 3:
            x = F.dropna(subset=["pos20", "s7"]).copy()
            x["pb"] = pd.qcut(x["pos20"].rank(method="first"), 3, labels=False)
            x["sb"] = (x["s7"] > 0).astype(int)
            out["pos20_x_s7sign_H3"] = x.groupby(["sb", "pb"])["u"].agg(["size", "mean"])
            # among s7>0, does pos20 grade?
            y = x[x["s7"] > 0]
            out["s7pos_spearman"] = pd.Series({"pos20": y[["pos20", "u"]].corr("spearman").iloc[0, 1],
                                               "s7": y[["s7", "u"]].corr("spearman").iloc[0, 1],
                                               "n": len(y),
                                               "pos20_vs_s7": y[["pos20", "s7"]].corr("spearman").iloc[0, 1]})
            # by year top tercile pos20
            x["year"] = pd.to_datetime(x["day"]).dt.year
            out["pos20_top_by_year"] = x[x["pb"] == 2].groupby("year")["u"].agg(["size", "mean"])
            out["pos20_top_by_coin"] = x[x["pb"] == 2].groupby("coin")["u"].agg(["size", "mean"])
    out["terciles"] = pd.DataFrame(res).T
    # book days: largest gains/losses
    Ds = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            Ds.append(dd.assign(coin=coin))
    Ds = pd.concat(Ds)
    br = Ds["book_return"].dropna()
    out["book_tail"] = pd.Series({"days": len(br), "mean": br.mean(),
                                  "top10_sum_share": br.nlargest(10).sum() / br.sum(),
                                  "bot10_sum_share": br.nsmallest(10).sum() / br.sum()})
    return out

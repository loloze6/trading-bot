def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            d = pd.DataFrame({"coin": coin, "win": w})
            d["fc"] = b["regime"].astype(str).eq("unknown")
            d["r1"] = c.pct_change()
            d["r3"] = c / c.shift(3) - 1
            d["r7"] = c / c.shift(7) - 1
            d["r14"] = c / c.shift(14) - 1
            rr = (h - l) / c
            d["mrr"] = rr.rolling(30, min_periods=15).mean()
            d["s7"] = d["r7"] / d["mrr"]
            d["s1"] = d["r1"] / d["mrr"]
            d["rangeratio"] = rr / d["mrr"]
            d["clv"] = (c - l) / (h - l).replace(0, np.nan)
            d["dlow20"] = c / l.rolling(20, min_periods=10).min() - 1
            d["dlow20s"] = d["dlow20"] / d["mrr"]
            d["dhigh20s"] = (c / h.rolling(20, min_periods=10).max() - 1) / d["mrr"]
            d["vol_rel"] = b["volume"] / b["volume"].rolling(30, min_periods=15).mean()
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["f3"] = c.shift(-3) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["pos"] = np.arange(len(b))
            d["alloc"] = b["postRebalance_current_allocation"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift3 = D.loc[D.pos % 3 == 0, "f3"].mean()
    G = D[(D.pos % 3 == 0) & D.f3.notna()].copy()
    G["u3"] = G.f3 - drift3
    F = G[G.fc]
    out = {"drift3": drift3, "n_grid_fc": len(F), "n_grid_all": len(G),
           "fc_mean_u3": F.u3.mean(), "fc_t_u3": stats.ttest_1samp(F.u3, 0).statistic}
    def qtab(df, col, q=5):
        x = df[[col, "u3"]].dropna()
        x["q"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        g = x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("u3", "size"), m=("u3", "mean"), sd=("u3", "std"))
        g["t"] = g.m / (g.sd / np.sqrt(g.n))
        rho = stats.spearmanr(x[col], x.u3)
        g["spearman"] = rho.correlation; g["sp_p"] = rho.pvalue
        return g.drop(columns="sd").round(4)
    for col in ["s7", "s1", "r14", "rangeratio", "clv", "dlow20s", "dhigh20s", "vol_rel"]:
        out["fc_" + col] = qtab(F, col)
    out["all_s7"] = qtab(G, "s7")
    out["fc_weekday"] = F.groupby("wd").u3.agg(["size", "mean", "std"]).assign(t=lambda g: g["mean"]/(g["std"]/np.sqrt(g["size"]))).round(4)
    out["fc_year"] = F.groupby("year").u3.agg(["size", "mean"]).round(4)
    out["fc_coin"] = F.groupby("coin").u3.agg(["size", "mean"]).round(4)
    # down-week cases in falling calm (long side of falls?)
    neg = F[F.r7 < 0]
    out["fc_down7_s7"] = qtab(neg, "s7", 4)
    # interaction: low close & wide range
    F2 = F.dropna(subset=["clv", "rangeratio"]).copy()
    F2["clv_lo"] = F2.clv < 0.33; F2["wide"] = F2.rangeratio > F2.rangeratio.median()
    out["fc_clv_wide"] = F2.groupby(["clv_lo", "wide"]).u3.agg(["size", "mean", "std"]).assign(t=lambda g: g["mean"]/(g["std"]/np.sqrt(g["size"]))).round(4)
    # book daily returns: in-position vs not
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            days.append(dd.assign(coin=coin, win=w))
    DD = pd.concat(days)
    out["book_daily_by_coin"] = DD.groupby("coin").book_return.agg(["mean", "std", "size"]).round(5)
    return out

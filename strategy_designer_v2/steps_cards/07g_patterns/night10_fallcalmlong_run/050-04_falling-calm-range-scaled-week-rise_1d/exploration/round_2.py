def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["fc"] = b["regime"].astype(str).eq("unknown").values
            d["r1"] = c.pct_change()
            d["r7"] = c / c.shift(7) - 1
            d["r14"] = c / c.shift(14) - 1
            rr = (h - l) / c
            d["mrr"] = rr.rolling(30, min_periods=15).mean()
            d["s7"] = d["r7"] / d["mrr"]
            d["s1"] = d["r1"] / d["mrr"]
            d["s14"] = d["r14"] / d["mrr"]
            d["rangeratio"] = rr / d["mrr"]
            d["clv"] = (c - l) / (h - l).replace(0, np.nan)
            d["dlow20s"] = (c / l.rolling(20, min_periods=10).min() - 1) / d["mrr"]
            d["dhigh20s"] = (c / h.rolling(20, min_periods=10).max() - 1) / d["mrr"]
            d["vol_rel"] = b["volume"] / b["volume"].rolling(30, min_periods=15).mean()
            ts = pd.to_datetime(b["timestamp"])
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            d["dayk"] = ts.dt.floor("D").astype("int64").values
            d["f3"] = c.shift(-3) / c - 1
            d["pos"] = np.arange(len(b))
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift3 = D.loc[(D.pos % 3 == 0) & D.f3.notna(), "f3"].mean()
    G = D[(D.pos % 3 == 0) & D.f3.notna()].copy()
    G["u3"] = G.f3 - drift3
    F = G[G.fc].copy()
    def pooled_t(x):
        x = x.dropna(subset=["u3"])
        m = x.u3.mean()
        s = (x.u3 - m).groupby(x.dayk).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return m / se if se > 0 else np.nan
    out = {"summary": pd.Series({"drift3": drift3, "n_grid_fc": len(F), "n_grid_all": len(G),
           "fc_mean_u3": F.u3.mean(), "fc_t_pooled": pooled_t(F),
           "fc_days": F.dayk.nunique()})}
    def qtab(df, col, q=5):
        x = df[[col, "u3", "dayk"]].dropna().copy()
        if len(x) < 2 * q:
            return pd.Series({"n": len(x)})
        x["q"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        res = []
        for k, g in x.groupby("q"):
            res.append({"q": k, "lo": g[col].min(), "hi": g[col].max(), "n": len(g),
                        "m": g.u3.mean(), "t": pooled_t(g)})
        r = pd.DataFrame(res).set_index("q")
        rho = stats.spearmanr(x[col], x.u3)
        r["spearman"] = rho.correlation; r["sp_p"] = rho.pvalue
        return r.round(4)
    for col in ["s7", "s1", "s14", "rangeratio", "clv", "dlow20s", "dhigh20s", "vol_rel"]:
        try:
            out["fc_" + col] = qtab(F, col)
        except Exception as e:
            out["fc_" + col] = str(e)[:80]
    try:
        out["fc_weekday"] = F.groupby("wd").u3.agg(["size", "mean", "std"]).assign(t=lambda g: g["mean"] / (g["std"] / np.sqrt(g["size"]))).round(4)
        out["fc_year"] = F.groupby("year").u3.agg(["size", "mean"]).round(4)
        out["fc_coin"] = F.groupby("coin").u3.agg(["size", "mean"]).round(4)
        out["fc_win"] = F.groupby("win").u3.agg(["size", "mean"]).round(4)
    except Exception as e:
        out["groups_err"] = str(e)[:80]
    try:
        out["fc_down7_s7"] = qtab(F[F.r7 < 0], "s7", 4)
        out["fc_up7_s7"] = qtab(F[F.r7 > 0], "s7", 4)
    except Exception as e:
        out["s7_err"] = str(e)[:80]
    try:
        F2 = F.dropna(subset=["clv", "rangeratio"]).copy()
        F2["clv_lo"] = F2.clv < 0.33
        F2["wide"] = F2.rangeratio > F2.rangeratio.median()
        out["fc_clv_wide"] = F2.groupby(["clv_lo", "wide"]).u3.agg(["size", "mean", "std"]).assign(t=lambda g: g["mean"] / (g["std"] / np.sqrt(g["size"]))).round(4)
    except Exception as e:
        out["clv_err"] = str(e)[:80]
    try:
        days = []
        for coin, wins in data["days"].items():
            for w, dd in wins.items():
                days.append(dd.assign(coin=coin, win=w))
        DD = pd.concat(days)
        out["book_daily_by_coin"] = DD.groupby("coin").book_return.agg(["mean", "std", "size"]).round(5)
    except Exception as e:
        out["days_err"] = str(e)[:80]
    return out

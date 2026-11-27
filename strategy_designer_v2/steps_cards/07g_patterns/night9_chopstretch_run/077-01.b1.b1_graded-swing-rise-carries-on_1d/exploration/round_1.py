def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            z14 = (c / c.shift(14) - 1) / (sd30 * np.sqrt(14))
            z3 = (c / c.shift(3) - 1) / (sd30 * np.sqrt(3))
            z1 = r1 / sd30
            ret60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c / sd30
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol_rel = sd30 / r1.rolling(90).std()
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            n = len(b)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                "day": b["timestamp"].astype(str).str[:10], "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "regime": b["regime"], "fc": b["forecast"], "z14": z14, "z3": z3, "z1": z1,
                "ret60": ret60, "rng": rng, "clo": clo, "vrel": vol_rel, "f7": f7, "f1": f1, "f3": f3,
                "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def tab(D, key, ycol, bins):
        D = D.dropna(subset=[key, ycol]).copy()
        D["q"] = pd.qcut(D[key], bins, duplicates="drop")
        g = D.groupby("q", observed=True)[ycol]
        t = g.mean() / (g.std() / np.sqrt(g.count()))
        return pd.DataFrame({"n": g.count(), "mean%": g.mean() * 100, "t": t})
    for h, col in [(7, "f7"), (3, "f3"), (1, "f1")]:
        drift = A[A.pos % h == 0].groupby("coin")[col].mean()
        A["u" + str(h)] = A[col] - A["coin"].map(drift)
    G7 = A[A.pos % 7 == 0]
    out["z14 quintile u7 in-profile"] = tab(G7[G7.regime == "unknown"], "z14", "u7", 5)
    out["z14 quintile u7 out-profile"] = tab(G7[G7.regime != "unknown"], "z14", "u7", 5)
    out["z14 quintile u7 all"] = tab(G7, "z14", "u7", 10)
    G3 = A[A.pos % 3 == 0]
    out["z3 decile u3 all"] = tab(G3, "z3", "u3", 10)
    G1 = A
    out["z1 decile u1 all"] = tab(G1, "z1", "u1", 10)
    out["range/sd decile u3"] = tab(G3, "rng", "u3", 5)
    out["closeloc quintile u3"] = tab(G3, "clo", "u3", 5)
    out["vol rel quintile u7"] = tab(G7, "vrel", "u7", 5)
    out["ret60 quintile u7"] = tab(G7, "ret60", "u7", 5)
    g = A.dropna(subset=["u1"]).groupby("wd")["u1"]
    out["weekday u1"] = pd.DataFrame({"n": g.count(), "mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count()))})
    out["regime share"] = A["regime"].value_counts(normalize=True)
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "count"]) * 1
    q = bk["book_return"]
    top = bk[q >= q.quantile(0.98)]; bot = bk[q <= q.quantile(0.02)]
    out["book extremes"] = pd.DataFrame({"n": [len(top), len(bot)], "book%": [top.book_return.mean()*100, bot.book_return.mean()*100],
                                       "coin%": [top.coin_return.mean()*100, bot.coin_return.mean()*100]}, index=["top2%", "bot2%"])
    return out

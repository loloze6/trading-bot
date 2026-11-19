def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    hourly = []
    days = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            past = c / c.shift(72) - 1
            loss = (-r1).clip(lower=0)
            gain = r1.clip(lower=0)
            sl = loss.rolling(72).sum()
            top3l = loss.rolling(72).apply(lambda x: np.sort(x)[-3:].sum(), raw=True)
            sg = gain.rolling(72).sum()
            top3g = gain.rolling(72).apply(lambda x: np.sort(x)[-3:].sum(), raw=True)
            vol = r1.rolling(72).std()
            vol720 = r1.rolling(720).std()
            v = b["volume"].astype(float)
            vshare = v.rolling(72).apply(lambda x: np.sort(x)[-3:].sum() / max(x.sum(), 1e-12), raw=True)
            fwd = c.shift(-72) / c - 1
            idx = np.arange(0, len(b), 72)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "past": past.iloc[idx].values,
                "fwd": fwd.iloc[idx].values,
                "grindL": (1 - top3l / sl).iloc[idx].values,
                "grindG": (1 - top3g / sg).iloc[idx].values,
                "vol": vol.iloc[idx].values,
                "volratio": (vol / vol720).iloc[idx].values,
                "vshare": vshare.iloc[idx].values,
                "fc": b["forecast"].iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values,
            })
            rows.append(d)
            hourly.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r1,
                                        "pos": b["postRebalance_current_allocation"].astype(float),
                                        "nxt": c.shift(-1) / c - 1}))
            dd = data["days"][coin][w].copy()
            dd["coin"] = coin; dd["w"] = w
            days.append(dd)
    g = pd.concat(rows).dropna(subset=["past", "fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def summ(df, key):
        a = df.groupby(key, observed=True)["ex"].agg(["count", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a
    g["pastq"] = g.groupby("coin")["past"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["fwd excess by past72 quintile (per-coin)"] = summ(g, "pastq")
    dn = g[g.past < 0].copy(); up = g[g.past > 0].copy()
    dn["gq"] = pd.qcut(dn["grindL"], 4, labels=False)
    up["gq"] = pd.qcut(up["grindG"], 4, labels=False)
    out["down moves: fwd excess by grind quartile"] = summ(dn, "gq")
    out["up moves: fwd excess by grind quartile"] = summ(up, "gq")
    dn["vq"] = pd.qcut(dn["vshare"], 4, labels=False)
    up["vq"] = pd.qcut(up["vshare"], 4, labels=False)
    out["down: by top3 volume share quartile"] = summ(dn, "vq")
    out["up: by top3 volume share quartile"] = summ(up, "vq")
    g["volq"] = g.groupby("coin")["volratio"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["fwd excess by vol ratio (72h/720h) quartile"] = summ(g.dropna(subset=["volq"]), "volq")
    # past * signed by vol ratio interaction: reversal strength
    gg = g.dropna(subset=["volq"]).copy()
    gg["z"] = gg["past"] / (gg["vol"] * np.sqrt(72))
    out["corr(z past, fwd excess) by vol quartile"] = gg.groupby("volq").apply(lambda x: pd.Series({"n": len(x), "corr": x["z"].corr(x["ex"])}))
    out["corr(z past, fwd ex) by coin"] = gg.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "corr": x["z"].corr(x["ex"])}))
    h = pd.concat(hourly).dropna()
    hh = h.groupby("hour")["r"].agg(["count", "mean", "std"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["1h return by hour"] = hh[["count", "mean", "t"]]
    wd = h.groupby("wd")["r"].agg(["count", "mean", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["1h return by weekday"] = wd[["count", "mean", "t"]]
    D = pd.concat(days).dropna(subset=["book_return"])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book daily by year"] = D.groupby("year").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book daily by coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out

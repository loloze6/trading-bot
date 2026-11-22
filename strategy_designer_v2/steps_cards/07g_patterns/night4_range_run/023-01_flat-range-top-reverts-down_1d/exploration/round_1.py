def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            mx = hi.rolling(30).max(); mn = lo.rolling(30).min()
            rng = mx - mn
            ratio = (c - c.shift(29)).abs() / rng
            mid = (c - (mx + mn) / 2) / c * 100
            rngpos = (c - mn) / rng  # 0..1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            ret5past = c / c.shift(5) - 1
            ret1past = r1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            n = len(b)
            idx = np.arange(0, n, H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": idx,
                "fc": b["forecast"].values[idx],
                "alloc": b["postRebalance_current_allocation"].values[idx],
                "ratio": ratio.values[idx], "mid": mid.values[idx], "rngpos": rngpos.values[idx],
                "vol20": vol20.values[idx], "past5": ret5past.values[idx], "past1": ret1past.values[idx],
                "fwd": fwd.values[idx],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                "rngpct": (rng / c).values[idx],
            })
            rows.append(d)
    g = pd.concat(rows, ignore_index=True)
    g = g.dropna(subset=["fwd"])
    cm = g.groupby("coin")["fwd"].agg(["mean", "std"])
    g["drift"] = g["coin"].map(cm["mean"]); g["usd"] = g["coin"].map(cm["std"])
    g["ex"] = (g["fwd"] - g["drift"]) / g["usd"]
    out = {}
    out["coin 5d mean/std"] = cm

    def tab(df, key, q=5):
        df = df.dropna(subset=[key, "ex"]).copy()
        df["q"] = df.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = df.groupby("q")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "t", "count"]]

    flat = g[g["ratio"] <= 0.33]; trend = g[g["ratio"] > 0.33]
    out["flat: rngpos quintile -> ex5 strength"] = tab(flat, "rngpos")
    out["trend: rngpos quintile -> ex5 strength"] = tab(trend, "rngpos")
    out["all: ratio quintile -> ex5"] = tab(g, "ratio")
    out["all: past5 quintile -> ex5"] = tab(g, "past5")
    out["all: vol20 quintile -> ex5"] = tab(g, "vol20")
    out["all: rangewidth quintile -> ex5"] = tab(g, "rngpct")
    out["flat: past5 quintile -> ex5"] = tab(flat, "past5")
    out["trend: past5 quintile -> ex5"] = tab(trend, "past5")
    # correlations by regime
    res = {}
    for nm, df in [("flat", flat), ("trend", trend), ("all", g)]:
        for k in ["rngpos", "past5", "vol20", "ratio"]:
            dd = df.dropna(subset=[k, "ex"])
            r, p = stats.spearmanr(dd[k], dd["ex"])
            res[(nm, k)] = (round(r, 4), round(p, 4), len(dd))
    out["spearman (regime,var)->(rho,p,n)"] = pd.Series(res).astype(str)
    out["weekday -> ex5"] = g.groupby("wd")["ex"].agg(["mean", "count"])
    # by year: forecast*ex
    act = g[g["fc"] != 0].copy()
    act["score"] = act["fc"] / 10 * (act["fwd"] - act["drift"])
    out["active score by coin"] = act.groupby("coin")["score"].agg(["mean", "count"])
    # book daily: largest gains/losses context
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["c_next"] = d["coin_return"].shift(-1)
            dl.append(d)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["book_return"])
    D["ex_book"] = D["book_return"]
    out["book daily mean/std by coin"] = D.groupby("coin")["book_return"].agg(["mean", "std", "count"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 20, labels=False)
    out["book ventile: mean book, coin ret"] = D.groupby("bq")[["book_return", "coin_return"]].mean().iloc[[0, 1, 18, 19]]
    out["corr book vs coin daily"] = float(D[["book_return", "coin_return"]].corr().iloc[0, 1])
    out["n grid all"] = len(g)
    return out

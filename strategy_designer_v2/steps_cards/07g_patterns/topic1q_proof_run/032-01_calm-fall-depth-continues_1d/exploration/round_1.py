def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": c.shift(-1) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "p1": c / c.shift(1) - 1,
                "p5": c / c.shift(5) - 1,
                "p30": c / c.shift(30) - 1,
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "inprof": (b["regime"] == "unknown").astype(int),
                "fc": b["forecast"],
                "pos": b["postRebalance_current_allocation"],
                "pos_gain": b["postRebalance_current_allocation"] * (c.shift(-1) / c - 1),
            })
            d["vol20"] = d["p1"].rolling(20).std()
            d["vol_rel"] = d["vol20"] / d["p1"].abs().expanding(20).mean()
            d["rng_rel"] = d["rng"] / d["rng"].rolling(20).mean().shift(1)
            d["pos_idx"] = np.arange(len(d))
            rows.append(d)
    X = pd.concat(rows, ignore_index=True)
    drift = X.groupby("coin")["r1"].mean()
    X["ex1"] = X["r1"] - X["coin"].map(drift)
    X["day"] = X["ts"].dt.floor("D")

    def tab(df, key, col="ex1"):
        g = df.dropna(subset=[key, col])
        out = []
        for k, s in g.groupby(key, observed=True):
            daily = s.groupby("day")[col].mean()
            out.append({"grp": str(k), "n": len(s), "days": len(daily), "mean%": 100 * daily.mean(),
                        "t": daily.mean() / (daily.std(ddof=1) / np.sqrt(len(daily))) if len(daily) > 2 else np.nan})
        return pd.DataFrame(out)

    res = {}
    X["q30"] = X.groupby("coin")["p30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["all bars: next-day excess by 30d return quintile"] = tab(X, "q30")
    P = X[X.inprof == 1].copy()
    P["q30p"] = pd.qcut(P["p30"], 3, labels=False)
    res["in profile: by 30d tercile"] = tab(P, "q30p")
    res["in profile vs out: next-day excess"] = tab(X, "inprof")
    X["q1"] = X.groupby("coin")["p1"].transform(lambda s: pd.qcut(s, 5, labels=False))
    res["all: by 1d return quintile"] = tab(X, "q1")
    X["q5"] = X.groupby("coin")["p5"].transform(lambda s: pd.qcut(s, 5, labels=False))
    res["all: by 5d return quintile"] = tab(X, "q5")
    X["qv"] = X.groupby("coin")["vol_rel"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res["all: by vol_rel tercile"] = tab(X, "qv")
    X["qc"] = pd.cut(X["clpos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    res["all: by close position in range"] = tab(X, "qc")
    X["wd"] = X["ts"].dt.dayofweek
    res["all: by weekday"] = tab(X, "wd")
    P["q1p"] = pd.qcut(P["p1"], 3, labels=False)
    res["in profile: by 1d tercile"] = tab(P, "q1p")
    P["q5p"] = pd.qcut(P["p5"], 3, labels=False)
    res["in profile: by 5d tercile"] = tab(P, "q5p")
    # crossed: 30d quint x 1d quint, all bars
    X["q30_q1"] = X["q30"].astype("Int64").astype(str) + "_" + X["q1"].astype("Int64").astype(str)
    t = tab(X, "q30_q1")
    res["all: 30d quint x 1d quint"] = t
    # book: by window, year
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["w"] = w; dd["coin"] = coin; D.append(dd)
    D = pd.concat(D)
    bk = D.groupby(["w"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    res["book vs coin mean daily return by window (%)"] = bk * 100
    return res

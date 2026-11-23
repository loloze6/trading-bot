def explore(data):
    import numpy as np, pandas as pd
    out = {}
    feats = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy()
            b = data["bars"][coin][w].copy()
            b["dk"] = pd.to_datetime(b["timestamp"], utc=True).dt.floor("D")
            alloc = b.groupby("dk")["postRebalance_current_allocation"].last()
            fc = b.groupby("dk")["forecast"].last()
            d["dk"] = pd.to_datetime(d["day"], utc=True).dt.floor("D")
            d = d.set_index("dk")
            d["alloc"] = alloc.reindex(d.index).values
            d["fc"] = fc.reindex(d.index).values
            c = d["close"]
            d["ret20"] = c / c.shift(20) - 1
            d["ret5"] = c / c.shift(5) - 1
            d["trend"] = c / c.rolling(100, min_periods=50).mean() - 1
            d["vol20"] = d["coin_return"].rolling(20).std()
            d["fwd5"] = c.shift(-5) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["wn"] = int(w[1:])
            d["year"] = d.index.year
            feats.append(d.reset_index())
    F = pd.concat(feats, ignore_index=True)
    F["inpos"] = F.groupby(["coin", "wn"])["alloc"].shift(1).fillna(0).abs() > 0
    B = F.dropna(subset=["book_return"])
    bk = B.groupby(["wn", "dk"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"),
                                     year=("year", "first")).reset_index().sort_values(["wn", "dk"])
    v = (1 + bk["br"]).cumprod()
    dd = v / v.cummax() - 1
    bk["dd"] = dd.values
    out["max_dd"] = float(dd.min())
    # drawdown episodes
    bk["peakid"] = (bk["dd"] == 0).cumsum()
    ep = bk.groupby("peakid").agg(depth=("dd", "min"), days=("dd", "size"), wfirst=("wn", "min"), wlast=("wn", "max"),
                                  coin_chain=("cr", lambda x: (1 + x).prod() - 1), book_chain=("br", lambda x: (1 + x).prod() - 1),
                                  year=("year", "first"))
    out["worst_episodes"] = ep.sort_values("depth").head(6).round(4)
    out["per_year"] = bk.groupby("year").agg(book=("br", lambda x: (1 + x).prod() - 1), coin=("cr", lambda x: (1 + x).prod() - 1),
                                             worst=("dd", "min")).round(4)
    # pair-level book by coin state, days in position
    P = B[B["inpos"]].copy()
    for col in ["ret20", "trend", "vol20"]:
        P[col + "q"] = P.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        g = P.groupby(col + "q")["book_return"].agg(["mean", "std", "count"])
        g["sharpe"] = g["mean"] / g["std"] * np.sqrt(365)
        out["pos_book_by_" + col] = g.round(5)
    # grid: condition alone vs with signal
    G = F[(F["pos"] % 5 == 0)].dropna(subset=["fwd5"]).copy()
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex"] = G["fwd5"] - G["coin"].map(drift)
    G["sig"] = G["fc"] > 0
    res = []
    for col in ["ret20", "trend", "vol20", "ret5"]:
        g = G.dropna(subset=[col]).copy()
        g["q"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        t = g.groupby(["q", "sig"])["fwd5"].agg(["mean", "std", "count"])
        t["ex"] = g.groupby(["q", "sig"])["ex"].mean()
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["p10"] = g.groupby(["q", "sig"])["fwd5"].quantile(0.1)
        t = t.reset_index(); t["feat"] = col
        res.append(t)
    out["grid_by_state"] = pd.concat(res)[["feat", "q", "sig", "mean", "ex", "p10", "count", "t"]].round(4)
    s = G[G["sig"]].copy()
    s["fq"] = pd.qcut(s["fc"].rank(method="first"), 3, labels=False)
    out["by_fc_tercile"] = s.groupby("fq").agg(mean=("fwd5", "mean"), ex=("ex", "mean"), n=("fwd5", "size"), fc=("fc", "mean")).round(4)
    # book on worst 5% days: share in position, coin state
    thr = bk["br"].quantile(0.05)
    worstdays = bk[bk["br"] <= thr][["wn", "dk"]]
    W = B.merge(worstdays, on=["wn", "dk"])
    out["worst_days_state"] = pd.DataFrame({"inpos_share": [W["inpos"].mean(), B["inpos"].mean()],
                                            "trend_mean": [W["trend"].mean(), B["trend"].mean()],
                                            "ret20_mean": [W["ret20"].mean(), B["ret20"].mean()]},
                                           index=["worst5pct", "all"]).round(4)
    out["mean_alloc_inpos"] = float(P["alloc"].abs().mean())
    return out

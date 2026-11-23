def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily series
    rows = []
    feats = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy()
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D") if not np.issubdtype(d["day"].dtype, np.datetime64) else d["day"].dt.floor("D")
            d = d.set_index("day")
            d["alloc"] = alloc.reindex(d.index).values
            d["fc"] = fc.reindex(d.index).values
            c = d["close"]
            d["ret20"] = c / c.shift(20) - 1
            d["ret60"] = c / c.shift(60) - 1
            d["near"] = c / c.rolling(60, min_periods=20).max() - 1
            d["vol20"] = d["coin_return"].rolling(20).std()
            d["fwd5"] = c.shift(-5) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["w"] = w
            d["wn"] = int(w[1:])
            feats.append(d.reset_index())
    F = pd.concat(feats)
    # book daily
    bk = F.dropna(subset=["book_return"]).groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), alloc=("alloc", "mean"), r20=("ret20", "mean"), vol=("vol20", "mean"), near=("near","mean")).reset_index().sort_values(["wn", "day"])
    v = (1 + bk["br"]).cumprod()
    peak = v.cummax()
    dd = v / peak - 1
    bk["dd"] = dd.values
    out["max_dd"] = float(dd.min())
    # per window: book return, coin return, min dd in window
    pw = bk.groupby("wn").agg(book=("br", lambda x: (1 + x).prod() - 1), coin=("cr", lambda x: (1 + x).prod() - 1), alloc=("alloc", "mean"), worst_dd=("dd", "min"), r20=("r20","mean"), vol=("vol","mean"))
    out["per_window"] = pw.round(4)
    # days in deep drawdown (dd < half max) vs other
    bk["deep"] = bk["dd"] < 0.5 * dd.min()
    # falling days: book down days in drawdown-deepening
    bk["deepening"] = (bk["dd"] < bk["dd"].shift(1)) & (bk["dd"] < -0.1)
    out["state_by_dd"] = bk.groupby("deepening")[["br", "cr", "alloc", "r20", "vol", "near"]].mean().round(4)
    # grid analysis
    G = F[(F["pos"] % 5 == 0)].dropna(subset=["fwd5"]).copy()
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex"] = G["fwd5"] - G["coin"].map(drift)
    G["sig"] = G["fc"] > 0
    res = []
    for name, col in [("ret20", "ret20"), ("ret60", "ret60"), ("near", "near"), ("vol20", "vol20")]:
        g = G.dropna(subset=[col]).copy()
        g["q"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
        t = g.groupby(["q", "sig"])["fwd5"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t = t.reset_index(); t["feat"] = name
        res.append(t)
    out["grid_by_state"] = pd.concat(res)[["feat", "q", "sig", "mean", "count", "t"]].round(4)
    # forecast strength terciles among sig
    s = G[G["sig"]].copy()
    s["fq"] = pd.qcut(s["fc"].rank(method="first"), 3, labels=False)
    out["by_fc_tercile"] = s.groupby("fq")["fwd5"].agg(["mean", "count"]).round(4)
    # book daily return by state of coin (pair level), when in position
    P = F.dropna(subset=["book_return"]).copy()
    P["inpos"] = P["alloc"].shift(1).fillna(0).abs() > 0
    P["r20q"] = P.groupby("coin")["ret20"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    P["volq"] = P.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["pair_book_by_r20"] = P[P["inpos"]].groupby("r20q")["book_return"].agg(["mean", "std", "count"]).round(5)
    out["pair_book_by_vol"] = P[P["inpos"]].groupby("volq")["book_return"].agg(["mean", "std", "count"]).round(5)
    return out

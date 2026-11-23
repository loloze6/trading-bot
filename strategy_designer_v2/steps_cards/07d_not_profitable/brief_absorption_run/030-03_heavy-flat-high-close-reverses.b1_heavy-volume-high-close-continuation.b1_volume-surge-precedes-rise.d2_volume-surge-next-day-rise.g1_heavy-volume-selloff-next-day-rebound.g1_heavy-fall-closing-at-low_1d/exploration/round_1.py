def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            b["coin"] = coin; b["win"] = w; b["wn"] = int(w[1:])
            b["nxt"] = c.shift(-1) / c - 1
            b["ret1"] = c.pct_change()
            b["ret20"] = c / c.shift(20) - 1
            b["ret5"] = c / c.shift(5) - 1
            b["vol20"] = b["ret1"].rolling(20).std()
            b["vol_ratio"] = b["vol20"] / b["ret1"].rolling(60).std()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["cl_low"] = (b["high"] - c) / rng
            b["vr"] = b["volume"] / b["volume"].shift(1).rolling(20).mean()
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"] * b["nxt"]
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["year"] = b["ts"].dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B = B[B["nxt"].notna()]
    mu = B.groupby("coin")["nxt"].mean()
    B["ex"] = B["nxt"] - B["coin"].map(mu)
    out = {}
    # book daily chain
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["wn"] = int(w[1:]); D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    bk = bk[bk["br"].notna()]
    v = (1 + bk["br"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v / peak - 1
    bk["dd"] = dd
    i = int(np.argmin(dd)); j = int(np.argmax(v[:i + 1]))
    out["deepest fall"] = pd.Series({"depth": dd[i], "days": i - j, "window_start": bk["wn"].iloc[j], "window_end": bk["wn"].iloc[i],
                                     "coins mean return in fall": (1 + bk["cr"].iloc[j + 1:i + 1]).prod() - 1})
    # falls per window
    out["book by window"] = bk.groupby("wn").agg(book=("br", lambda x: (1 + x).prod() - 1), coins=("cr", lambda x: (1 + x).prod() - 1), mindd=("dd", "min")).round(3)
    A = B[B["alloc"].abs() > 1e-6]
    out["n active bars"] = len(A)
    out["active share on down day"] = float((A["ret1"] < 0).mean())
    # gain by prior 20d trend quintile
    A = A.copy()
    A["q20"] = pd.qcut(A["ret20"], 5, labels=False)
    g = A.groupby("q20").agg(n=("gain", "size"), gain=("gain", "mean"), nxt=("nxt", "mean"), alloc=("alloc", "mean"), r20=("ret20", "mean"))
    g["t"] = A.groupby("q20")["nxt"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["active by prior 20d return quintile"] = g.round(4)
    A["qv"] = pd.qcut(A["vol_ratio"], 5, labels=False)
    out["active by vol20/vol60 quintile"] = A.groupby("qv").agg(n=("gain", "size"), gain=("gain", "mean"), nxt=("nxt", "mean"), alloc=("alloc", "mean")).round(4)
    A["qa"] = pd.qcut(A["alloc"], 5, labels=False, duplicates="drop")
    out["active by alloc quintile"] = A.groupby("qa").agg(n=("gain", "size"), gain=("gain", "mean"), nxt=("nxt", "mean"), alloc=("alloc", "mean"), gsd=("gain", "std")).round(4)
    # down days: signal strength vs trend; condition alone
    Dn = B[B["ret1"] < 0].copy()
    Dn["sig"] = Dn["cl_low"] * Dn["vr"]
    Dn["strong"] = Dn["sig"] >= Dn["sig"].quantile(0.8)
    Dn["downtrend"] = Dn["ret20"] < 0
    res = {}
    for k, gg in Dn.groupby(["downtrend", "strong"]):
        res[str(k)] = {"n": len(gg), "ex": gg["ex"].mean(), "t": gg["ex"].mean() / gg["ex"].std() * np.sqrt(len(gg))}
    allb = B.dropna(subset=["ret20"])
    for k, gg in allb.groupby(allb["ret20"] < 0):
        res["all bars downtrend=" + str(k)] = {"n": len(gg), "ex": gg["ex"].mean(), "t": gg["ex"].mean() / gg["ex"].std() * np.sqrt(len(gg))}
    out["down days: downtrend x strong signal"] = pd.DataFrame(res).T.round(4)
    # holding behaviour: alloc on up days
    out["alloc share held on up days"] = float((B.loc[B["ret1"] > 0, "alloc"].abs() > 1e-6).mean())
    out["gain up-day held vs down-day held"] = A.groupby(A["ret1"] < 0)["gain"].agg(["size", "mean"]).round(5)
    return out

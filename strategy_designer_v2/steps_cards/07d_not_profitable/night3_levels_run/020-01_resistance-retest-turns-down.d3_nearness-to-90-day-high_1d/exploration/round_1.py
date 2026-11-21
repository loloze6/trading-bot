def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    windows = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns per window
    chain = []
    for w in windows:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna()
        g["w"] = w
        chain.append(g.reset_index())
    ch = pd.concat(chain, ignore_index=True)
    ch["eq"] = (1 + ch["book"]).cumprod()
    ch["peak"] = ch["eq"].cummax()
    ch["dd"] = ch["eq"] / ch["peak"] - 1
    ch["heq"] = (1 + ch["hold"]).cumprod()
    ch["hdd"] = ch["heq"] / ch["heq"].cummax() - 1
    # per window stats
    ws = ch.groupby("w").agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"), n=("book", "size"),
                              min_dd=("dd", "min"))
    ws["book_chain"] = ch.groupby("w")["book"].apply(lambda x: (1 + x).prod() - 1)
    ws["hold_chain"] = ch.groupby("w")["hold"].apply(lambda x: (1 + x).prod() - 1)
    ws = ws.reindex(windows)
    out["windows"] = ws.round(4)
    # drawdown episodes
    ch["in_dd"] = ch["dd"] < 0
    ep = (ch["in_dd"] != ch["in_dd"].shift()).cumsum()
    eps = []
    for k, grp in ch[ch["in_dd"]].groupby(ep[ch["in_dd"]]):
        i = grp["dd"].idxmin()
        eps.append({"start_w": grp["w"].iloc[0], "trough_w": ch.loc[i, "w"], "depth": grp["dd"].min(),
                    "days_to_trough": int(i - grp.index[0]), "len": len(grp),
                    "hold_ret_to_trough": (1 + ch.loc[grp.index[0]:i, "hold"]).prod() - 1})
    eps = pd.DataFrame(eps).sort_values("depth").head(8)
    out["deepest_falls"] = eps.round(4)
    years = len(ch) / 365
    out["summary"] = pd.Series({"years": years, "cagr": ch["eq"].iloc[-1] ** (1 / years) - 1,
                                "maxdd": ch["dd"].min(), "hold_maxdd": ch["hdd"].min(),
                                "hold_cagr": ch["heq"].iloc[-1] ** (1 / years) - 1}).round(4)
    # per-coin bar-level states
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.shift(-1) / cl - 1
            pos = b["postRebalance_current_allocation"]
            raw = b["debug_info.components.high_prox.last_history_value"]
            f = b["forecast"]
            ret20 = cl / cl.shift(20) - 1
            ret5p = cl / cl.shift(5) - 1
            vol = np.log(cl).diff().rolling(20).std()
            fwd5 = cl.shift(-5) / cl - 1
            grid = (np.arange(len(b)) % 5 == 0)
            rows.append(pd.DataFrame({"coin": c, "w": w, "pos": pos, "gain": pos * r1, "r1": r1, "raw": raw,
                                      "f": f, "ret20": ret20, "ret5p": ret5p, "vol": vol, "fwd5": fwd5,
                                      "grid": grid}))
    B = pd.concat(rows, ignore_index=True)
    B["volq"] = B.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    B["r20q"] = B.groupby("coin")["ret20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    B["rawq"] = B.groupby("coin")["raw"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    B["fq"] = pd.qcut(B["f"].rank(method="first"), 5, labels=False)
    def tab(key):
        g = B.dropna(subset=["gain", key]).groupby(key)
        t = g.agg(gain_mean=("gain", "mean"), gain_std=("gain", "std"), pos=("pos", "mean"), r1=("r1", "mean"), n=("gain", "size"))
        t["worst_1pct"] = g["gain"].quantile(0.01)
        G = B[B["grid"]].dropna(subset=["fwd5", key]).groupby(key)["fwd5"]
        t["fwd5_grid"] = G.mean(); t["fwd5_t"] = G.mean() / (G.std() / np.sqrt(G.size())); t["n5"] = G.size()
        return t.round(5)
    out["by_vol_q"] = tab("volq")
    out["by_ret20_q"] = tab("r20q")
    out["by_raw_nearness_q"] = tab("rawq")
    out["by_forecast_q"] = tab("fq")
    return out

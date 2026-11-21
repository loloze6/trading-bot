def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    windows = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    chain = []
    for w in windows:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); frames.append(d)
        g = pd.concat(frames).groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna()
        g["w"] = w; chain.append(g.reset_index())
    ch = pd.concat(chain, ignore_index=True)
    ch["eq"] = (1 + ch["book"]).cumprod(); ch["peak"] = ch["eq"].cummax(); ch["dd"] = ch["eq"] / ch["peak"] - 1
    # falling legs: from peak to trough of episodes deeper than 15%
    ch["leg"] = False
    ind = ch["dd"] < 0
    ep = (ind != ind.shift()).cumsum()
    for k, grp in ch[ind].groupby(ep[ind]):
        if grp["dd"].min() < -0.15:
            i = grp["dd"].idxmin()
            ch.loc[grp.index[0]:i, "leg"] = True
    out["leg_share_days"] = pd.Series({"leg_days": int(ch["leg"].sum()), "all": len(ch),
                                       "book_sum_leg": ch.loc[ch["leg"], "book"].sum(),
                                       "hold_sum_leg": ch.loc[ch["leg"], "hold"].sum(),
                                       "book_sum_rest": ch.loc[~ch["leg"], "book"].sum()}).round(4)
    legdays = set(zip(ch.loc[ch["leg"], "w"], ch.loc[ch["leg"], "day"]))
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.shift(-1) / cl - 1
            pos = b["postRebalance_current_allocation"]
            raw = b["debug_info.components.high_prox.last_history_value"]
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            hiA = cl / raw
            hich20 = hiA / hiA.shift(20) - 1
            ret40 = cl / cl.shift(40) - 1
            fwd5 = cl.shift(-5) / cl - 1
            grid = (np.arange(len(b)) % 5 == 0)
            leg = [(w, d) in legdays for d in day]
            rows.append(pd.DataFrame({"coin": c, "yr": day.dt.year.values, "pos": pos, "gain": pos * r1, "r1": r1,
                                      "raw": raw, "hich20": hich20, "ret40": ret40, "fwd5": fwd5, "grid": grid,
                                      "leg": leg}))
    B = pd.concat(rows, ignore_index=True)
    B["rawq"] = B.groupby("coin")["raw"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    B["hi_state"] = np.where(B["hich20"] > 1e-9, "high_rising", np.where(B["hich20"] < -1e-9, "high_falling", "high_flat"))
    def tab(df, keys):
        g = df.dropna(subset=["gain"] + keys).groupby(keys)
        t = g.agg(gain=("gain", "mean"), gsum=("gain", "sum"), pos=("pos", "mean"), r1=("r1", "mean"), n=("gain", "size"))
        G = df[df["grid"]].dropna(subset=["fwd5"] + keys).groupby(keys)["fwd5"]
        t["fwd5"] = G.mean(); t["t5"] = G.mean() / (G.std() / np.sqrt(G.size())); t["n5"] = G.size()
        return t.round(5)
    out["leg_by_rawq"] = tab(B[B["leg"]], ["rawq"])
    out["rest_by_rawq"] = tab(B[~B["leg"]], ["rawq"])
    out["by_hi_state"] = tab(B, ["hi_state"])
    out["hi_state_x_rawq"] = tab(B, ["hi_state", "rawq"])
    out["leg_by_hi_state"] = tab(B[B["leg"]], ["hi_state"])
    out["bear_years_by_rawq"] = tab(B[B["yr"].isin([2018, 2022])], ["rawq"])
    return out

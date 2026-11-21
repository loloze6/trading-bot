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
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); d["coin"] = c; frames.append(d)
        g = pd.concat(frames).groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna()
        g["w"] = w; chain.append(g.reset_index())
    ch = pd.concat(chain, ignore_index=True)
    ch["eq"] = (1 + ch["book"]).cumprod(); ch["dd"] = ch["eq"] / ch["eq"].cummax() - 1
    ch["deep"] = ch["dd"] < -0.25
    deepdays = set(zip(ch.loc[ch["deep"], "w"], ch.loc[ch["deep"], "day"]))
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.shift(-1) / cl - 1
            pos = b["postRebalance_current_allocation"]
            raw = b["debug_info.components.high_prox.last_history_value"]
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            ret20 = cl / cl.shift(20) - 1
            ret40 = cl / cl.shift(40) - 1
            draw10 = raw - raw.shift(10)
            hi = cl.cummax()  # in-window running high
            new_hi = (cl >= cl.rolling(10, min_periods=1).max()).astype(int)
            fwd5 = cl.shift(-5) / cl - 1
            grid = (np.arange(len(b)) % 5 == 0)
            yr = day.dt.year
            deep = [ (w, d) in deepdays for d in day ]
            rows.append(pd.DataFrame({"coin": c, "w": w, "yr": yr.values, "pos": pos, "gain": pos * r1, "r1": r1,
                                      "raw": raw, "ret20": ret20, "ret40": ret40, "draw10": draw10,
                                      "fwd5": fwd5, "grid": grid, "deep": deep, "newhi10": new_hi}))
    B = pd.concat(rows, ignore_index=True)
    B["rawq"] = B.groupby("coin")["raw"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    B["r40q"] = B.groupby("coin")["ret40"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    B["d10q"] = B.groupby("coin")["draw10"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    def tab(df, keys):
        g = df.dropna(subset=["gain"] + keys).groupby(keys)
        t = g.agg(gain=("gain", "mean"), gsum=("gain", "sum"), pos=("pos", "mean"), r1=("r1", "mean"), n=("gain", "size"))
        G = df[df["grid"]].dropna(subset=["fwd5"] + keys).groupby(keys)["fwd5"]
        t["fwd5"] = G.mean(); t["t5"] = G.mean() / (G.std() / np.sqrt(G.size())); t["n5"] = G.size()
        return t.round(5)
    out["deep_vs_not"] = tab(B, ["deep"])
    out["deep_by_rawq"] = tab(B[B["deep"]], ["rawq"])
    out["notdeep_by_rawq"] = tab(B[~B["deep"]], ["rawq"])
    out["by_ret40q"] = tab(B, ["r40q"])
    out["top_near_by_ret40_sign"] = tab(B[B["rawq"] == 4].assign(up40=lambda d: d["ret40"] > 0), ["up40"])
    out["by_draw10q"] = tab(B, ["d10q"])
    out["top_near_by_newhi10"] = tab(B[B["rawq"] == 4], ["newhi10"])
    out["by_year"] = tab(B, ["yr"])
    out["by_coin"] = tab(B, ["coin"])
    return out

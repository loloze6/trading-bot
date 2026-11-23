def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    recs = []; grid = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True).copy()
            rng = b["high"] - b["low"]
            b["ratio"] = rng / rng.rolling(30, min_periods=20).mean()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            b["next1"] = b["close"].shift(-1) / b["close"] - 1
            for h in (5, 10, 20):
                b[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["coin"] = coin; b["w"] = w; b["i"] = range(len(b))
            b["alloc"] = b["postRebalance_current_allocation"]
            recs.append(b[["coin", "w", "i", "ratio", "ret20", "dayret", "next1", "alloc", "forecast"]])
            for h in (5, 10, 20):
                g = b.iloc[::h][["coin", "ratio", "ret20", "dayret", f"f{h}"]].copy()
                g["h"] = h; g = g.rename(columns={f"f{h}": "fwd"}); grid.append(g)
    G = pd.concat(grid).dropna(subset=["fwd", "ratio", "ret20"])
    G["drift"] = G.groupby(["coin", "h"])["fwd"].transform("mean")
    G["ex"] = G["fwd"] - G["drift"]
    G["rq"] = G.groupby("h")["ratio"].transform(lambda s: pd.qcut(s, 5, labels=False)) + 1
    G["hi"] = np.where(G["rq"] >= 4, "wide", "narrow")
    G["trend"] = np.where(G["ret20"] > 0, "up", "down")
    def summ(df, keys):
        r = df.groupby(keys)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["total"] = df.groupby(keys)["fwd"].mean()
        return r.drop(columns="std")
    out = {}
    out["by_h_rq"] = summ(G, ["h", "rq"])
    out["trend_x_wide_h5"] = summ(G[G.h == 5], ["trend", "hi"])
    out["trend_x_wide_h20"] = summ(G[G.h == 20], ["trend", "hi"])
    B = pd.concat(recs).dropna(subset=["next1"]).reset_index(drop=True)
    cost = 0.0019 / 2
    def book(pos):
        x = B[["coin", "w", "i"]].copy(); x["pos"] = pos.values
        x["chg"] = x.groupby(["coin", "w"])["pos"].diff().abs().fillna(x["pos"].abs())
        x["g"] = x["pos"] * B["next1"].values - x["chg"] * cost
        d = x.groupby(["w", "i"])["g"].mean()
        inpos = (x["pos"] != 0).mean()
        ordered = pd.concat([d.loc[w] for w in sorted(d.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))])
        v = (1 + ordered).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(v)) - 1
        return pd.Series({"mean_in_pos": d.mean() / inpos, "share_in_pos": inpos,
                          "sharpe": d.mean() / d.std() * np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr / -dd if dd < 0 else np.nan})
    def held(sig, h):
        # long 1x for h bars after a signal bar, per coin-window
        pos = np.zeros(len(B))
        for (c, w), idx in B.groupby(["coin", "w"]).groups.items():
            idx = np.array(sorted(idx)); s = sig.values[idx]; p = np.zeros(len(idx)); left = 0
            for k in range(len(idx)):
                if s[k]: left = h
                p[k] = 1.0 if left > 0 else 0.0
                left -= 1
            pos[idx] = p
        return pd.Series(pos)
    q60 = B["ratio"].quantile(0.6); q80 = B["ratio"].quantile(0.8)
    up = B["ret20"] > 0
    out["books"] = pd.DataFrame({
        "wide60_long_h5": book(held(B.ratio > q60, 5)),
        "wide80_long_h5": book(held(B.ratio > q80, 5)),
        "wide80_long_h10": book(held(B.ratio > q80, 10)),
        "wide60_up_long_h5": book(held((B.ratio > q60) & up, 5)),
        "wide80_up_long_h10": book(held((B.ratio > q80) & up, 10)),
        "narrow_up_long_h5": book(held((B.ratio <= q60) & up, 5)),
        "hold": book(pd.Series(np.ones(len(B)))),
    }).T
    return out

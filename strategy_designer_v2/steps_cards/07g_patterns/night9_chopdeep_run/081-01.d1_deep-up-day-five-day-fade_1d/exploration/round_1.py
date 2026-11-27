def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi20 = c.rolling(20, min_periods=20).max()
            sd20 = r1.rolling(20, min_periods=20).std()
            depth = (c / hi20 - 1) / sd20
            tr = c / c.shift(60) - 1 if len(c) > 60 else pd.Series(np.nan, index=c.index)
            rng = (b["high"] - b["low"]) / c
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"])
            vol = b["volume"].astype(float)
            volr = vol / vol.rolling(20, min_periods=10).mean()
            n = len(c)
            for h in (1, 5):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                d = pd.DataFrame({
                    "coin": coin, "win": w, "h": h, "pos": idx,
                    "ts": b["timestamp"].values[idx],
                    "r1": r1.values[idx], "depth": depth.values[idx],
                    "trend": tr.values[idx] if hasattr(tr, "values") else np.nan,
                    "rng": rng.values[idx], "clpos": clpos.values[idx],
                    "volr": volr.values[idx], "sd20": sd20.values[idx],
                    "fwd": fwd.values[idx],
                    "alloc": b["postRebalance_current_allocation"].values[idx],
                })
                rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["fwd"])
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["unus"] = D["fwd"] - D["drift"]
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["wd"] = pd.to_datetime(D["ts"]).dt.dayofweek

    def clt(s, days):
        g = pd.DataFrame({"v": s - s.mean(), "d": days}).groupby("d")["v"].sum()
        G = len(g)
        if G < 3: return np.nan, G
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return s.mean() / se, G

    def summ(df, by):
        out = []
        for k, g in df.groupby(by, observed=True):
            g = g.dropna(subset=["unus"])
            t, G = clt(g["unus"], g["day"])
            out.append({"grp": str(k), "n": len(g), "days": G, "mean_fwd": g["fwd"].mean(),
                        "mean_unus": g["unus"].mean(), "t": t})
        return pd.DataFrame(out)

    res = {}
    D["up"] = np.where(D["r1"] > 0, "up", "down")
    D["dq"] = pd.qcut(D["depth"], 5, labels=False, duplicates="drop")
    D["tr3"] = pd.cut(D["trend"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    for h in (1, 5):
        S = D[D.h == h]
        res[f"h{h}_up_x_depthq"] = summ(S, ["up", "dq"])
        res[f"h{h}_up_x_trend"] = summ(S, ["up", "tr3"])
        res[f"h{h}_up_deep_x_trend"] = summ(S[S.dq <= 1], ["up", "tr3"])
        S2 = S.copy(); S2["r1q"] = pd.qcut(S2["r1"] / S2["sd20"], 5, labels=False, duplicates="drop")
        res[f"h{h}_r1z_q"] = summ(S2, ["r1q"])
        S2["clq"] = pd.qcut(S2["clpos"], 4, labels=False, duplicates="drop")
        res[f"h{h}_clpos_q_deep"] = summ(S2[S2.dq <= 1], ["clq"])
        S2["vq"] = pd.qcut(S2["volr"], 4, labels=False, duplicates="drop")
        res[f"h{h}_volr_q_updeep"] = summ(S2[(S2.dq <= 1) & (S2.up == "up")], ["vq"])
    S = D[D.h == 1]
    res["h1_weekday"] = summ(S, ["wd"])
    res["h5_year"] = summ(D[D.h == 5].assign(yr=pd.to_datetime(D["ts"]).dt.year), ["yr"])
    # book: daily returns by window and side share
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, win=w))
    B = pd.concat(bk)
    res["book_by_window"] = B.groupby("win").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "count"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    res["trades"] = T.groupby(pd.cut(T["dur_d"], [0, 5, 6, 10, 30, 1000])).agg(n=("net_profit_loss_percent", "count"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"))
    return res

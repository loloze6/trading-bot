def explore(data):
    import numpy as np, pandas as pd
    rows = []; ev = []; dd = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            ph = h.shift(1).rolling(480).max(); pl = l.shift(1).rolling(480).min()
            a24 = (c / c.shift(24) - 1).abs().rolling(720, min_periods=240).mean()
            r24 = c / c.shift(24) - 1
            vol = (c.pct_change()).rolling(720, min_periods=240).std()
            f120 = c.shift(-120) / c - 1; f240 = c.shift(-240) / c - 1
            f24 = c.shift(-24) / c - 1
            above = (c > ph)
            first = above & ~above.shift(1, fill_value=False)
            # hours since the current above-streak began
            grp = (~above).cumsum()
            streak = above.groupby(grp).cumsum()
            df = pd.DataFrame({"coin": coin, "w": w, "dist": (c/ph-1)/a24, "dlow": (c/pl-1)/a24,
                               "r24s": r24/a24, "vol": vol, "f120": f120, "f240": f240,
                               "streak": streak, "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday, "f24": f24})
            grid = df.iloc[::120].copy()
            rows.append(grid)
            e = df[first].copy(); ev.append(e)
    G = pd.concat(rows); E = pd.concat(ev)
    G = G.dropna(subset=["f120", "dist"])
    st = G.groupby("coin")["f120"].agg(["mean", "std"])
    G["u"] = G["f120"] - G["coin"].map(st["mean"]); G["s"] = G["u"] / G["coin"].map(st["std"])
    E = E.dropna(subset=["f120", "dist"])
    E["u"] = E["f120"] - E["coin"].map(st["mean"]); E["s"] = E["u"]/E["coin"].map(st["std"])
    def summ(df, key, col="u"):
        x = df.groupby(key, observed=True)[col].agg(["mean", "std", "count"])
        x["t"] = x["mean"] / (x["std"] / np.sqrt(x["count"]))
        return x.drop(columns="std")
    out = {}
    G["distbin"] = pd.cut(G["dist"], [-99, -6, -3, -1.5, -0.5, 0, 0.5, 1, 2, 99])
    out["grid: 120h unusual by scaled distance to 20d high"] = summ(G, "distbin")
    G["lowbin"] = pd.cut(G["dlow"], [-99, -1, 0, 0.5, 1.5, 3, 6, 99])
    out["grid: 120h unusual by scaled distance to 20d low"] = summ(G, "lowbin")
    G["r24bin"] = pd.cut(G["r24s"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    out["grid: 120h unusual by 24h return in usual daily moves"] = summ(G, "r24bin")
    G["vq"] = G.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    Gb = G[G["dist"] > 0]
    out["grid breakouts: by vol tercile"] = summ(Gb, "vq")
    out["grid breakouts: 240h vs 120h unusual"] = pd.Series({"u120": Gb["u"].mean(), "f240_raw": Gb["f240"].mean(),
        "drift240_approx": 2*st["mean"].mean(), "n": len(Gb)})
    out["grid breakouts: by coin"] = summ(Gb, "coin")
    out["grid all: by vol tercile"] = summ(G, "vq")
    E["sbin"] = pd.cut(E["dist"], [0, 0.1, 0.3, 0.6, 99])
    out["first-break events: by break size"] = summ(E, "sbin")
    E["hb"] = (E["hour"] // 4) * 4
    out["first-break events: by UTC hour block"] = summ(E, "hb")
    out["first-break events: by weekday"] = summ(E, "wd")
    out["first-break events: 24h raw fwd"] = pd.Series({"f24": E["f24"].mean(), "t": E["f24"].mean()/(E["f24"].std()/np.sqrt(E["f24"].count())), "n": E["f24"].count()})
    G["stb"] = pd.cut(G["streak"], [0.5, 24, 72, 168, 1e6])
    out["grid: by hours since breakout streak began"] = summ(G.dropna(subset=["stb"]), "stb")
    return out

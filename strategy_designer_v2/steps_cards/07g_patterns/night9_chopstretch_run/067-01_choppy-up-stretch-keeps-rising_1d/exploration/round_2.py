def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            s20 = r.rolling(20).std()
            sma = c.rolling(20).mean()
            z = (c - sma) / sma / s20
            r60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(len(b)), "z": z,
                               "r60": r60, "vol30": vol30, "ts": b["timestamp"].astype(str),
                               "chop": (b["regime"] != "chop").astype(int)})
            for h in [5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in [5, 10]:
        g = A[A["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(dr)
        A[f"u{h}"] = A["coin"].map(g.groupby("coin")[f"f{h}"].std())
    A["trend"] = np.where(A["r60"] > 0.10, "rising", np.where(A["r60"] < -0.10, "falling",
                  np.where(A["r60"].notna(), "choppy", "unk")))
    A["agit"] = A.groupby("coin")["vol30"].transform(lambda s: np.where(s > s.median(), "agit", "calm"))
    A.loc[A["vol30"].isna(), "agit"] = "unk"

    def clus_slope(g, h):
        g = g.dropna(subset=["z", f"x{h}"])
        if len(g) < 30:
            return pd.Series({"n": len(g)})
        x = g["z"].clip(-6, 6).values; y = (g[f"x{h}"] / g[f"u{h}"]).values
        xm = x - x.mean(); beta = (xm * y).sum() / (xm ** 2).sum()
        e = y - y.mean() - beta * xm
        sc = pd.Series(xm * e).groupby(g["ts"].values).sum()
        G = len(sc); se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (xm ** 2).sum()
        up = g[g["z"] > 0]; dn = g[g["z"] < 0]
        top = g[g["z"] > 1.5]; bot = g[g["z"] < -1.5]
        return pd.Series({"n": len(g), "dates": G, "slope_per_usual": beta, "t": beta / se,
                          "long_dir_x": up[f"x{h}"].mean(), "short_dir_x": -dn[f"x{h}"].mean(),
                          "top_x": top[f"x{h}"].mean(), "n_top": len(top),
                          "bot_dir_x": -bot[f"x{h}"].mean(), "n_bot": len(bot)})

    for h in [5, 10]:
        G = A[A["pos"] % h == 0]
        res = {}
        for k, gg in G.groupby("trend"): res[k] = clus_slope(gg, h)
        for k, gg in G[G["trend"].isin(["rising", "falling"])].groupby(["trend", "agit"]):
            res[k[0] + "_" + k[1]] = clus_slope(gg, h)
        res["nonchop_regime"] = clus_slope(G[G["chop"] == 0], h)
        res["chop_regime"] = clus_slope(G[G["chop"] == 1], h)
        res["nonchop_w7_12"] = clus_slope(G[(G["chop"] == 0) & (G["wn"] <= 12)], h)
        res["nonchop_w13_18"] = clus_slope(G[(G["chop"] == 0) & (G["wn"] > 12)], h)
        res["all"] = clus_slope(G, h)
        out[f"slope_h{h}"] = pd.DataFrame(res).T.round(4)
    # per coin, non-chop, h10
    G = A[(A["pos"] % 10 == 0) & (A["chop"] == 0)]
    out["nonchop_h10_by_coin"] = pd.DataFrame({k: clus_slope(gg, 10) for k, gg in G.groupby("coin")}).T.round(4)
    out["share_trend_known"] = A["trend"].value_counts(normalize=True).round(3)
    return out

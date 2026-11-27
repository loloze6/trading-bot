def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            f = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"].astype(str).str[:10]})
            f["pos"] = np.arange(len(b))
            rng = (h - l).replace(0, np.nan)
            f["loc"] = (c - l) / rng
            f["r1"] = c.pct_change()
            f["r5"] = c / c.shift(5) - 1
            f["r20"] = c / c.shift(20) - 1
            f["r60"] = c / c.shift(60) - 1
            f["vol30"] = c.pct_change().rolling(30).std()
            f["rngpct"] = (h - l) / c
            for hh in (1, 2, 5):
                f[f"fw{hh}"] = c.shift(-hh) / c - 1
            f["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            f["year"] = pd.to_datetime(b["timestamp"]).dt.year
            f["fc"] = b["forecast"]; f["alloc"] = b["postRebalance_current_allocation"]
            rows.append(f)
    D = pd.concat(rows, ignore_index=True)
    # agitation proxy: 30d vol vs coin's median of vol30 over all windows
    D["agit"] = D["vol30"] > D.groupby("coin")["vol30"].transform("median")
    D["trend"] = np.where(D["r60"] > 0.10, "rising", np.where(D["r60"] < -0.10, "falling", np.where(D["r60"].notna(), "choppy", None)))

    def stat(sub, col, drift):
        x = (sub[col] - sub["coin"].map(drift)).dropna()
        s = sub.loc[x.index]
        n = len(x)
        if n < 10: return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "days": 0})
        m = x.mean()
        S = (x - m).groupby(s["ts"]).sum()
        G = len(S)
        se = np.sqrt(G / (G - 1) * (S ** 2).sum()) / n if G > 1 else np.nan
        return pd.Series({"n": n, "mean": m, "t": m / se, "days": G})

    out = {}
    for hh in (2, 5):
        G = D[D["pos"] % hh == 0].copy()
        drift = G.groupby("coin")[f"fw{hh}"].mean()
        col = f"fw{hh}"
        G["locq"] = pd.cut(G["loc"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
        G["r20q"] = pd.cut(G["r20"], [-9, -.2, -.1, -.03, .03, .1, .2, 9])
        G["r1q"] = pd.cut(G["r1"], [-9, -.08, -.04, -.01, .01, .04, .08, 9])
        out[f"h{hh} by trend x agit"] = G.groupby(["trend", "agit"]).apply(lambda s: stat(s, col, drift))
        if hh == 2:
            ca = G[(G.trend == "choppy") & G.agit]
            out["h2 choppy agit by loc"] = ca.groupby("locq").apply(lambda s: stat(s, col, drift))
            cc = G[(G.trend == "choppy") & ~G.agit]
            out["h2 choppy calm by loc"] = cc.groupby("locq").apply(lambda s: stat(s, col, drift))
            out["h2 all by r1"] = G.groupby("r1q").apply(lambda s: stat(s, col, drift))
            out["h2 agit by r1"] = G[G.agit].groupby("r1q").apply(lambda s: stat(s, col, drift))
        if hh == 5:
            out["h5 all by r20"] = G.groupby("r20q").apply(lambda s: stat(s, col, drift))
            out["h5 choppy by r20"] = G[G.trend == "choppy"].groupby("r20q").apply(lambda s: stat(s, col, drift))
            out["h5 falling agit by loc"] = G[(G.trend == "falling") & G.agit].groupby("locq").apply(lambda s: stat(s, col, drift))
    G1 = D.copy(); drift1 = G1.groupby("coin")["fw1"].mean()
    out["h1 by weekday"] = G1.groupby("wd").apply(lambda s: stat(s, "fw1", drift1))
    # book: days in position, by year
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd)
    out["book ret by window"] = DD.groupby("win")["book_return"].agg(["count", "mean", "sum"])
    act = D[D["alloc"].fillna(0) != 0]
    out["active bars by coin"] = act.groupby("coin").size()
    return out

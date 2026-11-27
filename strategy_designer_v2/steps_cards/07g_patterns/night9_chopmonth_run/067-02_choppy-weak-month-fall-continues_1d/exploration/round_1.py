def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            d["r1"] = c.pct_change()
            d["ret30"] = c / c.shift(30) - 1
            d["ret7p"] = c / c.shift(7) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["f7"] = c.shift(-7) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            d["choppy"] = (d["regime"] == "unknown")
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["rng"] = (d["high"] - d["low"]) / d["close"]
            d["clv"] = (d["close"] - d["low"]) / (d["high"] - d["low"]).replace(0, np.nan)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    g7 = A[A["pos"] % 7 == 0].copy()
    m7 = g7.groupby("coin")["f7"].mean()
    g7["u7"] = g7["f7"] - g7["coin"].map(m7)
    sd7 = g7.groupby("coin")["f7"].std()
    g7["z7"] = g7["u7"] / g7["coin"].map(sd7)
    out = {}
    def tday(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna().groupby("d")["v"].sum()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    def tab(df, key, val="u7"):
        r = []
        for k, sub in df.groupby(key):
            sub = sub.dropna(subset=[val])
            r.append({"grp": k, "n": len(sub), "mean": sub[val].mean(), "t_day": tday(sub[val], sub["day"]), "days": sub["day"].nunique()})
        return pd.DataFrame(r)
    G = g7.dropna(subset=["ret30", "u7"]).copy()
    G["z30"] = G["ret30"] / (G["vol20"] * np.sqrt(30))
    G["q30"] = pd.qcut(G["z30"], 5, labels=False)
    out["chop_by_ret30_quint"] = tab(G[G.choppy], "q30")
    out["notchop_by_ret30_quint"] = tab(G[~G.choppy], "q30")
    out["chop_corr"] = pd.Series({"spearman_ret30_u7_chop": stats.spearmanr(G[G.choppy].z30, G[G.choppy].u7)[0],
                                  "spearman_ret30_u7_notchop": stats.spearmanr(G[~G.choppy].z30, G[~G.choppy].u7)[0],
                                  "n_chop": int(G.choppy.sum()), "n_not": int((~G.choppy).sum())})
    G["q7p"] = pd.qcut(G["ret7p"] / (G["vol20"] * np.sqrt(7)), 5, labels=False)
    out["all_by_past7_quint"] = tab(G, "q7p")
    G["qv"] = pd.qcut(G["vol20"] / G.groupby("coin")["vol20"].transform("median"), 3, labels=False)
    out["all_by_vol_tercile"] = tab(G, "qv")
    # daily: big moves
    D = A.dropna(subset=["r1", "vol20", "f1"]).copy()
    mf1 = D.groupby("coin")["f1"].mean()
    D["u1"] = D["f1"] - D["coin"].map(mf1)
    D["zr"] = D["r1"] / D["vol20"].shift(0)
    D["qz"] = pd.cut(D["zr"], [-99, -2, -1, 0, 1, 2, 99])
    out["next_day_by_today_z"] = tab(D, "qz", "u1")
    out["next_day_by_weekday"] = tab(D, "wd", "u1")
    D["qclv"] = pd.qcut(D["clv"], 5, labels=False, duplicates="drop")
    out["next_day_by_closeloc"] = tab(D, "qclv", "u1")
    # book days
    dd = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            x = df.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    B = pd.concat(dd).dropna(subset=["book_return"])
    bb = B.groupby("day")["book_return"].mean()
    out["book_by_window"] = B.groupby("win").apply(lambda x: x.groupby("day")["book_return"].mean().mean()*1e4).rename("bp_day")
    tr = []
    for coin, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): x = df.copy(); x["coin"] = coin; tr.append(x)
    T = pd.concat(tr)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean"])
    return out

def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            d["r1"] = c.pct_change()
            d["ret30"] = c / c.shift(30) - 1
            d["ret14"] = c / c.shift(14) - 1
            d["ret60"] = c / c.shift(60) - 1
            d["vol30"] = d["r1"].rolling(30).std()
            d["f7"] = c.shift(-7) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            d["choppy"] = (d["regime"] == "unknown")
            ts = pd.to_datetime(d["timestamp"])
            d["year"] = ts.dt.year
            d["day"] = ts.dt.floor("D")
            d["clv"] = (d["close"] - d["low"]) / (d["high"] - d["low"]).replace(0, np.nan)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["agit"] = A["vol30"] > A.groupby("coin")["vol30"].transform("median")
    def tday(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna().groupby("d")["v"].sum()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    out = {}
    g7 = A[A["pos"] % 7 == 0].copy()
    m7 = g7.groupby("coin")["f7"].mean(); sd7 = g7.groupby("coin")["f7"].std()
    g7["u7"] = g7["f7"] - g7["coin"].map(m7)
    g7["s30"] = g7["ret30"] / (g7["vol30"] * np.sqrt(30))
    G = g7.dropna(subset=["s30", "u7"]).copy()
    G["sig"] = np.sign(G["s30"])
    G["dirmove"] = G["sig"] * G["u7"]
    G["w_dirmove"] = G["s30"] * G["u7"]  # graded signal x unusual move
    def summ(df, key):
        r = []
        for k, sub in df.groupby(key):
            r.append({"grp": str(k), "n": len(sub), "days": sub["day"].nunique(),
                      "dir_mean": sub["dirmove"].mean(), "t_dir": tday(sub["dirmove"], sub["day"]),
                      "graded_mean": sub["w_dirmove"].mean(), "t_graded": tday(sub["w_dirmove"], sub["day"]),
                      "spear": stats.spearmanr(sub["s30"], sub["u7"])[0] if len(sub) > 10 else np.nan})
        return pd.DataFrame(r)
    C = G[G.choppy].copy()
    out["chop_by_side"] = summ(C, "sig")
    out["chop_by_agit"] = summ(C, "agit")
    out["chop_by_year"] = summ(C, "year")
    out["chop_by_window"] = summ(C, "win")
    out["notchop_all"] = summ(G[~G.choppy], "agit")
    # 14-day lookback variant in choppy
    C2 = C.dropna(subset=["ret14"]).copy()
    C2["s14"] = C2["ret14"] / (C2["vol30"] * np.sqrt(14))
    C2["g14"] = C2["s14"] * C2["u7"]
    out["chop_14d_graded"] = pd.Series({"mean": C2["g14"].mean(), "t": tday(C2["g14"], C2["day"]),
                                        "spear": stats.spearmanr(C2["s14"], C2["u7"])[0], "n": len(C2)})
    # 3-day grid in choppy, month signal
    g3 = A[A["pos"] % 3 == 0].copy()
    g3["u3"] = g3["f3"] - g3["coin"].map(g3.groupby("coin")["f3"].mean())
    g3["s30"] = g3["ret30"] / (g3["vol30"] * np.sqrt(30))
    H = g3[g3.choppy].dropna(subset=["s30", "u3"])
    H = H.assign(gg=H["s30"] * H["u3"])
    out["chop_3d_graded"] = pd.Series({"mean": H["gg"].mean(), "t": tday(H["gg"], H["day"]),
                                       "spear": stats.spearmanr(H["s30"], H["u3"])[0], "n": len(H), "days": H["day"].nunique()})
    # close location next day, by agitation and choppy
    D = A.dropna(subset=["clv", "f1", "vol30"]).copy()
    D["u1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["cl"] = (0.5 - D["clv"]) * D["u1"]
    r = []
    for k, sub in D.groupby(["choppy", "agit"]):
        r.append({"grp": str(k), "n": len(sub), "graded_mean_bp": sub["cl"].mean()*1e4, "t": tday(sub["cl"], sub["day"])})
    out["closeloc_next_day_by_chop_agit"] = pd.DataFrame(r)
    return out

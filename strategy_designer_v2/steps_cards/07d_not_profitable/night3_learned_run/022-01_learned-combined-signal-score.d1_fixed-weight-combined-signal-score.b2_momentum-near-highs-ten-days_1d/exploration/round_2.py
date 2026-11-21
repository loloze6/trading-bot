def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            a = b["postRebalance_current_allocation"].astype(float)
            r1 = c.shift(-1) / c - 1
            r10 = c.shift(-10) / c - 1
            lr = np.log(c).diff()
            vol30 = lr.rolling(30, min_periods=20).std()
            vol90 = lr.rolling(90, min_periods=40).std()
            ret28 = c / c.shift(28) - 1
            ret7 = c / c.shift(7) - 1
            dd90 = c / c.rolling(90, min_periods=20).max() - 1
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)), "a": a, "r1": r1, "r10": r10,
                               "fc": b["forecast"].astype(float), "volratio": vol30 / vol90,
                               "ret28": ret28, "ret7": ret7, "dd90": dd90,
                               "chg": (a - b["previous_allocation"].astype(float)).abs()})
            rows.append(df)
    B = pd.concat(rows, ignore_index=True)
    mu1 = B.dropna(subset=["r1"]).groupby("coin")["r1"].mean()
    G = B[B["i"] % 10 == 0].dropna(subset=["r10", "fc"]).copy()
    mu10 = G.groupby("coin")["r10"].mean()
    G["ex10"] = G["r10"] - G["coin"].map(mu10)
    G["fcd"] = pd.qcut(G["fc"], 10, labels=False, duplicates="drop")
    out["grid_ex10_by_fc_decile"] = G.groupby("fcd").agg(n=("ex10", "size"), fc=("fc", "mean"),
        ex10_pct=("ex10", lambda x: x.mean() * 100),
        t=("ex10", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    B = B.dropna(subset=["r1", "a"]).copy()
    B["mu"] = B["coin"].map(mu1)
    B["g"] = B["a"] * B["r1"]
    B["tim"] = B["a"] * (B["r1"] - B["mu"])
    def agg(x):
        return pd.Series({"n": len(x), "mean_a": x["a"].mean(), "gain_bps": x["g"].mean() * 1e4,
                          "timing_bps": x["tim"].mean() * 1e4,
                          "t_gain": x["g"].mean() / (x["g"].std() / np.sqrt(len(x))),
                          "turnover_bps": x["chg"].mean() * 1e4})
    S = B[B.a < 0].copy()
    S["ddq"] = pd.qcut(S["dd90"], 4, labels=False, duplicates="drop")
    out["short_by_dd90_quartile"] = S.groupby("ddq").apply(agg).join(S.groupby("ddq")["dd90"].mean())
    S["r7q"] = pd.qcut(S["ret7"], 4, labels=False, duplicates="drop")
    out["short_by_ret7_quartile"] = S.groupby("r7q").apply(agg).join(S.groupby("r7q")["ret7"].mean())
    L = B[B.a > 0].copy()
    L["r28q"] = pd.qcut(L["ret28"], 4, labels=False, duplicates="drop")
    out["long_by_ret28_quartile"] = L.groupby("r28q").apply(agg).join(L.groupby("r28q")["ret28"].mean())
    L["vrq"] = pd.qcut(L["volratio"], 3, labels=False, duplicates="drop")
    out["long_by_volratio"] = L.groupby("vrq").apply(agg)
    L["ddq"] = pd.qcut(L["dd90"].rank(method="first"), 4, labels=False)
    out["long_by_dd90_quartile"] = L.groupby("ddq").apply(agg).join(L.groupby("ddq")["dd90"].mean())
    out["mean_daily_turnover_bps"] = B["chg"].mean() * 1e4
    # book if shorts were flat: approx bar gain mean long only per coin-bar
    out["gain_all_bps"] = B["g"].mean() * 1e4
    out["gain_long_only_bps"] = (B["g"] * (B["a"] > 0)).mean() * 1e4
    return out

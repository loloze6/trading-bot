def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 20:
                continue
            c = b["close"]
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "cloc": (c - b["low"]) / rng,
                "ret5": c / c.shift(5) - 1,
                "ret1": c / c.shift(1) - 1,
                "ret60": c / c.shift(60) - 1,
                "fwd5": c.shift(-5) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "inprof": (b["regime"] != "chop"),
                "pos": np.arange(len(b)),
            })
            d["vol20"] = d["ret1"].rolling(20, min_periods=10).std().shift(1)
            d["z1"] = d["ret1"] / d["vol20"]
            d["z5"] = d["ret5"] / (d["vol20"] * np.sqrt(5))
            rows.append(d)
    P = pd.concat(rows, ignore_index=True)
    P["day"] = P["ts"].dt.floor("D")
    P["year"] = P["ts"].dt.year
    for h in (1, 2, 5):
        g = P[P.pos % h == 0]
        dr = g.groupby("coin")["fwd%d" % h].mean()
        P["u%d" % h] = P["fwd%d" % h] - P["coin"].map(dr)
    P["tr"] = pd.cut(P["ret60"], [-10, -0.1, 0.1, 10], labels=["falling", "choppy", "rising"]).astype(str)
    P.loc[P.inprof, "tr"] = "chopagi"

    def st(df, col):
        df = df.dropna(subset=[col])
        if len(df) < 3:
            return pd.Series({"n": len(df), "mean": np.nan, "t": np.nan, "days": 0})
        dev = df[col] - df[col].mean()
        s = dev.groupby(df["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(df)
        return pd.Series({"n": len(df), "mean": df[col].mean(), "t": df[col].mean() / se if se > 0 else np.nan, "days": G})
    out = {}
    G5 = P[P.pos % 5 == 0].copy(); G2 = P[P.pos % 2 == 0].copy(); G1 = P.copy()
    zb = [-99, -2, -1, 0, 1, 2, 3, 99]
    for nm, G, col in (("z1_u1", G1, "u1"), ("z1_u2", G2, "u2"), ("z1_u5", G5, "u5")):
        G["z1q"] = pd.cut(G["z1"], zb)
        out["A_" + nm] = G.groupby("z1q").apply(lambda x: st(x, col)).round(4)
    G5["z1q"] = pd.cut(G5["z1"], [-99, 1, 2, 99])
    out["B_z1_tr_u5"] = G5.groupby(["tr", "z1q"]).apply(lambda x: st(x, "u5")).round(4)
    big = G5[G5.z1 > 2]
    out["C_big_up_by_year_u5"] = big.groupby("year").apply(lambda x: st(x, "u5")).round(4)
    out["C2_big_up_by_cloc_u5"] = big.groupby(pd.cut(big["cloc"], [-0.01, 0.5, 0.8, 1.01])).apply(lambda x: st(x, "u5")).round(4)
    # high close after 5d fall, outside profile, 2-day
    G2["clq"] = pd.cut(G2["cloc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1", "q2", "q3", "q4"])
    f = G2[G2.ret5 < 0]
    out["D_fall5_tr_cloc_u2"] = f.groupby(["tr", "clq"]).apply(lambda x: st(x, "u2")).round(4)
    f4 = f[(f.clq == "q4") & (~f.inprof)].copy()
    f4["z5q"] = pd.qcut(f4["z5"], 3, labels=["deep", "mid", "shallow"])
    out["E_q4fall_out_z5_u2"] = f4.groupby("z5q").apply(lambda x: st(x, "u2")).round(4)
    out["E2_q4fall_out_year_u2"] = f4.groupby("year").apply(lambda x: st(x, "u2")).round(4)
    out["E3_q4fall_out_coin_u2"] = f4.groupby("coin").apply(lambda x: st(x, "u2")).round(4)
    out["F_inprof_all_u5"] = st(G5[G5.inprof], "u5").round(4)
    return out

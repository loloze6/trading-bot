def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            sd30 = r1.rolling(30).std()
            sd90 = r1.rolling(90, min_periods=60).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "r7": r7, "r30": r30,
                "z7": r7 / (sd30 * np.sqrt(7)), "z30": r30 / (sd30 * np.sqrt(30)), "sd30": sd30,
                "volratio": sd30 / sd90, "f7": c.shift(-7) / c - 1, "day": ts.dt.floor("D"), "year": ts.dt.year}))
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 7 == 0].dropna(subset=["f7", "z7", "er", "z30"]).copy()
    G["raw"] = G["f7"] - G["coin"].map(G.groupby("coin")["f7"].mean())
    G["chop"] = G["er"] <= 0.3
    G["agree"] = np.sign(G["r7"]) == np.sign(G["r30"])
    G["volq"] = G.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def ct(x, day):
        d = pd.DataFrame({"x": x, "day": day}).dropna()
        m = d["x"].mean(); s = (d["x"] - m).groupby(d["day"]).sum(); g = len(s)
        se = np.sqrt((s ** 2).sum() * g / (g - 1)) / len(d)
        return pd.Series({"n": len(d), "days": g, "mean": m, "t": m / se})
    out = {}
    # 1: in chop, sign by 30d move, graded by |z30|
    C = G[G["chop"]].copy()
    C["u30"] = C["raw"] * np.sign(C["r30"])
    C["z30q"] = pd.qcut(C["z30"].abs(), 3, labels=False)
    out["chop_signed30_by_absz30"] = C.groupby("z30q").apply(lambda g: ct(g["u30"], g["day"]))
    out["chop_signed30_by_agree"] = C.groupby("agree").apply(lambda g: ct(g["u30"], g["day"]))
    out["chop_signed30_by_year"] = C.groupby("year").apply(lambda g: ct(g["u30"], g["day"]))
    # regression slope of raw on z30 in chop
    out["chop_corr_raw_z30"] = float(np.corrcoef(C["raw"], C["z30"])[0, 1])
    out["chop_corr_raw_z7"] = float(np.corrcoef(C["raw"], C["z7"])[0, 1])
    # 2: up vs down in chop_agree
    CA = C[C["agree"]].copy()
    CA["u7"] = CA["raw"] * np.sign(CA["r7"])
    out["chop_agree_by_side"] = CA.groupby(np.sign(CA["r7"])).apply(lambda g: ct(g["u7"], g["day"]))
    # 3: trending (er>0.3) agree, high vol: reversal graded by |z7|?
    T = G[~G["chop"]].copy()
    T["u7"] = T["raw"] * np.sign(T["r7"])
    T["rev7"] = -T["u7"]
    out["trend_by_volq"] = T.groupby("volq").apply(lambda g: ct(g["rev7"], g["day"]))
    TH = T[T["volq"] == 2].copy()
    TH["zq"] = pd.qcut(TH["z7"].abs(), 3, labels=False)
    out["trend_highvol_rev_by_absz7"] = TH.groupby("zq").apply(lambda g: ct(g["rev7"], g["day"]))
    out["trend_highvol_rev_by_side"] = TH.groupby(np.sign(TH["r30"])).apply(lambda g: ct(g["rev7"], g["day"]))
    T["erq"] = pd.qcut(T["er"], 3, labels=False)
    out["trend_rev_by_er_tercile"] = T.groupby("erq").apply(lambda g: ct(g["rev7"], g["day"]))
    # 4: overall: reversal of 30d move when er high, graded by er
    G["u30"] = G["raw"] * np.sign(G["r30"])
    G["erq5"] = pd.qcut(G["er"], 5, labels=False)
    out["all_signed30_by_er_quintile"] = G.groupby("erq5").apply(lambda g: ct(g["u30"], g["day"]))
    G["vrq"] = pd.qcut(G["volratio"], 3, labels=False)
    out["chopagree_by_volratio"] = G[G["chop"] & G["agree"]].assign(u7=lambda d: d["raw"] * np.sign(d["r7"])).groupby("vrq").apply(lambda g: ct(g["u7"], g["day"]))
    return out

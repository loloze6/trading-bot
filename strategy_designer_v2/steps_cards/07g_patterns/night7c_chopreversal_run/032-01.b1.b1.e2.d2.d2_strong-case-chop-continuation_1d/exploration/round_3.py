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
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "r7": r7, "r30": r30,
                "z7": r7 / (sd30 * np.sqrt(7)), "sd30": sd30, "day": ts.dt.floor("D"), "year": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float), "r1n": r1.shift(-1)})
            for h in (3, 7, 14, 21):
                d["f%d" % h] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["volq"] = A.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def ct(x, day):
        d = pd.DataFrame({"x": x, "day": day}).dropna()
        if len(d) < 3: return pd.Series({"n": len(d), "days": 0, "mean": np.nan, "t": np.nan})
        m = d["x"].mean(); s = (d["x"] - m).groupby(d["day"]).sum(); g = len(s)
        se = np.sqrt((s ** 2).sum() * g / (g - 1)) / len(d)
        return pd.Series({"n": len(d), "days": g, "mean": m, "t": m / se})
    out = {}
    hz = []
    for h in (3, 7, 14, 21):
        G = A[A["pos"] % h == 0].dropna(subset=["f%d" % h, "z7", "er"]).copy()
        G["raw"] = G["f%d" % h] - G["coin"].map(G.groupby("coin")["f%d" % h].mean())
        G["u7"] = G["raw"] * np.sign(G["r7"])
        ca = G[(G["er"] <= 0.3) & (np.sign(G["r7"]) == np.sign(G["r30"]))]
        r = ct(ca["u7"], ca["day"]); r["h"] = h; r["regime"] = "chop_agree"; hz.append(r)
        tr = G[(G["er"] > 0.3) & (G["volq"] == 2)]
        r = ct(-tr["u7"], tr["day"]); r["h"] = h; r["regime"] = "trend_highvol_rev"; hz.append(r)
        if h == 7:
            ca = ca.copy(); ca["zq"] = pd.qcut(ca["z7"].abs(), 3, labels=False)
            out["chop_agree_absz7_clustered"] = ca.groupby("zq").apply(lambda g: ct(g["u7"], g["day"]))
            out["chop_agree_top_z7_by_year"] = ca[ca["zq"] == 2].groupby("year").apply(lambda g: ct(g["u7"], g["day"]))
            tr = G[G["er"] > 0.3].copy()
            out["trend_rev_by_volq_by_year"] = tr[tr["volq"] == 2].groupby("year").apply(lambda g: ct(-g["u7"], g["day"]))
    out["by_horizon"] = pd.DataFrame(hz).set_index(["regime", "h"])
    # book: long vs short bar gains, by year
    A["gain"] = A["alloc"] * A["r1n"]
    A["side"] = np.sign(A["alloc"])
    out["bar_gain_by_side_year"] = A[A["side"] != 0].groupby(["side", "year"])["gain"].agg(["count", "mean"])
    return out

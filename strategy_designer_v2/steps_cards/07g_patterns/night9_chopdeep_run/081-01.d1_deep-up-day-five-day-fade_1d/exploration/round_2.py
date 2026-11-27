def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi20 = c.rolling(20, min_periods=20).max()
            sd20 = r1.rolling(20, min_periods=20).std()
            depth = (c / hi20 - 1) / sd20
            tr = c / c.shift(60) - 1
            sd30 = r1.rolling(30, min_periods=30).std()
            agit = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"])
            n = len(c)
            for h in (1, 2, 3, 5):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h,
                    "ts": b["timestamp"].values[idx], "r1": r1.values[idx],
                    "depth": depth.values[idx], "trend": tr.values[idx], "agit": agit.values[idx],
                    "clpos": clpos.values[idx], "fwd": fwd.values[idx]}))
    D = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "depth", "r1"])
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["unus"] = D["fwd"] - D["drift"]
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["yr"] = pd.to_datetime(D["ts"]).dt.year
    D["tr3"] = pd.cut(D["trend"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    D["ag"] = np.where(D["agit"] > 0.5, "agit", np.where(D["agit"].notna(), "calm", "na"))

    def clt(s, days):
        g = pd.DataFrame({"v": s - s.mean(), "d": days}).groupby("d")["v"].sum()
        G = len(g)
        if G < 3: return np.nan, G
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return s.mean() / se, G

    def summ(df, by):
        out = []
        for k, g in df.groupby(by, observed=True):
            t, G = clt(g["unus"], g["day"])
            out.append({"grp": str(k), "n": len(g), "days": G, "mean_fwd": g["fwd"].mean(),
                        "mean_unus": g["unus"].mean(), "t": t})
        return pd.DataFrame(out)

    def slope(df, x):
        # graded: day-clustered t of slope of unus on x
        d = df.dropna(subset=[x]); xx = d[x] - d[x].mean(); y = d["unus"] - d["unus"].mean()
        b = (xx * y).sum() / (xx ** 2).sum()
        e = (y - b * xx) * xx
        g = pd.DataFrame({"e": e, "d": d["day"]}).groupby("d")["e"].sum()
        G = len(g); se = np.sqrt((g ** 2).sum() * G / (G - 1)) / (xx ** 2).sum()
        return {"n": len(d), "days": G, "slope": b, "t": b / se}

    res = {}
    U = D[D.r1 > 0].copy()
    Dn = D[D.r1 <= 0].copy()
    sl = []
    for h in (1, 2, 3, 5):
        for nm, S in [("up_all", U), ("down_all", Dn), ("up_chop", U[U.tr3 == "chop"]), ("up_fall", U[U.tr3 == "fall"]),
                      ("up_rise", U[U.tr3 == "rise"]), ("up_chop_agit", U[(U.tr3 == "chop") & (U.ag == "agit")]),
                      ("up_chop_calm", U[(U.tr3 == "chop") & (U.ag == "calm")]), ("up_fall_agit", U[(U.tr3 == "fall") & (U.ag == "agit")]),
                      ("up_fall_calm", U[(U.tr3 == "fall") & (U.ag == "calm")])]:
            r = slope(S[S.h == h], "depth"); r.update({"set": nm, "h": h}); sl.append(r)
    res["slope_unus_on_depth"] = pd.DataFrame(sl)
    cp = []
    for h in (1, 2, 3, 5):
        for nm, S in [("up", U), ("up_deep", U[U.depth < U.depth.median()]), ("down", Dn)]:
            r = slope(S[S.h == h], "clpos"); r.update({"set": nm, "h": h}); cp.append(r)
    res["slope_unus_on_clpos"] = pd.DataFrame(cp)
    C = U[(U.tr3 == "chop")].copy()
    C["dq"] = pd.qcut(C["depth"], 3, labels=False)
    res["chop_up_depth_terciles_h1h5"] = summ(C[C.h.isin([1, 5])], ["h", "dq"])
    res["chop_up_deep_h5_by_yr"] = summ(C[(C.h == 5) & (C.dq == 0)], ["yr"])
    res["chop_up_deep_h1_by_yr"] = summ(C[(C.h == 1) & (C.dq == 0)], ["yr"])
    res["chop_up_deep_h5_by_coin"] = summ(C[(C.h == 5) & (C.dq <= 1)], ["coin"])
    F = U[(U.tr3 == "fall")].copy(); F["dq"] = pd.qcut(F["depth"], 3, labels=False)
    res["fall_up_depth_terciles_h1h3"] = summ(F[F.h.isin([1, 3])], ["h", "dq"])
    res["fall_up_deep_h1_by_yr"] = summ(F[(F.h == 1) & (F.dq == 0)], ["yr"])
    return res

def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "z1": r1 / sd30, "sd30": sd30,
                "z3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                "ret60": c / c.shift(60) - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "rising": (b["regime"] != "chop").values,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    A["trend"] = np.where(A["ret60"] > 0.10, "rising", np.where(A["ret60"] < -0.10, "falling", np.where(A["ret60"].notna(), "choppy", np.nan)))
    A["volq"] = A.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 2, labels=False))
    # 1) next-day rebound after a one-day fall: graded? by horizon, trend, vol
    res = {}
    for h in ["fwd1", "fwd2", "fwd3"]:
        # non-overlapping grid of size h
        hh = int(h[-1])
        s = A[(A["pos"] % hh == 0)].dropna(subset=[h, "z1"])
        dr = s.groupby("coin")[h].transform("mean")
        s = s.assign(ex=s[h] - dr)
        f = s[s["z1"] < 0]
        r = stats.linregress(f["z1"], f["ex"])
        res[f"{h} falls slope"] = pd.Series({"n": len(f), "slope": r.slope, "t": r.slope / r.stderr})
        u = s[s["z1"] > 0]
        r = stats.linregress(u["z1"], u["ex"])
        res[f"{h} rises slope"] = pd.Series({"n": len(u), "slope": r.slope, "t": r.slope / r.stderr})
    out["ex return on z1, by side and horizon"] = pd.DataFrame(res).T.round(5)
    s = A.dropna(subset=["fwd1", "z1"]).copy()
    s["ex"] = s["fwd1"] - s.groupby("coin")["fwd1"].transform("mean")
    f = s[s["z1"] < 0]
    res = {}
    for keys, g in f.groupby(["trend", "volq"]):
        if len(g) < 50: continue
        r = stats.linregress(g["z1"], g["ex"])
        res[str(keys)] = pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr,
                                    "mean_ex_z1<-1.5": g.loc[g["z1"] < -1.5, "ex"].mean(),
                                    "n_z1<-1.5": (g["z1"] < -1.5).sum()})
    out["next-day ex on z1 (falls) by trend x vol half"] = pd.DataFrame(res).T.round(5)
    f["zb"] = pd.cut(f["z1"], [-99, -2.5, -1.5, -1, -0.5, 0])
    t = f.groupby("zb")["ex"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    t["days"] = f.groupby("zb")["ts"].nunique()
    out["next-day ex by z1 fall bucket"] = t.round(5)
    # day-clustered t for the falls slope proxy: daily sum of z1-weighted deviations
    f2 = f.copy()
    f2["prod"] = -f2["z1"] * f2["ex"]
    d = f2.groupby("ts")["prod"].sum()
    out["falls: day-clustered t of -z1*ex"] = pd.Series({"days": len(d), "mean": d.mean(), "t": d.mean() / (d.std() / np.sqrt(len(d)))}).round(5)
    # 2) 3-day fall continuation outside rising, by 60d trend
    G = A[A["pos"] % 3 == 0].dropna(subset=["fwd3", "z3"]).copy()
    G["ex"] = G["fwd3"] - G.groupby("coin")["fwd3"].transform("mean")
    res = {}
    for keys, g in G[G["z3"] < 0].groupby(["trend", "volq"]):
        if len(g) < 50: continue
        r = stats.linregress(g["z3"], g["ex"])
        res[str(keys)] = pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr, "mean_ex": g["ex"].mean()})
    out["3d ex on z3 (falls) by trend x vol half"] = pd.DataFrame(res).T.round(5)
    res = {}
    for keys, g in G[G["z3"] > 0].groupby(["trend", "volq"]):
        if len(g) < 50: continue
        r = stats.linregress(g["z3"], g["ex"])
        res[str(keys)] = pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr, "mean_ex": g["ex"].mean()})
    out["3d ex on z3 (rises) by trend x vol half"] = pd.DataFrame(res).T.round(5)
    # 3) book: worst/best days
    D = pd.concat([d.assign(coin=c, win=w) for c, ws in data["days"].items() for w, d in ws.items()], ignore_index=True)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    bk["bq"] = pd.qcut(bk["br"].rank(method="first"), 20, labels=False)
    out["book: extreme day vigintiles"] = bk.groupby("bq").agg(n=("br", "size"), book=("br", "mean"), coins=("cr", "mean")).iloc[[0, 1, 18, 19]].round(4)
    bk["y"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book by year"] = bk.groupby("y").agg(n=("br", "size"), mean=("br", "mean"), sd=("br", "std"), coins=("cr", "mean")).round(5)
    return out

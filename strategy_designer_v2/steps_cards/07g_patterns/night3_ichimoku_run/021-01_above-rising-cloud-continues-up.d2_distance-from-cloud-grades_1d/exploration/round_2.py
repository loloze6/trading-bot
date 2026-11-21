def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "ret1": r1, "ret26": c / c.shift(26) - 1, "ret52": c / c.shift(52) - 1,
                "vol14": r1.rolling(14).std(), "vol60": r1.rolling(60).std(),
                "f26": c.shift(-26) / c - 1, "f7": c.shift(-7) / c - 1,
                "wd": ts.dt.weekday, "year": ts.dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # weekday, excess of coin mean daily return
    d = A.dropna(subset=["ret1"]).copy()
    d["ex"] = d["ret1"] - d.groupby("coin")["ret1"].transform("mean")
    def tt(x):
        return x.mean() / (x.std() / np.sqrt(len(x)))
    sat = d[d["wd"] == 5]
    out["sat_by_coin"] = sat.groupby("coin")["ex"].agg(["mean", "count", tt]).round(5)
    out["sat_by_year"] = sat.groupby("year")["ex"].agg(["mean", "count", tt]).round(5)
    fri = d[d["wd"] == 4]
    out["fri_by_coin"] = fri.groupby("coin")["ex"].agg(["mean", "count", tt]).round(5)
    wed = d[d["wd"] == 2]
    out["wed_by_coin"] = wed.groupby("coin")["ex"].agg(["mean", "count", tt]).round(5)
    # Saturday graded by Friday's return? Saturday excess vs prior-day ret
    d["prev"] = d.groupby(["coin", "win"])["ret1"].shift(1)
    s2 = d[(d["wd"] == 5)].dropna(subset=["prev"])
    sl = stats.linregress(s2["prev"], s2["ex"])
    out["sat_on_fri_ret"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(s2)})
    # weekend vol relative
    out["abs_by_wd"] = d.groupby("wd")["ret1"].apply(lambda x: x.abs().mean()).round(5)
    # 26-day momentum by coin and by window halves
    g = A[A["pos"] % 26 == 0].dropna(subset=["f26", "ret26"]).copy()
    g["ex"] = g["f26"] - g.groupby("coin")["f26"].transform("mean")
    res = []
    for k, gg in list(g.groupby("coin")) + [("w1-12", g[g["wn"] <= 12]), ("w13-24", g[g["wn"] > 12])]:
        s = stats.linregress(gg["ret26"], gg["ex"])
        res.append({"grp": k, "n": len(gg), "slope": s.slope, "t": s.slope / s.stderr})
    # vol-scaled momentum
    g2 = g.dropna(subset=["vol60"]).copy()
    g2["z"] = g2["ret26"] / (g2["vol60"] * np.sqrt(26))
    s = stats.linregress(g2["z"], g2["ex"])
    res.append({"grp": "volscaled_all", "n": len(g2), "slope": s.slope, "t": s.slope / s.stderr})
    g3 = g.dropna(subset=["ret52"])
    s = stats.linregress(g3["ret52"], g3["ex"])
    res.append({"grp": "ret52_all", "n": len(g3), "slope": s.slope, "t": s.slope / s.stderr})
    out["mom26"] = pd.DataFrame(res).round(4)
    # 7-day: trend sign in calm vs volatile
    g = A[A["pos"] % 7 == 0].dropna(subset=["f7", "vol14", "ret26"]).copy()
    g["ex"] = g["f7"] - g.groupby("coin")["f7"].transform("mean")
    g["vq"] = g.groupby("coin")["vol14"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    res = []
    for v in [0, 1, 2]:
        gg = g[g["vq"] == v]
        s = stats.linregress(gg["ret26"], gg["ex"])
        res.append({"vq": v, "n": len(gg), "slope": s.slope, "t": s.slope / s.stderr,
                    "upminusdown": gg[gg.ret26 > 0]["ex"].mean() - gg[gg.ret26 <= 0]["ex"].mean()})
    out["mom_by_vol_f7"] = pd.DataFrame(res).round(4)
    return out

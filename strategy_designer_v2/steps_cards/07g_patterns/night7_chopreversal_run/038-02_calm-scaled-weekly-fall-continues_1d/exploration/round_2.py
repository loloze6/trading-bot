def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            s3 = (c / c.shift(3) - 1) / (sd30 * np.sqrt(3))
            s7 = (c / c.shift(7) - 1) / (sd30 * np.sqrt(7))
            f5 = c.shift(-5) / c - 1
            f3 = c.shift(-3) / c - 1
            agit = (b["regime"] == "chop").astype(int)
            alloc = b["postRebalance_current_allocation"].astype(float)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "s3": s3, "s7": s7,
                                      "f5": f5, "f3": f3, "agit": agit, "alloc": alloc}))
    A = pd.concat(rows, ignore_index=True)
    out = {}
    g5 = A[A.pos % 5 == 0].dropna(subset=["f5", "s3", "s7"]).copy()
    drift = g5.groupby("coin")["f5"].mean()
    g5["u5"] = g5["f5"] - g5["coin"].map(drift)
    cal = g5[g5.agit == 0]
    def sl(d, x):
        if len(d) < 10: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["u5"]); return (r.slope, r.slope / r.stderr, len(d))
    out["calm slope u5 on s3 by window"] = pd.DataFrame({w: sl(d, "s3") for w, d in cal.groupby("w")}, index=["slope", "t", "n"]).T
    out["calm slope u5 on s3 by coin"] = pd.DataFrame({k: sl(d, "s3") for k, d in cal.groupby("coin")}, index=["slope", "t", "n"]).T
    out["calm slope s3 by side"] = pd.DataFrame({"rise": sl(cal[cal.s3 > 0], "s3"), "fall": sl(cal[cal.s3 < 0], "s3")}, index=["slope", "t", "n"])
    # signed directional unusual move: sign(s3)*u5 weighted
    cal = cal.assign(dirm=np.sign(cal.s3) * cal.u5)
    g = cal.groupby(cal.s3 > 0)["dirm"]
    out["calm dir. unusual move by side (True=rise)"] = pd.DataFrame({"mean": g.mean(), "n": g.count(), "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    # book allocation in calm by s7 quintile
    A2 = A.dropna(subset=["s7"])
    A2 = A2[A2.agit == 0].copy()
    A2["q"] = pd.qcut(A2.s7, 5, labels=False)
    out["mean alloc in calm by s7 quintile"] = A2.groupby("q")["alloc"].agg(["mean", lambda x: (x != 0).mean()])
    return out

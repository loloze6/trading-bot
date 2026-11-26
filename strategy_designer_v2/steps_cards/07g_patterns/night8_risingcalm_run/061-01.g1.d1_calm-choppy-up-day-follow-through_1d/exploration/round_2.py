def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z,
                               "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2) / c - 1,
                               "fwd5": c.shift(-5) / c - 1,
                               "tr": c / c.shift(30) - 1,
                               "vrel": sd / sd.rolling(90, min_periods=60).median(),
                               "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                               "day": ts.dt.floor("D"), "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h, col in [(1, "fwd1"), (2, "fwd2"), (5, "fwd5")]:
        dr = d[d.pos % h == 0].groupby("coin")[col].mean()
        d["ex" + str(h)] = d[col] - d["coin"].map(dr)
    def summ(gr, col):
        a = gr.agg(n=(col, "size"), mean=(col, "mean"), sd=(col, "std"))
        a["t"] = a["mean"] / (a["sd"] / np.sqrt(a["n"]))
        return a
    def daycl(sub, col, x):
        # slope with day-clustered t
        sub = sub.dropna(subset=[col, x])
        s = stats.linregress(sub[x], sub[col])
        res = sub[col] - (s.intercept + s.slope * sub[x])
        xd = sub[x] - sub[x].mean()
        sc = (xd * res).groupby(sub["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (xd ** 2).sum()
        return f"slope {s.slope:.5f} t_daycl {s.slope/se:.2f} n {len(sub)} days {sub['day'].nunique()}"
    d1 = d.dropna(subset=["z", "ex1", "vrel"]).copy()
    d1["agit"] = (d1["vrel"] > 1).astype(int)
    d1["zb"] = pd.cut(d1["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["next day ex by agit x z"] = summ(d1.groupby(["agit", "zb"]), "ex1")
    d1["trb"] = pd.cut(d1["tr"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    dn = d1[d1.z < 0]
    out["down days next-day ex, slope on z by agit"] = pd.Series({
        f"agit{a}": daycl(dn[dn.agit == a], "ex1", "z") for a in [0, 1]})
    out["down days next-day slope by trend x agit"] = pd.Series({
        f"{t}_agit{a}": daycl(dn[(dn.trb == t) & (dn.agit == a)], "ex1", "z")
        for t in ["fall", "chop", "rise"] for a in [0, 1]})
    up = d1[d1.z > 0]
    out["up days next-day slope by trend x agit"] = pd.Series({
        f"{t}_agit{a}": daycl(up[(up.trb == t) & (up.agit == a)], "ex1", "z")
        for t in ["fall", "chop", "rise"] for a in [0, 1]})
    g5 = d[(d.pos % 5 == 0)].dropna(subset=["z", "ex5", "vrel"]).copy()
    g5["agit"] = (g5["vrel"] > 1).astype(int)
    out["5d ex slope on z (up days) by agit"] = pd.Series({
        f"agit{a}": daycl(g5[(g5.agit == a) & (g5.z > 0)], "ex5", "z") for a in [0, 1]})
    out["5d ex slope on z (all days) by agit"] = pd.Series({
        f"agit{a}": daycl(g5[g5.agit == a], "ex5", "z") for a in [0, 1]})
    out["5d calm up-day slope by year"] = pd.Series({
        str(y): daycl(g5[(g5.agit == 0) & (g5.z > 0) & (g5.yr == y)], "ex5", "z")
        for y in sorted(g5.yr.unique())})
    out["next-day down-day slope by year"] = pd.Series({
        str(y): daycl(dn[dn.yr == y], "ex1", "z") for y in sorted(dn.yr.unique())})
    # low close next day, by agit
    out["next-day slope on close pos by agit"] = pd.Series({
        f"agit{a}": daycl(d1[d1.agit == a], "ex1", "clpos") for a in [0, 1]})
    return out

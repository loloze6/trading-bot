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
            ts = pd.to_datetime(b["timestamp"])
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "z": r / sd, "rngz": (hl / c.shift(1)) / sd,
                               "clpos": (c - b["low"]) / hl,
                               "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2) / c - 1,
                               "tr": c / c.shift(30) - 1,
                               "vrel": sd / sd.rolling(90, min_periods=60).median(),
                               "day": ts.dt.floor("D"), "yr": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in [1, 2]:
        dr = d[d.pos % h == 0].groupby("coin")["fwd" + str(h)].mean()
        d["ex" + str(h)] = d["fwd" + str(h)] - d["coin"].map(dr)
    d = d.dropna(subset=["z", "vrel", "clpos", "tr"])
    d["agit"] = (d.vrel > 1).astype(int)
    d["trb"] = pd.cut(d["tr"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    d["hc"] = d["clpos"] - 0.5  # signed nearness to the high
    def daycl(sub, col, x):
        sub = sub.dropna(subset=[col, x])
        if len(sub) < 20: return "n<20"
        s = stats.linregress(sub[x], sub[col])
        res = sub[col] - (s.intercept + s.slope * sub[x])
        xd = sub[x] - sub[x].mean()
        sc = (xd * res).groupby(sub["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (xd ** 2).sum()
        m = sub[col].mean()
        mc = sub.groupby("day")[col].sum() - 0
        return f"slope {s.slope:.5f} t_daycl {s.slope/se:.2f} mean {m:.5f} n {len(sub)} days {sub['day'].nunique()}"
    out = {}
    hi = d[d.clpos > 0.5]
    lo = d[d.clpos <= 0.5]
    out["agit: next-day ex on clpos, high-close half, by trend"] = pd.Series({
        str(t): daycl(hi[(hi.agit == 1) & (hi.trb == t)], "ex1", "clpos") for t in ["fall", "chop", "rise"]})
    out["agit: next-day ex on clpos, low-close half, by trend"] = pd.Series({
        str(t): daycl(lo[(lo.agit == 1) & (lo.trb == t)], "ex1", "clpos") for t in ["fall", "chop", "rise"]})
    out["agit: next-day ex on clpos, all, by trend"] = pd.Series({
        str(t): daycl(d[(d.agit == 1) & (d.trb == t)], "ex1", "clpos") for t in ["fall", "chop", "rise"]})
    out["agit: next-day ex on clpos, by year"] = pd.Series({
        str(y): daycl(d[(d.agit == 1) & (d.yr == y)], "ex1", "clpos") for y in sorted(d.yr.unique())})
    g2 = d[d.pos % 2 == 0]
    out["agit: 2-day ex on clpos, by trend"] = pd.Series({
        str(t): daycl(g2[(g2.agit == 1) & (g2.trb == t)], "ex2", "clpos") for t in ["fall", "chop", "rise"]})
    # high close weighted by range in swing units
    d["hcr"] = d["hc"] * d["rngz"]
    out["agit: next-day ex on (clpos-0.5)*range_z, by trend"] = pd.Series({
        str(t): daycl(d[(d.agit == 1) & (d.trb == t)], "ex1", "hcr") for t in ["fall", "chop", "rise"]})
    out["calm: next-day ex on clpos, by trend"] = pd.Series({
        str(t): daycl(d[(d.agit == 0) & (d.trb == t)], "ex1", "clpos") for t in ["fall", "chop", "rise"]})
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [18, 36]
    lst = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","high","low","close"]].copy().reset_index(drop=True)
            c = d["close"]; rng = d["high"] - d["low"]
            d["low12"] = d["low"].shift(1).rolling(12).min()
            d["high12"] = d["high"].shift(1).rolling(12).max()
            mr = rng.shift(1).rolling(180, min_periods=90).mean()
            d["width"] = (d["high12"] - d["low12"]) / mr
            d["r180"] = c / c.shift(180) - 1
            r1 = c.pct_change()
            sd = r1.rolling(180, min_periods=90).std()
            d["r180z"] = d["r180"] / (sd * np.sqrt(180))
            d["vol"] = sd
            d["pos"] = np.arange(len(d))
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["coin"] = coin; d["win"] = w
            lst.append(d)
    allb = pd.concat(lst, ignore_index=True)
    for h in H:
        dr = allb[allb["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        allb[f"u{h}"] = allb[f"f{h}"] - allb["coin"].map(dr)
    allb["volq"] = allb.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    def summ(x):
        x = x.dropna(); n = len(x)
        if n < 5: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    def cases(mask, h):
        sub = allb[mask & allb[f"u{h}"].notna()].copy()
        sub["cell"] = sub["pos"] // h
        return sub.groupby(["coin", "win", "cell"], sort=False).head(1)
    out = {}
    bup = allb["close"] > allb["high12"]; up = allb["r180"] > 0
    brk = allb["close"] < allb["low12"]
    cs = cases(bup & up, 36)
    out["bo_up_36_by_year"] = cs.groupby("year")["u36"].apply(summ).unstack()
    cs2 = cs[cs["width"].notna()].copy()
    cs2["q"] = pd.qcut(cs2["width"].rank(method="first"), 5, labels=False)
    out["bo_up_36_by_width"] = cs2.groupby("q")["u36"].apply(summ).unstack()
    # all grid bars: 30-day return z, at 36 bars
    for h in H:
        g = allb[(allb["pos"] % h == 0) & allb[f"u{h}"].notna() & allb["r180z"].notna()].copy()
        g["q"] = g.groupby("coin")["r180z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out[f"grid{h}_by_r180z_q"] = g.groupby("q")[f"u{h}"].apply(summ).unstack()
        if h == 36:
            out["grid36_deepq_by_year"] = g[g["q"] == 0].groupby("year")["u36"].apply(summ).unstack()
            out["grid36_topq_by_year"] = g[g["q"] == 4].groupby("year")["u36"].apply(summ).unstack()
    # width on all grid18 bars, within vol tercile, by year sign
    g = allb[(allb["pos"] % 18 == 0) & allb["u18"].notna() & allb["width"].notna()].copy()
    g["wq"] = g.groupby("coin")["width"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["grid18_width_q_by_volq"] = g.groupby(["volq", "wq"])["u18"].mean().unstack()
    out["grid18_width_q_by_r180sign"] = g.groupby([g["r180"] > 0, "wq"])["u18"].mean().unstack()
    rows = []
    for y, s in g.groupby("year"):
        rho, p = stats.spearmanr(s["width"], s["u18"]); rows.append(pd.Series({"year": y, "n": len(s), "rho": rho, "p": p}))
    out["grid18_width_rho_by_year"] = pd.DataFrame(rows)
    rows = []
    for co, s in g.groupby("coin"):
        rho, p = stats.spearmanr(s["width"], s["u18"]); rows.append(pd.Series({"coin": co, "n": len(s), "rho": rho}))
    out["grid18_width_rho_by_coin"] = pd.DataFrame(rows)
    # breakdown-uptrend width grading by year
    cb = cases(brk & up, 18); cb = cb[cb["width"].notna()].copy()
    cb["wide"] = cb["width"] > cb["width"].median()
    out["bd_up_wide_minus_narrow_by_year"] = cb.groupby(["year", "wide"])["u18"].mean().unstack()
    return out

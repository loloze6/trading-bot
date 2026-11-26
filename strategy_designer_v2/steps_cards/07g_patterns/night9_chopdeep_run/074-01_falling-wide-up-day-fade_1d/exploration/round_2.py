def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["ts"] = pd.to_datetime(b["timestamp"])
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            d["ret"] = c.pct_change()
            d["fwd1"] = c.shift(-1) / c - 1
            d["fwd2"] = c.shift(-2) / c - 1
            d["rr"] = (h - l) / (h - l).rolling(20).mean()
            d["vol30"] = d["ret"].rolling(30).std()
            d["r20"] = c / c.shift(20) - 1
            d["falling"] = (b["regime"] != "chop").astype(int)
            d["coin"] = coin; d["win"] = w
            d["wnum"] = int(w[1:])
            d["day"] = d["ts"].dt.floor("D")
            d["bookret"] = b["postRebalance_total_value"].astype(float).pct_change()
            d["pos"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    p = pd.concat(rows, ignore_index=True)
    drift1 = p.groupby("coin")["fwd1"].mean()
    p["ex1"] = p["fwd1"] - p["coin"].map(drift1)
    med = p.groupby("coin")["vol30"].transform("median")
    p["agit"] = (p["vol30"] > med).astype(int)
    p.loc[p["vol30"].isna(), "agit"] = np.nan
    def ct(g, col="ex1"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        D = len(s)
        se = np.sqrt((s**2).sum() * D / (D - 1)) / len(g)
        return pd.Series({"n": len(g), "days": D, "mean%": 100*m, "t_day": m/se})
    out = {}
    f = p[p.falling == 1].copy()
    f["up"] = (f["ret"] > 0).astype(int)
    f["wide"] = (f["rr"] > 1).astype(int)
    out["falling: ex1 by agit, up, wide (day-clustered)"] = f.dropna(subset=["agit","rr"]).groupby(["agit","up","wide"]).apply(ct)
    # graded within up&wide by rr tercile, by agitation
    uw = f[(f.up==1)&(f.wide==1)].dropna(subset=["agit"]).copy()
    uw["rrt"] = pd.qcut(uw["rr"], 3, labels=False)
    out["falling up wide: ex1 by agit, rr tercile"] = uw.groupby(["agit","rrt"]).apply(ct)
    out["falling up wide: ex1 by window"] = uw.groupby("wnum").apply(ct)
    # falling calm continuation: graded by 20-day return
    fc = f[f.agit==0].dropna(subset=["r20"]).copy()
    fc["r20q"] = pd.qcut(fc["r20"], 4, labels=False)
    out["falling calm: ex1 by r20 quartile"] = fc.groupby("r20q").apply(ct)
    out["falling calm: ex1 by window"] = fc.groupby("wnum").apply(ct)
    fa = f[f.agit==1].dropna(subset=["r20"]).copy()
    fa["r20q"] = pd.qcut(fa["r20"], 4, labels=False)
    out["falling agitated: ex1 by r20 quartile"] = fa.groupby("r20q").apply(ct)
    # non-falling calm, for comparison
    nf = p[(p.falling==0)].dropna(subset=["agit"])
    out["not falling: ex1 by agit"] = nf.groupby("agit").apply(ct)
    # weekday day-clustered, by falling
    p["wd"] = p["ts"].dt.dayofweek
    out["ex1 by weekday (clustered)"] = p.groupby("wd").apply(ct)
    # book: largest gains/losses, side and regime
    held = p[p["pos"].abs() > 0]
    out["book: positions count, share short"] = pd.Series({"n_bars_held": len(held), "share_short": float((held["pos"]<0).mean()), "mean_pos": float(held["pos"].mean())})
    return out

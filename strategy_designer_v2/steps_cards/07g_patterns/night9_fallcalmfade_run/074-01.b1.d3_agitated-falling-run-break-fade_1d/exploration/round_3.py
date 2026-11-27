def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append((c.shift(-1)/c-1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r0 = c.pct_change()
            nxt = c.shift(-1)/c-1
            r2 = c.shift(-2)/c-1
            ts = pd.to_datetime(b["timestamp"])
            dn = (r0 < 0).values
            rd = np.zeros(len(c)); loss = np.zeros(len(c))
            for i in range(1, len(c)):
                if dn[i]:
                    rd[i] = rd[i-1]+1; loss[i] = loss[i-1] + np.log(1+r0.iloc[i])
            sd30 = r0.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "r0": r0, "nxt": nxt, "x": nxt-mu, "x2": r2-2*mu,
                               "pdn": pd.Series(rd).shift(1).fillna(0),
                               "ploss": pd.Series(loss).shift(1).fillna(0),
                               "sd30": sd30, "regime": b["regime"].values,
                               "tr60": c/c.shift(60)-1, "tr20": c/c.shift(20)-1,
                               "day": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r0", "sd30"])
    d["agit"] = d["sd30"] / d.groupby("coin")["sd30"].transform("median")
    d["inprof"] = d["regime"] != "chop"
    d["depth"] = -d.ploss/d.sd30
    d["ag"] = np.where(d.agit > 1, "agit", "calm")
    d["t60"] = np.where(d.tr60.isna(), "na", np.where(d.tr60 < -0.10, "falling", np.where(d.tr60 > 0.10, "rising", "choppy")))

    def stat(g, col="x"):
        g = g.dropna(subset=[col])
        s = g.groupby("day")[col].sum()
        t = s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(s), "mean": g[col].mean(), "t_day": t})

    def slope(g, xcol, col="x"):
        g = g.dropna(subset=[xcol, col])
        X = g[xcol] - g[xcol].mean(); b = (X*g[col]).sum()/(X**2).sum()
        res = g[col] - g[col].mean() - b*X
        se = np.sqrt((res**2).sum()/(len(g)-2)/(X**2).sum())
        return pd.Series({"n": len(g), "slope": b, "t": b/se})

    out = {}
    rb = d[(d.r0 > 0) & (d.pdn >= 2)].copy()
    out["rb_by_t60_ag"] = rb.groupby(["t60", "ag"]).apply(stat)
    out["rb_by_t60_ag_2day"] = rb.groupby(["t60", "ag"]).apply(lambda g: stat(g, "x2"))
    out["rb_depth_slope_by_t60_ag"] = rb.groupby(["t60", "ag"]).apply(lambda g: slope(g, "depth"))
    fc = rb[(rb.t60 == "falling") & (rb.ag == "calm")].copy()
    if len(fc) > 9:
        fc["dt"] = pd.qcut(fc.depth, 3, labels=False, duplicates="drop")
        out["falling_calm_rb_by_depth_tertile"] = fc.groupby("dt").apply(stat)
    upn = d[(d.r0 > 0) & (d.pdn < 2)]
    out["up_noRB_by_t60_ag"] = upn.groupby(["t60", "ag"]).apply(stat)
    d20 = rb[(rb.tr20 < -0.05)].copy()
    d20["dt"] = pd.qcut(d20.depth, 3, labels=False, duplicates="drop")
    out["down20_rb_by_depth_tertile"] = d20.groupby("dt").apply(stat)
    out["down20_rb_by_coin"] = d20.groupby("coin").apply(stat)
    return out

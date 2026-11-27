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
            ts = pd.to_datetime(b["timestamp"])
            dn = (r0 < 0).values; up = (r0 > 0).values
            rd = np.zeros(len(c)); ru = np.zeros(len(c)); loss = np.zeros(len(c)); gain = np.zeros(len(c))
            for i in range(1, len(c)):
                if dn[i]:
                    rd[i] = rd[i-1]+1; loss[i] = loss[i-1] + np.log(1+r0.iloc[i])
                if up[i]:
                    ru[i] = ru[i-1]+1; gain[i] = gain[i-1] + np.log(1+r0.iloc[i])
            sd30 = r0.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "r0": r0, "nxt": nxt, "x": nxt-mu,
                               "pdn": pd.Series(rd).shift(1).fillna(0), "pup": pd.Series(ru).shift(1).fillna(0),
                               "ploss": pd.Series(loss).shift(1).fillna(0), "pgain": pd.Series(gain).shift(1).fillna(0),
                               "sd30": sd30, "regime": b["regime"].values,
                               "tr20": c/c.shift(20)-1,
                               "book": b["postRebalance_total_value"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "day": ts.dt.floor("D"), "yr": ts.dt.year})
            df["bookret_next"] = df["book"].shift(-1)/df["book"]-1
            df["agit"] = df["sd30"] / df.groupby("coin")["sd30"].transform("median")
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r0", "sd30"])
    d["agit"] = d["sd30"] / d.groupby("coin")["sd30"].transform("median")
    d["inprof"] = d["regime"] != "chop"
    d["z0"] = d.r0/d.sd30
    d["depth"] = -d.ploss/d.sd30
    d["tr"] = np.where(d.tr20 > 0.05, "up20", np.where(d.tr20 < -0.05, "down20", "flat20"))

    def stat(g, col="x"):
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
    out_rb = rb[~rb.inprof].copy()
    out_rb["ag"] = np.where(out_rb.agit > 1, "agit", "calm")
    out["rb_out_by_tr_agit"] = out_rb.groupby(["tr", "ag"]).apply(stat)
    out["rb_out_by_year"] = out_rb.groupby("yr").apply(stat)
    out["rb_in_by_year"] = rb[rb.inprof].groupby("yr").apply(stat)
    out["slopes_in"] = pd.DataFrame({"depth": slope(rb[rb.inprof], "depth"), "upz": slope(rb[rb.inprof], "z0"),
                                     "runlen": slope(rb[rb.inprof], "pdn")})
    out["slopes_out"] = pd.DataFrame({"depth": slope(out_rb, "depth"), "upz": slope(out_rb, "z0"),
                                      "runlen": slope(out_rb, "pdn")})
    out_rb["zt"] = pd.qcut(out_rb.z0, 3, labels=False)
    out["rb_out_by_upz"] = out_rb.groupby("zt").apply(stat)
    # all up days not ending a run, out of profile, for comparison
    upn = d[(d.r0 > 0) & (d.pdn < 2) & (~d.inprof)]
    out["up_noRB_out"] = stat(upn)
    # in-profile all days: next return on z0 slope
    out["inprof_z_slope"] = slope(d[d.inprof], "z0")
    out["all_z_slope_by_tr"] = d.groupby("tr").apply(lambda g: slope(g, "z0"))
    # book's largest gains/losses: next-day book return when in position
    pos = d[d.alloc.abs() > 0].dropna(subset=["bookret_next"]).copy()
    pos["q"] = pd.qcut(pos.bookret_next, 5, labels=False, duplicates="drop")
    out["book_quintiles"] = pos.groupby("q").agg(n=("x", "size"), bret=("bookret_next", "mean"),
                                                 upz=("z0", "mean"), depth=("depth", "mean"), runlen=("pdn", "mean"),
                                                 agit=("agit", "mean"))
    return out

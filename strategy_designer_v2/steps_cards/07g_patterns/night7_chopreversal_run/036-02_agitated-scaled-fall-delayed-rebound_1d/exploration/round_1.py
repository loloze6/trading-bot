def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            r5 = c / c.shift(5) - 1
            sd5 = sd * np.sqrt(5)
            z5 = r5 / sd5
            ag = (b["regime"] != "chop").astype(int)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "r": r, "z": z, "z5": z5,
                               "ag": ag, "wd": ts.dt.weekday, "yr": ts.dt.year, "sd": sd,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5):
        D[f"x{h}"] = D[f"f{h}"] - D.groupby("coin")[f"f{h}"].transform(lambda s: s.iloc[::1].mean())
    def grid(h):
        g = D[(D["pos"] % h == 0) & D[f"f{h}"].notna() & D["z"].notna()].copy()
        return g
    # forward excess by z bucket, agitated vs calm, horizons
    res = []
    for h in (1, 2, 3, 5):
        g = grid(h)
        g["zb"] = pd.cut(g["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
        for (ag, zb), s in g.groupby(["ag", "zb"], observed=True)[f"x{h}"]:
            res.append({"h": h, "ag": ag, "zb": str(zb), "n": len(s), "mean%": 100*s.mean(),
                        "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["fwd_excess_by_z"] = pd.DataFrame(res).pivot_table(index=["ag", "zb"], columns="h", values=["mean%", "t"]).round(2)
    # slope of forward excess on z, both sides, by agitation
    sl = []
    for h in (1, 2, 3, 5):
        g = grid(h)
        for ag in (0, 1):
            s = g[g.ag == ag]
            lr = stats.linregress(s["z"], s[f"x{h}"])
            sl.append({"h": h, "ag": ag, "n": len(s), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr})
            s2 = s[s.z5.notna()]
            lr = stats.linregress(s2["z5"], s2[f"x{h}"])
            sl.append({"h": h, "ag": ag, "n": len(s2), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "var": "z5"})
    out["slopes"] = pd.DataFrame(sl).round(3)
    # weekday 1-day excess
    g = grid(1)
    wd = g.groupby("wd")["x1"].agg(["count", "mean", "std"])
    wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"])); wd["mean"] *= 100
    out["weekday_x1"] = wd.round(3)
    # vol level: sd tercile within coin, 5-day forward
    g = grid(5)
    g["sdq"] = g.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    v = g.groupby(["sdq"])["x5"].agg(["count", "mean", "std"]); v["t"] = v["mean"]/(v["std"]/np.sqrt(v["count"])); v["mean"] *= 100
    out["vol_tercile_x5"] = v.round(3)
    # book: daily returns by window, and top/bottom days context
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    bw = DD.groupby("win")[["book_return", "coin_return"]].mean()*100
    out["book_by_window_mean%"] = bw.round(3)
    # yearly per coin z-slope consistency for 3-day, all regimes
    g = grid(3)
    cy = []
    for (coin), s in g.groupby("coin"):
        lr = stats.linregress(s["z"], s["x3"]); cy.append({"coin": coin, "n": len(s), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr})
    for yr, s in g.groupby("yr"):
        lr = stats.linregress(s["z"], s["x3"]); cy.append({"coin": str(yr), "n": len(s), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr})
    out["z_x3_by_coin_year"] = pd.DataFrame(cy).round(3)
    return out

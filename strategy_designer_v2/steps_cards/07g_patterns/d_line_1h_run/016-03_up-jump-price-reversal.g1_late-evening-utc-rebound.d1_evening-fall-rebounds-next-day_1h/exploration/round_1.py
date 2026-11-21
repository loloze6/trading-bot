def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    hr_rows = []; grid = []; bookd = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            hc = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            hr_rows.append(pd.DataFrame({"coin": coin, "hour_close": hc, "r": r1, "wd": (ts + pd.Timedelta(hours=1)).dt.weekday.values}))
            n = len(c)
            for t in range(24, n-24, 24):
                past = c[t]/c[t-24]-1; fwd = c[t+24]/c[t]-1
                rr = r1[t-23:t+1]; vv = v[t-23:t+1]
                sa = np.nansum(np.abs(rr))
                eff = abs(np.nansum(rr))/sa if sa > 0 else np.nan
                maxshare = np.nanmax(np.abs(rr))/sa if sa > 0 else np.nan
                vshare = np.nanmax(vv)/np.nansum(vv) if np.nansum(vv) > 0 else np.nan
                p72 = c[t]/c[t-72]-1 if t >= 72 else np.nan
                f72 = c[t+72]/c[t]-1 if t+72 < n else np.nan
                grid.append((coin, w, hc[t], past, fwd, eff, maxshare, vshare, sa, p72, f72))
    H = pd.concat(hr_rows).dropna()
    g = H.groupby("hour_close")["r"].agg(["mean", "std", "count"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["hourly ret by close hour (pooled)"] = g[["mean", "t", "count"]]
    g2 = H.groupby("wd")["r"].agg(["mean", "std", "count"])
    g2["t"] = g2["mean"]/(g2["std"]/np.sqrt(g2["count"]))
    out["hourly ret by weekday"] = g2[["mean", "t"]]
    G = pd.DataFrame(grid, columns=["coin", "w", "h", "past", "fwd", "eff", "maxsh", "vsh", "absum", "p72", "f72"]).dropna(subset=["past", "fwd"])
    G["exc"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["sgnpast"] = np.sign(G["past"])
    res = {}
    for nm, sub in [("all", G)]:
        X = np.c_[np.ones(len(sub)), sub["past"], sub["past"]*sub["eff"], sub["past"]*sub["vsh"]]
        y = sub["exc"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X@beta; s2 = resid@resid/(len(y)-X.shape[1])
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        res = pd.DataFrame({"beta": beta, "t": beta/se}, index=["c", "past", "past*eff", "past*vsh"])
    out["fwd24 exc on past, past*eff, past*volshare (n=%d)" % len(G)] = res
    G["effq"] = pd.qcut(G["eff"], 3, labels=["lo", "mid", "hi"])
    G["pq"] = pd.qcut(G["past"], 5, labels=False)
    tab = G.groupby(["pq", "effq"])["exc"].agg(["mean", "count"]).unstack()
    out["fwd24 exc by past quintile x eff tercile"] = tab
    # volatility level
    G["volq"] = G.groupby("coin")["absum"].transform(lambda s: pd.qcut(s, 5, labels=False))
    vt = G.groupby("volq").apply(lambda d: pd.Series({"slope_t": stats.linregress(d["past"], d["exc"]).slope / stats.linregress(d["past"], d["exc"]).stderr, "meanexc": d["exc"].mean(), "n": len(d)}))
    out["fwd24 on past24 slope t by vol quintile"] = vt
    G2 = G.dropna(subset=["p72", "f72"])
    lr = stats.linregress(G2["p72"], G2["f72"])
    out["f72 on p72 (overlapping-ish grid24) slope,t"] = f"{lr.slope:.4f}, t={lr.slope/lr.stderr:.2f}, n={len(G2)}"
    per = G.groupby("coin").apply(lambda d: pd.Series({"slope_t": stats.linregress(d["past"], d["exc"]).slope/stats.linregress(d["past"], d["exc"]).stderr, "n": len(d)}))
    out["per coin fwd24 on past24 t"] = per
    return out

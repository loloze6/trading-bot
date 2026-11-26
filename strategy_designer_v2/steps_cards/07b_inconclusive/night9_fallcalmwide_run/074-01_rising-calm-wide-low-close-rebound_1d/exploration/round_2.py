def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allr).mean()
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            h = df["high"].astype(float).values; l = df["low"].astype(float).values
            r = pd.Series(c).pct_change()
            s = r.rolling(30).std().values
            rng = (h-l)/c/s
            loc = (h-c)/np.where(h-l>0, h-l, np.nan)
            f = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(n):
                if f[i] > 0:
                    d = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                         "f": f[i], "rng": rng[i], "loc": loc[i], "todayret": r.iloc[i],
                         "lowgap": (c[i]-l[i])/c[i]/s[i]}
                    for H in (1, 2, 3, 5):
                        d[f"x{H}"] = (c[i+H]/c[i]-1 - H*mu) if i+H < n else np.nan
                    rows.append(d)
    D = pd.DataFrame(rows)
    def pooled(sub, col):
        sub = sub.dropna(subset=[col])
        if len(sub) < 3: return (len(sub), np.nan, np.nan)
        m = sub[col].mean()
        dev = (sub[col]-m).groupby(sub["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(sub)
        return (len(sub), m, m/se if se > 0 else np.nan)
    res = {}
    out = {}
    for k in ["f", "rng", "loc", "lowgap", "todayret"]:
        for H in (1, 2, 3, 5):
            g = D[[k, f"x{H}"]].dropna()
            r_ = g.corr().iloc[0, 1]; rs = stats.spearmanr(g[k], g[f"x{H}"])[0]
            out[(k, H)] = {"pearson": r_, "spearman": rs, "t": r_*np.sqrt((len(g)-2)/(1-r_**2)), "n": len(g)}
    res["corr_by_var_horizon"] = pd.DataFrame(out).T
    D["lq"] = pd.qcut(D["loc"].rank(method="first"), 3, labels=False)
    D["rh"] = pd.qcut(D["rng"].rank(method="first"), 2, labels=False)
    t = {}
    for H in (1, 3):
        for k, g in D.groupby(["rh", "lq"]):
            n, m, tt = pooled(g, f"x{H}"); t[(H,)+k] = {"n": n, "mean": m, "t": tt}
    res["range_half_x_loc_terc"] = pd.DataFrame(t).T
    t = {}
    for k, g in D.groupby("lq"):
        for H in (2, 3, 5):
            n, m, tt = pooled(g, f"x{H}"); t[(k, H)] = {"n": n, "mean": m, "t": tt, "locmean": g["loc"].mean()}
    res["loc_terc_horizons"] = pd.DataFrame(t).T
    t = {}
    for k, g in D.groupby("year"):
        for H in (1, 3):
            n, m, tt = pooled(g, f"x{H}"); t[(k, H)] = {"n": n, "mean": m, "t": tt}
        gg = g[["loc", "x1"]].dropna()
        t[(k, "corr_loc_x1")] = {"n": len(gg), "mean": gg.corr().iloc[0, 1]}
    res["by_year_h"] = pd.DataFrame(t).T
    t = {}
    for k, g in D.groupby("coin"):
        n, m, tt = pooled(g, "x3"); t[k] = {"n": n, "mean_x3": m, "t": tt}
    res["by_coin_x3"] = pd.DataFrame(t).T
    return res

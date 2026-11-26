def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        # coin mean daily return over all windows
        allr = []
        for w, df in ws.items():
            c = df["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allr).mean() if allr else np.nan
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
                    d = {"coin": coin, "w": w, "year": ts.iloc[i].year, "wd": ts.iloc[i].weekday(),
                         "day": ts.iloc[i].normalize(), "f": f[i], "rng": rng[i], "loc": loc[i],
                         "todayret": r.iloc[i]}
                    for H in (1, 2, 3, 5):
                        d[f"x{H}"] = (c[i+H]/c[i]-1 - H*mu) if i+H < n else np.nan
                    rows.append(d)
    D = pd.DataFrame(rows)
    def pooled(sub, col="x1"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 3: return (len(sub), np.nan, np.nan)
        m = sub[col].mean()
        dev = (sub[col]-m).groupby(sub["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(sub)
        return (len(sub), m, m/se if se > 0 else np.nan)
    def tab(key, col="x1"):
        out = {}
        for k, g in D.groupby(key):
            n, m, t = pooled(g, col); out[k] = {"n": n, "mean": m, "t": t}
        return pd.DataFrame(out).T
    res = {}
    res["overall_by_horizon"] = pd.DataFrame({H: dict(zip(["n","mean","t"], pooled(D, f"x{H}"))) for H in (1,2,3,5)}).T
    res["by_coin"] = tab("coin")
    res["by_window"] = tab("w")
    res["by_year"] = tab("year")
    D["fq"] = pd.qcut(D["f"].rank(method="first"), 4, labels=False)
    D["rq"] = pd.qcut(D["rng"].rank(method="first"), 4, labels=False)
    D["lq"] = pd.qcut(D["loc"].rank(method="first"), 3, labels=False)
    res["by_forecast_q"] = tab("fq")
    res["by_range_q"] = tab("rq")
    res["by_loc_terc"] = tab("lq")
    res["by_range_q_x3"] = tab("rq", "x3")
    res["by_weekday"] = tab("wd")
    res["range_q_means"] = D.groupby("rq")[["rng","loc","f","todayret"]].mean()
    res["corr_x1"] = pd.Series({k: D[[k,"x1"]].dropna().corr().iloc[0,1] for k in ["f","rng","loc","todayret"]})
    res["median_x1"] = float(D["x1"].median()); res["share_pos_x1"] = float((D["x1"]>0).mean())
    return res

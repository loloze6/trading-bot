def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            fc = df["forecast"].values.astype(float)
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(0, n, 72):
                if t < 72:
                    continue
                past = c[t] / c[t - 72] - 1
                hr = r[t - 71:t + 1]
                hr = hr[~np.isnan(hr)]
                top3 = np.sort(hr)[-3:].sum() if len(hr) >= 3 else np.nan
                topl3 = np.sort(hr)[:3].sum() if len(hr) >= 3 else np.nan
                g = np.clip(1 - top3 / past, 0, 1) if past > 0 else np.nan
                gd = np.clip(1 - topl3 / past, 0, 1) if past < 0 else np.nan
                d = {"coin": coin, "w": w, "year": year[t], "past": past, "grind": g, "grind_dn": gd,
                     "fc": fc[t]}
                for h in (24, 72, 144):
                    d["f%d" % h] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    for h in (24, 72, 144):
        D["x%d" % h] = D["f%d" % h] - D.groupby("coin")["f%d" % h].transform("mean")

    def ols(sub, y, xs):
        s = sub[[y] + xs].dropna()
        if len(s) < 30:
            return (np.nan, np.nan, len(s))
        X = np.column_stack([np.ones(len(s))] + [s[x].values for x in xs])
        Y = s[y].values
        b, *_ = np.linalg.lstsq(X, Y, rcond=None)
        e = Y - X @ b
        s2 = e @ e / (len(Y) - X.shape[1])
        cov = s2 * np.linalg.inv(X.T @ X)
        return (b[1], b[1] / np.sqrt(cov[1, 1]), len(s))

    up = D[D["past"] > 0]
    out = {}
    res = {}
    for h in (24, 72, 144):
        for v in ("fc", "grind"):
            res["%s_h%d" % (v, h)] = ols(up, "x%d" % h, [v, "past"])
    out["by_horizon_var"] = pd.DataFrame(res, index=["coef", "t", "n"]).T
    res = {}
    for coin, s in up.groupby("coin"):
        res[coin] = ols(s, "x72", ["fc", "past"]) + ols(s, "x72", ["grind", "past"])[1:2]
    out["by_coin"] = pd.DataFrame(res, index=["coef_fc", "t_fc", "n", "t_grind"]).T
    res = {}
    for y, s in up.groupby("year"):
        res[y] = ols(s, "x72", ["fc", "past"]) + ols(s, "x72", ["grind", "past"])[1:2]
    out["by_year"] = pd.DataFrame(res, index=["coef_fc", "t_fc", "n", "t_grind"]).T
    u = up.dropna(subset=["grind", "x72"]).copy()
    u["gq"] = pd.qcut(u["grind"].rank(method="first"), 5, labels=False)
    out["grind_quintile"] = u.groupby("gq").agg(n=("x72", "size"), grind=("grind", "mean"),
                                                past=("past", "mean"), x72=("x72", "mean"),
                                                x24=("x24", "mean"), x144=("x144", "mean"))
    u["pq"] = pd.qcut(u["past"].rank(method="first"), 3, labels=False)
    res = {}
    for q, s in u.groupby("pq"):
        res[q] = ols(s, "x72", ["grind", "past"]) + (s["past"].mean(),)
    out["by_rise_size_tercile"] = pd.DataFrame(res, index=["coef", "t", "n", "mean_past"]).T
    dn = D[D["past"] < 0]
    out["down_side_grind"] = pd.Series(ols(dn, "x72", ["grind_dn", "past"]), index=["coef", "t", "n"])
    out["fc_grind_corr"] = float(up[["fc", "grind"]].dropna().corr().iloc[0, 1])
    return out

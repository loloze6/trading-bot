def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []; days = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            vol20 = r1.shift(1).rolling(20).std()
            f = pd.DataFrame({"ret1": r1, "z1": r1 / vol20, "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                              "clv": (c - l) / (h - l).replace(0, np.nan),
                              "ret20": c / c.shift(20) - 1})
            f["fwd"] = c.shift(-H) / c - 1
            f["unus"] = (f["fwd"] - drift) / usual
            f["fwd1"] = c.shift(-1) / c - 1 - drift / H
            f["coin"] = coin; f["win"] = w; f["wn"] = int(w[1:])
            rows.append(f.iloc[np.arange(0, len(f), H)].dropna(subset=["fwd"]))
            days.append(f.dropna(subset=["fwd1"])[["wd", "fwd1", "coin", "yr"]])
    g = pd.concat(rows); d1 = pd.concat(days)
    out = {}
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    def tab(df, col, bins):
        d = df.dropna(subset=[col, "unus"]).copy()
        d["b"] = pd.cut(d[col], bins)
        t = d.groupby("b", observed=True)["unus"].agg(["size", "mean"])
        t["t"] = d.groupby("b", observed=True)["unus"].apply(tt)
        return t
    out["5d unus by z of 1-day return"] = tab(g, "z1", [-20, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 20])
    g["mild_down"] = g["z1"].between(-1.5, -0.5)
    out["mild down (z -1.5..-0.5) unus by year"] = g[g.mild_down].groupby("yr")["unus"].agg(["size", "mean"])
    out["mild down unus by coin"] = g[g.mild_down].groupby("coin")["unus"].agg(["size", "mean"])
    g["half"] = np.where(g["wn"] <= 12, "w1-w12", "w13-w24")
    out["mild down unus by half"] = g[g.mild_down].groupby("half")["unus"].agg(["size", "mean"])
    w = stats.ttest_ind(g[g.mild_down]["unus"], g[~g.mild_down]["unus"].dropna(), equal_var=False, nan_policy="omit")
    out["mild down minus other welch"] = pd.Series({"t": w.statistic})
    out["5d unus by ret20"] = tab(g, "ret20", [-5, -0.2, -0.1, 0, 0.1, 0.2, 0.4, 50])
    # weekday next-day by year: Thu+Fri minus Mon+Wed
    d1["grp"] = np.where(d1.wd.isin([3, 4]), "ThuFri", np.where(d1.wd.isin([0, 2]), "MonWed", "other"))
    out["next-day pct by year and group"] = (d1.groupby(["yr", "grp"])["fwd1"].mean() * 100).unstack()
    return out

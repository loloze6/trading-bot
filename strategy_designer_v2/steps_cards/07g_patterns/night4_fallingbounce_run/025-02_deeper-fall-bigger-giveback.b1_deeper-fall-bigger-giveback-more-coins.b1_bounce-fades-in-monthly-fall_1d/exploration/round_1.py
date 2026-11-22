def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # pooled drift per coin
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        drift = pd.concat(allr).mean() if allr else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol
            r90 = c / c.shift(90) - 1
            r30 = c / c.shift(30) - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            f5 = c.shift(-5) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "r90": r90, "r30": r30,
                               "f1": f1 - drift, "f3": f3 - 3 * drift, "f5": f5 - 5 * drift,
                               "vol": vol, "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "pos": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["z", "f1"])
    out = {}

    def summ(g, col):
        x = g[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    d["zbin"] = pd.cut(d["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    d["reg90"] = np.where(d["r90"] < 0, "r90neg", "r90pos")
    d["reg30"] = np.where(d["r30"] < 0, "r30neg", "r30pos")
    d.loc[d["r90"].isna(), "reg90"] = "na"
    d.loc[d["r30"].isna(), "reg30"] = "na"
    for col in ["f1", "f3"]:
        res = d.groupby(["zbin", "reg90", "reg30"], observed=True).apply(lambda g: summ(g, col)).reset_index()
        out["by zbin x regime, " + col] = res

    # up-jumps: relation of next-day return to r30 depth, all regimes
    up = d[d["z"] >= 2].dropna(subset=["r30"])
    up = up.assign(q30=pd.qcut(up["r30"], 5, labels=False))
    out["up jumps by r30 quintile f1"] = up.groupby("q30").apply(lambda g: pd.concat([summ(g, "f1"), pd.Series({"r30mean": g["r30"].mean()})]))
    out["up jumps by r30 quintile f3"] = up.groupby("q30").apply(lambda g: summ(g, "f3"))
    dn = d[d["z"] <= -2].dropna(subset=["r30"])
    dn = dn.assign(q30=pd.qcut(dn["r30"], 5, labels=False))
    out["down jumps by r30 quintile f1"] = dn.groupby("q30").apply(lambda g: pd.concat([summ(g, "f1"), pd.Series({"r30mean": g["r30"].mean()})]))
    out["down jumps by r30 quintile f3"] = dn.groupby("q30").apply(lambda g: summ(g, "f3"))

    # weekday on all bars (daily grid is non overlapping for f1)
    out["weekday f1"] = d.groupby("wd").apply(lambda g: summ(g, "f1"))
    # vol tercile
    d["vq"] = d.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["vol tercile f1"] = d.groupby("vq").apply(lambda g: summ(g, "f1"))
    # active book exposure share
    out["share bars in position"] = float((d["pos"].abs() > 1e-9).mean())
    out["active cases by year"] = d.assign(yr=0).groupby("w").apply(lambda g: pd.Series({"n_active": int((g["fc"] != 0).sum())})).T
    return out

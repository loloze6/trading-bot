def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = 72
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            r24 = c / c.shift(24) - 1
            r72p = c / c.shift(72) - 1
            absum = lr.abs().rolling(24).sum()
            eff = (np.log(c / c.shift(24))).abs() / absum
            maxh = lr.abs().rolling(24).max() / absum
            v = b["volume"].astype(float)
            vshare = v.rolling(24).max() / v.rolling(24).sum()
            vol24 = lr.rolling(24).std()
            vol30d = lr.rolling(720, min_periods=200).std()
            fwd = c.shift(-H) / c - 1
            fwd24 = c.shift(-24) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "r24": r24.iloc[idx].values, "r72p": r72p.iloc[idx].values,
                "eff": eff.iloc[idx].values, "maxh": maxh.iloc[idx].values, "vshare": vshare.iloc[idx].values,
                "volratio": (vol24 / vol30d).iloc[idx].values, "fwd": fwd.iloc[idx].values,
                "fwd24": fwd24.iloc[idx].values, "fc": b["forecast"].iloc[idx].values,
                "hour": ts.dt.hour.iloc[idx].values, "wd": ts.dt.weekday.iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values})
            rows.append(d)
    g = pd.concat(rows).dropna(subset=["fwd", "r24"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd"].transform("std")
    g["z"] = g["ex"] / g["sd"]
    g["r24z"] = g["r24"] / g.groupby("coin")["r24"].transform("std")
    g["sr24"] = np.sign(g["r24"])
    g["dirz"] = g["z"] * g["sr24"]  # continuation in direction of 24h move
    out = {}
    def tab(col, q=5, val="z"):
        x = g.dropna(subset=[col]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("b")[val].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std").round(4)
    out["r24 quintile -> z fwd72"] = tab("r24")
    out["r72past quintile -> z fwd72"] = tab("r72p")
    out["eff quintile -> continuation z (dir of 24h)"] = tab("eff", val="dirz")
    out["maxhour share quintile -> continuation z"] = tab("maxh", val="dirz")
    out["volume max share quintile -> continuation z"] = tab("vshare", val="dirz")
    out["vol ratio quintile -> z"] = tab("volratio")
    # regression: z on r24z, r24z*eff
    x = g.dropna(subset=["eff", "r24z", "volratio"]).copy()
    x["effc"] = x["eff"] - x["eff"].mean()
    X = np.column_stack([np.ones(len(x)), x["r24z"], x["r24z"] * x["effc"], x["volratio"] - x["volratio"].mean()])
    beta, *_ = np.linalg.lstsq(X, x["z"].values, rcond=None)
    res = x["z"].values - X @ beta
    s2 = res @ res / (len(x) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["reg z ~ r24z + r24z*eff + volratio"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "r24z", "r24z_x_eff", "volratio"]).round(4)
    out["n cases"] = len(g)
    t = g.groupby("wd")["z"].agg(["mean", "count"]); out["weekday z"] = t.round(4)
    t = g.groupby("year")["z"].agg(["mean", "count"]); out["year z"] = t.round(4)
    # by coin: corr r24 vs z
    out["coin corr r24-z"] = g.groupby("coin").apply(lambda d: pd.Series({"corr": d["r24"].corr(d["z"]), "n": len(d)})).round(4)
    # down moves only: eff effect on z
    dn = g[g["r24"] < 0].dropna(subset=["eff"]).copy()
    dn["b"] = pd.qcut(dn["eff"].rank(method="first"), 3, labels=False)
    out["falls: eff tercile -> z (rebound)"] = dn.groupby("b")["z"].agg(["mean", "count"]).round(4)
    up = g[g["r24"] > 0].dropna(subset=["eff"]).copy()
    up["b"] = pd.qcut(up["eff"].rank(method="first"), 3, labels=False)
    out["rises: eff tercile -> z"] = up.groupby("b")["z"].agg(["mean", "count"]).round(4)
    # book: days around largest losses
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    D = pd.concat(dd)
    D["mon"] = pd.to_datetime(D["day"]).dt.year
    out["book by year"] = D.groupby("mon")[["book_return", "coin_return"]].mean().round(5)
    return out

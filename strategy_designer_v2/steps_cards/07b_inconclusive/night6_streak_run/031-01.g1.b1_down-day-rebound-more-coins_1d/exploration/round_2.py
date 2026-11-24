def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [3, 10]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in H:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.extend(list(c[idx + h] / c[idx] - 1))
            drift[h] = np.nanmean(vals)
        for w, df in wins.items():
            c = df["close"].reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            z = r1 / vol
            r60 = c / c.shift(60) - 1
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                for k, i in enumerate(idx):
                    if np.isnan(z.iloc[i]):
                        continue
                    rows.append((coin, w, h, ts.iloc[i].normalize(), z.iloc[i],
                                 fwd[k] - drift[h], fwd[k], r60.iloc[i]))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "day", "z", "u", "fwd", "r60"])
    # market-adjusted: minus same-day mean fwd across coins (diagnostic only)
    d["ma"] = d["fwd"] - d.groupby(["h", "day"])["fwd"].transform("mean")
    d["ncoin"] = d.groupby(["h", "day"])["fwd"].transform("count")

    def slope_t(sub, x, y):
        sub = sub.dropna(subset=[x, y])
        if len(sub) < 30:
            return np.nan, np.nan, len(sub)
        X = np.c_[np.ones(len(sub)), sub[x].values]; Y = sub[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]
        e = Y - X @ b
        XtX = np.linalg.inv(X.T @ X)
        s = pd.DataFrame(X * e[:, None]).groupby(sub["day"].values).sum().values
        G = len(s)
        V = XtX @ (s.T @ s) @ XtX * G / (G - 1)
        return b[1] * 100, b[1] / np.sqrt(V[1, 1]), len(sub)

    out = {}
    res = []
    for h in H:
        dd = d[d.h == h].copy()
        dd["fall"] = -dd["z"]; dd["absz"] = dd["z"].abs()
        dn = dd[dd.z < 0]
        dnm = dn[dn.ncoin >= 5]
        for lab, sub, x, y in [
            ("down raw u", dn, "fall", "u"),
            ("down mkt-adj (>=5 coins)", dnm, "fall", "ma"),
            ("down u same subset", dnm, "fall", "u"),
            ("all days |z| u", dd, "absz", "u"),
            ("all days signed z u", dd, "z", "u"),
            ("down r60>0", dn[dn.r60 > 0], "fall", "u"),
            ("down r60<=0", dn[dn.r60 <= 0], "fall", "u"),
        ]:
            b, t, n = slope_t(sub, x, y)
            res.append((h, lab, n, b, t))
    out["slopes"] = pd.DataFrame(res, columns=["h", "test", "n", "slope_%", "t"])
    # share of variance of u explained by market (h=3, down days)
    dn = d[(d.h == 3) & (d.z < 0) & (d.ncoin >= 5)]
    out["h3 down: std u %"] = float(dn.u.std() * 100)
    out["h3 down: std mkt-adj %"] = float(dn.ma.std() * 100)
    # down, fall terciles, mkt-adj mean and day-clustered t
    dn = dn.copy(); dn["q"] = pd.qcut(-dn.z, 3, labels=["small", "mid", "large"])
    res = []
    for q, sub in dn.groupby("q", observed=True):
        for col in ["u", "ma"]:
            g = sub.groupby("day")[col]
            m = sub[col].mean()
            se = np.sqrt(((g.sum() - g.count() * m) ** 2).sum()) / len(sub)
            res.append((str(q), col, len(sub), m * 100, m / se))
    out["h3 down terciles"] = pd.DataFrame(res, columns=["fall", "measure", "n", "mean_%", "t"])
    return out

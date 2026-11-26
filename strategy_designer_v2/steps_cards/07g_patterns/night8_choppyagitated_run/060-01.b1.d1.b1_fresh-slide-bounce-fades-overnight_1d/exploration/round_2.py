def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "z1": r / vol,
                "z5l": (c.shift(1) / c.shift(6) - 1) / (vol * np.sqrt(5)),
                "tr60": c / c.shift(60) - 1,
                "vol": vol,
                "clv": (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "fc": b["forecast"].astype(float),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # agitation proxy: coin's vol30 vs that coin's median vol30 over all its recorded bars
    d["agit"] = np.where(d["vol"] > d.groupby("coin")["vol"].transform("median"), "agit", "calm")
    mu = d.groupby("coin")["r"].mean()
    d["mu"] = d["coin"].map(mu)
    d["x1"] = d["f1"] - d["mu"]; d["x3"] = d["f3"] - 3 * d["mu"]
    d["pw"] = d.groupby(["coin", "win"]).cumcount()
    d["trb"] = pd.cut(d["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])

    def tday(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 3: return pd.Series({"n": len(s)})
        m = s[col].mean(); dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "mean%": 100 * m, "t": m / se})

    def slope(s, xcol, ycol):
        s = s.dropna(subset=[xcol, ycol])
        if len(s) < 20: return pd.Series({"n": len(s)})
        x = s[xcol] - s[xcol].mean(); y = s[ycol]
        b = (x * y).sum() / (x ** 2).sum()
        e = y - y.mean() - b * x
        se = np.sqrt(((x * e).groupby(s["day"]).sum() ** 2).sum()) / (x ** 2).sum()
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "slope%": 100 * b, "t": b / se})

    out = {}
    d["z1c"] = pd.cut(d["z1"], [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["x1 by trend,agit,z1"] = d.groupby(["trb", "agit", "z1c"], observed=True).apply(lambda s: tday(s, "x1"))
    g3 = d[d["pw"] % 3 == 0]
    out["x3 grid by trend,agit,z1"] = g3.groupby(["trb", "agit", "z1c"], observed=True).apply(lambda s: tday(s, "x3"))
    # graded slopes
    up = d[d["z1"] > 0]; dn = d[d["z1"] < 0]
    out["slope x1 on z1, up days"] = up.groupby(["trb", "agit"], observed=True).apply(lambda s: slope(s, "z1", "x1"))
    out["slope x1 on -z1, down days"] = dn.assign(nz=-dn["z1"]).groupby(["trb", "agit"], observed=True).apply(lambda s: slope(s, "nz", "x1"))
    up3 = g3[g3["z1"] > 0]; dn3 = g3[g3["z1"] < 0]
    out["slope x3 grid on z1, up days"] = up3.groupby(["trb", "agit"], observed=True).apply(lambda s: slope(s, "z1", "x3"))
    out["slope x3 grid on -z1, down days"] = dn3.assign(nz=-dn3["z1"]).groupby(["trb", "agit"], observed=True).apply(lambda s: slope(s, "nz", "x3"))
    # falling up days: close location slope (lower close -> more giveback?)
    fu = d[(d["trb"] == "fall") & (d["z1"] > 0.5)]
    out["fall up-days x1 on (1-clv)"] = slope(fu.assign(w=1 - fu["clv"]), "w", "x1").to_frame().T
    # book: daily returns, largest days
    br = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            br.append(dd.assign(coin=coin, win=w))
    bd = pd.concat(br)
    bk = bd.groupby("day")["book_return"].mean().dropna()
    q = bk.quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    out["book daily return quantiles %"] = (100 * q).to_frame("pct")
    top = bk.abs().sort_values(ascending=False)
    out["share of book sum from top 10 |days|"] = float(bk[top.index[:10]].sum() / bk.sum())
    out["book days nonzero"] = int((bk != 0).sum())
    return out

def explore(data):
    import numpy as np, pandas as pd
    res = {}
    rows = []
    grid = []
    for coin, wins in data["bars"].items():
        xs = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 14, 14):
                xs.append(c[i + 14] / c[i] - 1)
        dr, sd = np.mean(xs), np.std(xs, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            z = r1 / vol30.shift(1)
            z3 = (c / c.shift(3) - 1) / (vol30.shift(3) * np.sqrt(3))
            df = pd.DataFrame(dict(coin=coin, win=w, day=ts.dt.normalize(), year=ts.dt.year,
                                   z=z, z3=z3, n1=r1.shift(-1), n3=c.shift(-3) / c - 1))
            rows.append(df)
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            for i in range(0, len(c) - 14, 14):
                grid.append(dict(day=ts.iloc[i].normalize(), vr=vr.iloc[i], vol30=vol30.iloc[i],
                                 fwdz=(c.iloc[i + 14] / c.iloc[i] - 1 - dr) / sd))
    d = pd.concat(rows)

    def cslope(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 30: return pd.Series(dict(b=np.nan, t=np.nan, n=len(df), days=0))
        X = df[x].clip(-5, 5); X = X - X.mean()
        e = df[y] - df[y].mean()
        b = (X * e).sum() / (X ** 2).sum()
        r = e - b * X
        sc = (X * r).groupby(df["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(b=b, t=b / se, n=len(df), days=df["day"].nunique()))

    x = d[d.coin == "XMRUSD"]
    res["xmr_n1_on_z_by_year"] = pd.DataFrame({str(k): cslope(s, "z", "n1") for k, s in x.groupby("year")}).T
    res["xmr_n1_on_z_all"] = cslope(x, "z", "n1")
    res["xmr_n3_on_z3"] = cslope(x.iloc[::3], "z3", "n3")
    res["xmr_up_vs_down"] = pd.DataFrame({"up_z_gt0": cslope(x[x.z > 0], "z", "n1"),
                                         "down_z_lt0": cslope(x[x.z < 0], "z", "n1")}).T
    res["all_n1_on_z_pooled"] = cslope(d, "z", "n1")
    g = pd.DataFrame(grid).dropna()
    g["vrs"] = (g.vr - g.vr.mean()) / g.vr.std()
    g["vls"] = (g.vol30 - g.vol30.mean()) / g.vol30.std()
    g["inter"] = g.vrs * g.vls
    # residualise interaction on vrs and vls, then slope
    X = np.column_stack([np.ones(len(g)), g.vrs, g.vls])
    bta = np.linalg.lstsq(X, g.inter.values, rcond=None)[0]
    g["inter_res"] = g.inter - X @ bta
    yb = np.linalg.lstsq(X, g.fwdz.values, rcond=None)[0]
    g["y_res"] = g.fwdz - X @ yb
    res["vr_x_vol_interaction"] = cslope(g, "inter_res", "y_res")
    return res

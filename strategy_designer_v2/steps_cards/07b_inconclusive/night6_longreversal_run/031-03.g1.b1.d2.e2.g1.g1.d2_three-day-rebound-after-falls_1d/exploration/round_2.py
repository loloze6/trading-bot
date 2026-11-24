def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, df in data["bars"][coin].items():
        df = df.reset_index(drop=True)
        c = df["close"].values; n = len(df)
        r1 = pd.Series(c).pct_change()
        vol = r1.rolling(30, min_periods=20).std()
        vr = vol / vol.rolling(180, min_periods=45).mean()
        yr = pd.to_datetime(df["timestamp"]).dt.year.values
        for i in range(n):
            d = {"w": w, "pos": i, "f": df["forecast"].values[i], "yr": yr[i],
                 "z1": r1.values[i]/vol.values[i] if vol.values[i] > 0 else np.nan, "vr": vr.values[i]}
            for h in (1, 2, 3):
                d[f"fr{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
            rows.append(d)
    a = pd.DataFrame(rows)
    out = {}
    def tc(x, y):
        m = x.notna() & y.notna(); x, y = x[m], y[m]; n = len(x)
        r = np.corrcoef(x, y)[0, 1]
        return n, r, r*np.sqrt((n-2)/(1-r**2))
    for h in (1, 3):
        g = a[a.pos % h == 0].dropna(subset=[f"fr{h}"]).copy()
        g["ex"] = g[f"fr{h}"] - g[f"fr{h}"].mean()
        res = []
        for nm, x in [("forecast", g.f), ("fall_z_only", (-g.z1).clip(lower=0)),
                      ("fall_z_x_vr", (-g.z1).clip(lower=0)*g.vr), ("negz_both", -g.z1)]:
            n, r, t = tc(x, g.ex); res.append({"x": nm, "n": n, "corr": r, "t": t})
        out[f"h{h}_variants"] = pd.DataFrame(res)
        fl = g[g.z1 < 0].dropna(subset=["vr"]).copy()
        fl["vrq"] = pd.qcut(fl.vr, 3, labels=["vr_low", "vr_mid", "vr_high"])
        out[f"h{h}_falls_by_volratio"] = fl.groupby("vrq").apply(
            lambda x: pd.Series(dict(zip(["n", "corr", "t"], tc(-x.z1, x.ex))) | {"ex": x.ex.mean()}))
        out[f"h{h}_by_year"] = g.groupby("yr").apply(
            lambda x: pd.Series(dict(zip(["n", "corr", "t"], tc(x.f, x.ex)))))
        gz = g.dropna(subset=["z1"]).copy()
        gz["zb"] = pd.cut(gz.z1, [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
        out[f"h{h}_by_z1_bin"] = gz.groupby("zb").agg(n=("ex", "size"), ex=("ex", "mean"))
    return out

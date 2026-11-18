def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z = r1 / vol20
            vr = v / v.shift(1).rolling(30).mean()
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=int(yr.iloc[i]),
                                     f=float(df["forecast"].iloc[i]), z=z.iloc[i], vr=vr.iloc[i],
                                     ret=c.iloc[i + h] / c.iloc[i] - 1))
    d = pd.DataFrame(rows)
    d["mean_c"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mean_c"]
    d["q"] = -d["f"] / 10 * d["ex"]
    out = {}
    def tt(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    a = d[d.f < 0]
    out["main_by_h"] = a.groupby("h")["q"].apply(tt).unstack()
    out["ex_active_by_h"] = a.groupby("h")["ex"].apply(tt).unstack()
    a5 = a[a.h == 5]
    out["main5_by_coin"] = a5.groupby("coin")["q"].apply(tt).unstack()
    out["main5_by_year"] = a5.groupby("year")["q"].apply(tt).unstack()
    a5 = a5.copy()
    a5["fq"] = pd.qcut(a5["f"].rank(method="first"), 5, labels=False)
    out["ex5_by_forecast_quintile(0=most neg)"] = a5.groupby("fq")["ex"].apply(tt).unstack()
    # all grid bars, h=5: excess by sign of day and volume (thin/heavy)
    g = d[(d.h == 5)].dropna(subset=["z", "vr"]).copy()
    g["side"] = np.where(g.z > 0, "up", "down")
    g["zb"] = pd.cut(g.z.abs(), [0, 1, 2, 100], labels=["<1", "1-2", ">2"])
    g["volb"] = pd.cut(g.vr, [0, 0.7, 1, 1.5, 100], labels=["<0.7", "0.7-1", "1-1.5", ">1.5"])
    out["ex5_side_zb_volb"] = g.groupby(["side", "zb", "volb"], observed=True)["ex"].apply(tt).unstack()
    g1 = d[(d.h == 1)].dropna(subset=["z", "vr"]).copy()
    g1["side"] = np.where(g1.z > 0, "up", "down")
    g1["big"] = g1.z.abs() > 1.5
    g1["thin"] = g1.vr < 1
    out["ex1_side_big_thin"] = g1.groupby(["side", "big", "thin"])["ex"].apply(tt).unstack()
    return out

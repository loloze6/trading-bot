def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = r1 / sd
            calm = (b["regime"] == "chop")
            n = len(b)
            for h in (1, 2, 3, 5, 7):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if np.isnan(z.iloc[i]) or np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, z=z.iloc[i], fwd=fwd.iloc[i],
                                     calm=bool(calm.iloc[i]), ts=b["timestamp"].iloc[i]))
    df = pd.DataFrame(rows)
    df["dm"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["sdir"] = np.sign(df["z"]) * df["dm"]

    def clus(g):
        g = g.dropna(subset=["z", "dm"])
        if len(g) < 20: return pd.Series(dict(n=len(g), slope=np.nan, t_clu=np.nan, sdir=np.nan))
        X = g["z"] - g["z"].mean(); y = g["dm"]
        bt = (X * y).sum() / (X ** 2).sum()
        res = y - y.mean() - bt * X
        sc = (X * res).groupby(g["ts"]).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series(dict(n=len(g), slope=bt, t_clu=bt / se, sdir=g["sdir"].mean()))

    out = {}
    out["by_h_calm_clustered"] = df.groupby(["h", "calm"]).apply(clus)
    d1 = df[(df.h == 1)].copy()
    d1["zb"] = pd.cut(d1["z"].abs(), [0, 0.5, 1, 1.5, 2, 3, 99])
    out["h1_zbucket_calm"] = d1.groupby(["calm", "zb"])["sdir"].agg(["count", "mean"])
    a1 = d1[~d1.calm]
    out["h1_agit_window"] = a1.groupby("w").apply(clus)
    out["h1_agit_coin"] = a1.groupby("coin").apply(clus)
    out["h1_agit_side"] = a1.groupby(np.sign(a1["z"])).apply(clus)
    d5 = df[(df.h == 5) & df.calm]
    out["h5_calm_year"] = d5.groupby(pd.to_datetime(d5["ts"]).dt.year).apply(clus)
    return out

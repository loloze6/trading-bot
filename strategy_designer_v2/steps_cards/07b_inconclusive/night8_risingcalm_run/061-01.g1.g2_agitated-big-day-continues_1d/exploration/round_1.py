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
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if np.isnan(z.iloc[i]) or np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, i=i, z=z.iloc[i], f=b["forecast"].iloc[i],
                                     fwd=fwd.iloc[i], calm=bool(calm.iloc[i]), day=i))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["dm"] = df["fwd"] - df["drift"]
    df["sdir"] = np.sign(df["z"]) * df["dm"]  # move in day's direction

    def slope(g, x="z"):
        g = g.dropna(subset=[x, "dm"])
        if len(g) < 20: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, sdir=np.nan, t_sdir=np.nan))
        X = g[x] - g[x].mean(); y = g["dm"]
        bt = (X * y).sum() / (X ** 2).sum()
        res = y - y.mean() - bt * X
        se = np.sqrt((X ** 2 * res ** 2).sum()) / (X ** 2).sum()
        s = g["sdir"]
        return pd.Series(dict(n=len(g), slope=bt, t=bt / se, sdir=s.mean(), t_sdir=s.mean() / (s.std() / np.sqrt(len(s)))))

    out = {}
    out["by_h_calm"] = df.groupby(["h", "calm"]).apply(slope)
    d5 = df[df.h == 5].copy()
    d5["zb"] = pd.cut(d5["z"].abs(), [0, 0.5, 1, 1.5, 2, 3, 99])
    out["h5_zbucket_calm"] = d5.groupby(["calm", "zb"])["sdir"].agg(["count", "mean"])
    out["h5_side_calm"] = d5.groupby(["calm", np.sign(d5["z"])]).apply(slope)
    out["h5_coin_calm"] = d5.groupby(["calm", "coin"]).apply(slope)
    out["h5_window_calm"] = d5.groupby(["w", "calm"]).apply(slope)
    d5["big"] = d5["z"].abs() > 1.5
    out["h5_big_calm"] = d5[d5.big].groupby(["calm", "h"]).apply(slope)
    d10 = df[df.h == 10].copy()
    out["h10_big_calm"] = d10[d10.z.abs() > 1.5].groupby("calm")["sdir"].agg(["count", "mean", "std"])
    return out

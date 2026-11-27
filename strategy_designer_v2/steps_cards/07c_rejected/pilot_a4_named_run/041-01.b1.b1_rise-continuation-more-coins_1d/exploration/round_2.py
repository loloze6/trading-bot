def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    H = [1, 2, 3, 4, 5, 7]
    for coin, wins in data["bars"].items():
        drift = {}
        for h in H:
            vals = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    vals.append(c[i + h] / c[i] - 1)
            drift[h] = np.mean(vals) if vals else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            inprof = (b["regime"].astype(str) != "chop")
            ts = pd.to_datetime(b["timestamp"])
            for h in H:
                for off in range(h):
                    for i in range(off, len(b) - h, h):
                        if np.isnan(z.iloc[i]) or not inprof.iloc[i]:
                            continue
                        fr = c.iloc[i + h] / c.iloc[i] - 1
                        rows.append(dict(coin=coin, win=w, h=h, off=off, z=z.iloc[i],
                                         ex=fr - drift[h], tot=fr, day=ts.iloc[i].normalize(), yr=ts.iloc[i].year))
    df = pd.DataFrame(rows)
    df["zbin"] = pd.cut(df["z"], [-np.inf, -1, -0.5, 0, 0.5, 1, np.inf])

    def tday(g):
        d = g.groupby("day")["ex"].sum()
        n = len(g); m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": len(d), "mean_ex_%": 100 * m, "t_day": m / se if se > 0 else np.nan,
                          "mean_tot_%": 100 * g["tot"].mean()})
    g0 = df[df.off == 0]
    out["grid0_h_zbin"] = g0.groupby(["h", "zbin"], observed=True).apply(tday)
    # offset robustness: mean excess by offset for z<-1 and 0<z<1
    out["falls_z<-1_by_h_off_mean%"] = (df[df.z < -1].groupby(["h", "off"])["ex"].mean() * 100).unstack()
    out["smallrise_0-1_by_h_off_mean%"] = (df[(df.z > 0) & (df.z < 1)].groupby(["h", "off"])["ex"].mean() * 100).unstack()
    out["rise_z>1_by_h_off_mean%"] = (df[df.z > 1].groupby(["h", "off"])["ex"].mean() * 100).unstack()
    f = g0[(g0.z < -1)]
    out["falls_z<-1_grid0_by_coin_h"] = f.groupby(["h", "coin"]).apply(tday)
    out["falls_z<-1_h3_by_year"] = g0[(g0.z < -1) & (g0.h == 3)].groupby("yr").apply(tday)
    s = g0[(g0.z > 0) & (g0.z < 1) & (g0.h == 1)]
    out["smallrise_h1_by_coin"] = s.groupby("coin").apply(tday)
    out["smallrise_h1_by_year"] = s.groupby("yr").apply(tday)
    return out

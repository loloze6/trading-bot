def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        # coin drift per horizon over all windows, non-overlapping grid
        drift = {}
        for h in [1, 2, 3, 5]:
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
            for h in [1, 2, 3, 5]:
                for i in range(0, len(b) - h, h):
                    if np.isnan(z.iloc[i]):
                        continue
                    fr = c.iloc[i + h] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, win=w, h=h, z=z.iloc[i], inprof=bool(inprof.iloc[i]),
                                     ex=fr - drift[h], tot=fr, yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    out["counts"] = df.groupby(["h", "inprof"]).size().unstack()
    df["zbin"] = pd.cut(df["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])

    def summ(g):
        n = len(g); m = g["ex"].mean(); s = g["ex"].std()
        return pd.Series({"n": n, "mean_ex_%": 100 * m, "t": m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan,
                          "mean_tot_%": 100 * g["tot"].mean()})
    ip = df[df.inprof]
    out["inprof_by_h_zbin"] = ip.groupby(["h", "zbin"], observed=True).apply(summ)
    out["outprof_h1_zbin"] = df[(~df.inprof) & (df.h == 1)].groupby("zbin", observed=True).apply(summ)
    sl = []
    for h in [1, 2, 3, 5]:
        g = ip[ip.h == h]
        for side, gg in [("up", g[g.z > 0]), ("down", g[g.z < 0]), ("all", g)]:
            res = stats.linregress(gg["z"], gg["ex"])
            sl.append(dict(h=h, side=side, n=len(gg), slope_pct=100 * res.slope, t=res.slope / res.stderr))
    out["inprof_slopes"] = pd.DataFrame(sl)
    g = ip[(ip.h == 1) & (ip.z > 1)]
    out["inprof_h1_z>1_by_coin"] = g.groupby("coin").apply(summ)
    out["inprof_h1_z>1_by_year"] = g.groupby("yr").apply(summ)
    g3 = ip[(ip.h == 3) & (ip.z > 1)]
    out["inprof_h3_z>1_by_coin"] = g3.groupby("coin").apply(summ)
    out["inprof_all_by_h"] = ip.groupby("h").apply(summ)
    return out

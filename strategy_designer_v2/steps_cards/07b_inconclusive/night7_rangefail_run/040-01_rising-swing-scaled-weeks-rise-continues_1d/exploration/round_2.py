def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values)
            n = len(df)
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            lr = c.pct_change()
            r20 = c / c.shift(20) - 1
            sd20 = lr.rolling(20).std()
            ssr = r20 / (sd20 * np.sqrt(20))
            sd30 = lr.rolling(30).std()
            agit = sd30 > sd30.expanding(30).median()
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            for h in [7, 14, 28]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[i + h] / c[i] - 1,
                                     fc=df["forecast"].values[i], ssr=ssr[i], r20=r20[i],
                                     agit=agit[i] if not np.isnan(sd30[i]) else np.nan,
                                     r60=r60[i], r5=r5[i], inprof=(reg[i] == "unknown"),
                                     year=ts[i].year, day=ts[i].normalize()))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")

    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_ex=g["ex"].mean() if len(g) else np.nan))
        X = g[x] - g[x].mean()
        b = (X * g["ex"]).sum() / (X ** 2).sum()
        a = g["ex"].mean() - b * g[x].mean()
        res = g["ex"] - a - b * g[x]
        s = (X * res).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        dm = g.groupby("day")["ex"].sum()
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), slope=b, t=b / se,
                              mean_ex=g["ex"].mean(), t_mean_day=dm.mean() / (dm.std() / np.sqrt(len(dm))) * 1.0))
    out = {}
    p = d[d.inprof & (d.ssr > 0)].copy()
    out["agit_split"] = p.groupby(["h", "agit"]).apply(lambda g: slope(g, "ssr"))
    out["ssr_le_2_only"] = p[p.ssr <= 2].groupby("h").apply(lambda g: slope(g, "ssr"))
    out["ssr_gt_2_mean"] = p[p.ssr > 2].groupby("h").apply(lambda g: slope(g, "ssr"))
    out["all_inprof_ssr_any"] = d[d.inprof].groupby("h").apply(lambda g: slope(g, "ssr"))
    out["slope_on_r60_inprof"] = d[d.inprof].groupby("h").apply(lambda g: slope(g, "r60"))
    out["slope_on_r5_inprof"] = d[d.inprof].groupby("h").apply(lambda g: slope(g, "r5"))
    q = d[d.inprof & (d.h == 14)].copy()
    q["qb"] = pd.qcut(q["ssr"], 5, labels=False, duplicates="drop")
    out["ssr_q_all_inprof_14"] = q.groupby("qb").agg(n=("ex", "size"), ssr=("ssr", "mean"), ex=("ex", "mean"))
    q2 = d[d.inprof & (d.h == 7) & (d.ssr > 0)].copy()
    q2["qb"] = pd.qcut(q2["ssr"], 5, labels=False, duplicates="drop")
    out["ssr_q_7"] = q2.groupby("qb").agg(n=("ex", "size"), ssr=("ssr", "mean"), ex=("ex", "mean"))
    out["by_year_ssr_14"] = p[p.h == 14].groupby("year").apply(lambda g: slope(g, "ssr"))
    return out

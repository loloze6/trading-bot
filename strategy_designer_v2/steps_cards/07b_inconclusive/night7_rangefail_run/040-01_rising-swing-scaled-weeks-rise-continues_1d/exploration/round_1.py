def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [7, 14, 21, 28]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            raw = df.get("debug_info.components.swing_rise.last_history_value")
            fc = df["forecast"].values
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            # recompute raw swing-scaled 20d return from prices (within window, needs 20 back)
            lr = pd.Series(c).pct_change()
            r20 = pd.Series(c) / pd.Series(c).shift(20) - 1
            sd20 = lr.rolling(20).std()
            ssr = r20 / (sd20 * np.sqrt(20))
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     fwd=c[i + h] / c[i] - 1, fc=fc[i],
                                     raw=(raw.values[i] if raw is not None else np.nan),
                                     ssr=ssr.values[i], r20=r20.values[i],
                                     inprof=(reg[i] == "unknown"),
                                     year=ts[i].year, day=ts[i].normalize()))
    d = pd.DataFrame(rows)
    d["mean_h"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["mean_h"]

    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_ex=g["ex"].mean() if len(g) else np.nan))
        X = g[x] - g[x].mean()
        b = (X * g["ex"]).sum() / (X ** 2).sum()
        a = g["ex"].mean() - b * g[x].mean()
        res = g["ex"] - a - b * g[x]
        s = (X * res).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        tm = g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g)))
        return pd.Series(dict(n=len(g), slope=b, t=b / se, mean_ex=g["ex"].mean(), t_mean=tm))

    act = d[(d.inprof) & (d.fc > 0)]
    out = {}
    out["by_h_fc"] = act.groupby("h").apply(slope)
    act_raw = d[(d.inprof) & (d.ssr > 0)]
    out["by_h_rawssr"] = act_raw.groupby("h").apply(lambda g: slope(g, "ssr"))
    a14 = act[act.h == 14]
    out["by_coin_14"] = a14.groupby("coin").apply(slope)
    out["by_window_14"] = a14.groupby("w").apply(slope)
    out["by_year_14"] = a14.groupby("year").apply(slope)
    q = a14.copy()
    q["qb"] = pd.qcut(q["fc"], 5, labels=False, duplicates="drop")
    out["fc_quintile_14"] = q.groupby("qb").agg(n=("ex", "size"), fc=("fc", "mean"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    r = d[(d.inprof) & (d.ssr > 0) & (d.h == 14)].copy()
    r["qb"] = pd.qcut(r["ssr"], 5, labels=False, duplicates="drop")
    out["ssr_quintile_14"] = r.groupby("qb").agg(n=("ex", "size"), ssr=("ssr", "mean"), ex=("ex", "mean"))
    # all profiles: raw ssr > 0, by profile in/out
    allp = d[(d.h == 14) & (d.ssr > 0)].copy()
    out["ssr_by_inprof_14"] = allp.groupby("inprof").apply(lambda g: slope(g, "ssr"))
    out["n_inprof_fc0_14"] = int(((d.h == 14) & d.inprof & (d.fc == 0)).sum())
    return out

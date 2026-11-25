def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            hl = ((df["high"] - df["low"]) / df["close"]).values
            for i in range(28, n, 5):
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "fc": df["forecast"].iloc[i], "reg": df["regime"].iloc[i],
                     "ret28": c[i] / c[i-28] - 1,
                     "rng": hl[i-27:i+1].mean() / np.nanmean(hl[:i+1])}
                for h in [5, 10]:
                    r[f"f{h}"] = c[i+h] / c[i] - 1 if i + h < n else np.nan
                rows.append(r)
    g = pd.DataFrame(rows)
    for h in [5, 10]:
        g[f"x{h}"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
    d = g[g.ret28 < 0].copy()
    med = d.rng.median()
    d["calm"] = np.where(d.rng <= med, "calm", "wild")
    def cl(dd, y="x5", x="ret28"):
        dd = dd.dropna(subset=[x, y])
        if len(dd) < 20: return pd.Series({"n": len(dd)})
        X = dd[x] - dd[x].mean(); Y = dd[y] - dd[y].mean()
        b = (X*Y).sum() / (X*X).sum()
        e = (Y - b*X) * X
        s = e.groupby(dd["day"]).sum()
        G = len(s)
        se = np.sqrt((s**2).sum() * G/(G-1)) / (X*X).sum()
        return pd.Series({"n": len(dd), "days": G, "slope": b, "t": b/se, "mean_y": dd[y].mean()})
    out = {}
    out["calm_vs_wild_x5"] = d.groupby("calm").apply(cl)
    out["calm_vs_wild_x10"] = d.groupby("calm").apply(lambda z: cl(z, "x10"))
    out["calm_by_year_x5"] = d[d.calm == "calm"].groupby("year").apply(cl)
    out["calm_by_year_x10"] = d[d.calm == "calm"].groupby("year").apply(lambda z: cl(z, "x10"))
    out["calm_by_window_x10"] = d[d.calm == "calm"].groupby("w").apply(lambda z: cl(z, "x10"))
    dc = d[d.calm == "calm"].copy()
    dc["depth"] = pd.qcut(dc.ret28, 3, labels=["deep", "mid", "shallow"])
    out["calm_depth_means"] = dc.groupby("depth")[["ret28", "x5", "x10", "f5", "f10"]].mean()
    out["calm_depth_counts"] = dc.groupby("depth")["x5"].count()
    d["rq"] = pd.qcut(d.rng, 4, labels=["q1calm", "q2", "q3", "q4wild"])
    out["by_range_quartile_x10"] = d.groupby("rq").apply(lambda z: cl(z, "x10"))
    dc["big5"] = dc.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])
    out["calm_default_vs_other_x10"] = dc.groupby("big5").apply(lambda z: cl(z, "x10"))
    out["vol_fc_deep_cl"] = cl(d[(d.reg=="trending") & (d.ret28 < d.ret28.quantile(1/3))], "x5", "fc")
    return out

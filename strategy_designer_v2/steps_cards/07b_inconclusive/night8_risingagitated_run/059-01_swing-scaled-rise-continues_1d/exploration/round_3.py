def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            lr = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol30 = pd.Series(lr).rolling(30, min_periods=30).std().values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(0, n - 5, 5):
                rows.append(dict(coin=coin, w=w, f=f[t], r=c[t + 5] / c[t] - 1, yr=yr[t], vol=vol30[t],
                                 day=str(pd.to_datetime(df["timestamp"].iloc[t]).date()), late=int(t >= 30)))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    d["agit"] = np.where(d["vol"] > d.groupby("coin")["vol"].transform("median"), "agitated", "calm")
    d.loc[d["vol"].isna(), "agit"] = "nowarm"

    def reg(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 20 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g["f"], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    out["by_late"] = d.groupby("late").apply(reg)
    out["by_agit_all"] = d.groupby("agit").apply(reg)
    cm = d[d.agit == "calm"].copy()
    out["calm_by_coin"] = cm.groupby("coin").apply(reg)
    wr = cm.groupby("w").apply(reg)
    out["calm_windows_positive"] = pd.Series(dict(n_windows=len(wr), positive=(wr.slope > 0).sum(), t_ge1=(wr.t > 1).sum()))
    cm = cm[cm.f != 0]
    cm["sx"] = np.sign(cm.f) * cm.ex
    cm["vol5"] = cm["vol"] * np.sqrt(5)
    pday = cm.groupby("day")["sx"].sum()
    out["calm_size"] = pd.Series(dict(cases=len(cm), mean_unusual=cm.sx.mean(), days=len(pday),
                                       t_day=cm.sx.sum() / (pday.std() * np.sqrt(len(pday))) if len(pday) > 1 else np.nan,
                                       strength=(cm.sx / cm.vol5).mean()))
    cm["absq"] = pd.qcut(cm.f.abs(), 3, labels=False)
    out["calm_sx_by_absf"] = cm.groupby("absq")["sx"].agg(n="size", mean="mean", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["calm_by_side"] = cm.groupby(np.sign(cm.f))["ex"].agg(n="size", mean="mean", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    return out

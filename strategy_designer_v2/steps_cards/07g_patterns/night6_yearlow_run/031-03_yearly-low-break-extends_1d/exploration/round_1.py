def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 10
    rows = []
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets); usual[coin] = np.std(rets, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            n = len(c)
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            lo60 = c.shift(1).rolling(60).min()
            hi60 = c.shift(1).rolling(60).max()
            vol20 = r1.rolling(20).std()
            depthcol = "debug_info.components.depth.last_history_value"
            dep = b[depthcol] if depthcol in b.columns else pd.Series(np.nan, index=b.index)
            for i in range(0, n - H, H):
                fwd = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, win=w, ts=b["timestamp"].iloc[i], fwd=fwd,
                    ab=fwd - drift[coin], z=(fwd - drift[coin]) / usual[coin],
                    trend=b["regime"].iloc[i] == "trending", depth=pd.to_numeric(dep.iloc[i], errors="coerce"),
                    r1=r1.iloc[i], r5=r5.iloc[i], r20=r20.iloc[i],
                    d60=c.iloc[i] / lo60.iloc[i] - 1, h60=c.iloc[i] / hi60.iloc[i] - 1,
                    vol=vol20.iloc[i], wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                    yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")

    def summ(g):
        s = g.groupby("day")["ab"].sum()
        nd = len(s); m = g["ab"].mean()
        se = np.sqrt((s ** 2).sum() - 0) / len(g) if len(g) > 1 else np.nan
        # clustered se: sqrt(sum over days (sum dev)^2)/n with dev from mean
        dev = (g["ab"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=nd, mean_ab=m, t=m / se if se > 0 else np.nan,
                              mean_z=g["z"].mean(), mean_fwd=g["fwd"].mean()))

    out = {}
    out["all grid"] = summ(d).to_frame().T
    out["break vs not"] = d.groupby("trend").apply(summ)
    tb = d[d.trend & d.depth.notna()].copy()
    if len(tb) > 5:
        tb["q"] = pd.qcut(tb["depth"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
        out["break by depth tercile"] = tb.groupby("q").apply(summ)
    for col, lab in [("d60", "dist above prior 60d low"), ("h60", "dist below prior 60d high"),
                     ("r1", "1d return"), ("r5", "5d return"), ("r20", "20d return"), ("vol", "20d vol")]:
        x = d.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
        out["by quintile " + lab] = x.groupby("q").apply(summ)
        out["spearman " + lab] = round(stats.spearmanr(x[col], x["ab"]).correlation, 4)
    out["by weekday"] = d.groupby("wd").apply(summ)
    out["by year"] = d.groupby("yr").apply(summ)
    out["by coin"] = d.groupby("coin").apply(summ)
    out["break by coin"] = d[d.trend].groupby("coin").apply(summ)
    return out

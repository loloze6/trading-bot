def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 7
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rs) if rs else np.nan
        usual[coin] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            r30 = pd.Series(c).pct_change(30).values
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30).std().values
            for i in range(0, len(c) - H, H):
                if not (f[i] < 0):
                    continue
                out = {}
                for h in (3, 7, 14, 21):
                    out[f"fwd{h}"] = c[i + h] / c[i] - 1 if i + h < len(c) else np.nan
                rows.append(dict(coin=coin, w=w, year=ts[i].year, day=ts[i].normalize(),
                                 af=abs(f[i]), r30=r30[i], vol30=vol30[i],
                                 drift=drift[coin], usual=usual[coin], **out))
    d = pd.DataFrame(rows)
    d["unus"] = -(d["fwd7"] - d["drift"])
    d["tot"] = -d["fwd7"]
    d["q"] = pd.qcut(d["af"], 3, labels=["low", "mid", "high"])
    d["r30q"] = pd.qcut(d["r30"], 3, labels=["shallow", "mid", "deep"])

    def summ(g):
        n = len(g)
        m = g["unus"].mean()
        t = m / (g["unus"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        wm = (g["unus"] * g["af"]).sum() / g["af"].sum()
        return pd.Series(dict(n=n, unus_mean=m, t=t, w_unus=wm, tot_mean=g["tot"].mean(),
                              share_fall=(g["fwd7"] < 0).mean()))
    res = {}
    res["overall"] = summ(d)
    res["by_coin"] = d.groupby("coin").apply(summ)
    res["by_window"] = d.groupby("w").apply(summ)
    res["by_year"] = d.groupby("year").apply(summ)
    res["by_forecast_tercile"] = d.groupby("q").apply(summ)
    res["by_r30_tercile"] = d.groupby("r30q").apply(summ)
    hz = {}
    for h in (3, 7, 14, 21):
        x = -(d[f"fwd{h}"] - d["drift"] * h / 7)
        x = x.dropna()
        hz[h] = dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))),
                     tot=(-d[f"fwd{h}"]).mean())
    res["horizons"] = pd.DataFrame(hz).T
    res["drift_usual"] = pd.DataFrame(dict(drift=drift, usual=usual))
    d["volq"] = pd.qcut(d["vol30"], 2, labels=["lowvol", "highvol"])
    res["by_vol_half"] = d.groupby("volq").apply(summ)
    res["corr_af_unus"] = pd.Series(dict(spearman=stats.spearmanr(d["af"], d["unus"])[0],
                                         p=stats.spearmanr(d["af"], d["unus"])[1],
                                         sp_r30_fwd7=stats.spearmanr(d["r30"], d["fwd7"], nan_policy="omit")[0]))
    return res

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            nxt = c.shift(-1)/c - 1
            r1 = c/c.shift(1) - 1
            tr60 = c/c.shift(60) - 1
            hi20 = b["high"].astype(float).rolling(20, min_periods=20).max()
            sd20 = r1.rolling(20, min_periods=20).std()
            depth = (hi20 - c)/hi20/sd20
            f = b["forecast"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(len(b)-1):
                if f.iloc[i] < 0 and np.isfinite(nxt.iloc[i]):
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     af=-f.iloc[i], ex=nxt.iloc[i]-mu, r1=r1.iloc[i],
                                     r1z=r1.iloc[i]/sd20.iloc[i] if sd20.iloc[i]>0 else np.nan,
                                     tr=tr60.iloc[i], depth=depth.iloc[i]))
    d = pd.DataFrame(rows)
    def summ(g):
        n = len(g)
        m = -g["ex"].mean()
        t = m/(g["ex"].std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan
        sl = np.polyfit(g["af"], g["ex"], 1)[0] if n > 5 else np.nan
        cr = stats.pearsonr(g["af"], g["ex"])[0] if n > 5 else np.nan
        return pd.Series(dict(n=n, short_mean=m, t_mean=t, slope=sl, corr=cr))
    out = {}
    out["all"] = summ(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("w").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["afq"] = pd.qcut(d["af"], 5, labels=False, duplicates="drop")
    out["by_af_quintile"] = d.groupby("afq").apply(lambda g: pd.Series(dict(n=len(g), af=g["af"].mean(), depth=g["depth"].mean(), short_mean=-g["ex"].mean(), t=-g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))))))
    dd = d.dropna(subset=["depth"]).copy()
    dd["dq"] = pd.qcut(dd["depth"], 5, labels=False, duplicates="drop")
    out["by_rawdepth_quintile"] = dd.groupby("dq").apply(lambda g: pd.Series(dict(n=len(g), depth=g["depth"].mean(), short_mean=-g["ex"].mean(), t=-g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))))))
    dt = d.dropna(subset=["tr"]).copy()
    dt["trend"] = np.where(dt["tr"] > 0.1, "rising", np.where(dt["tr"] < -0.1, "falling", "choppy"))
    out["by_trend"] = dt.groupby("trend").apply(summ)
    dr = d.dropna(subset=["r1z"]).copy()
    dr["rq"] = pd.qcut(dr["r1z"], 4, labels=False)
    out["by_upday_size_q"] = dr.groupby("rq").apply(lambda g: pd.Series(dict(n=len(g), r1z=g["r1z"].mean(), short_mean=-g["ex"].mean(), t=-g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))), corr_af=stats.pearsonr(g["af"], g["ex"])[0])))
    out["corr_rawdepth_ex"] = float(stats.pearsonr(dd["depth"], dd["ex"])[0])
    out["corr_af_rawdepth"] = float(stats.pearsonr(dd["depth"], dd["af"])[0])
    return out

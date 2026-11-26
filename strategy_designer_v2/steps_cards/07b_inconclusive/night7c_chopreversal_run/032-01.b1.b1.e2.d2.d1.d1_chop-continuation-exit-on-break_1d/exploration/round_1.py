def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            for h in [1, 3, 7]:
                fwd = c.shift(-h) / c - 1
                for i in range(n):
                    if df.loc[i, "regime"] != "chop" or np.isnan(fwd.iloc[i]):
                        continue
                    f = df.loc[i, "forecast"]
                    if pd.isna(f) or f == 0:
                        continue
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].date(), h=h, grid=(i % h == 0),
                                     f=f, ex=fwd.iloc[i] - ((1 + mu) ** h - 1), er=er.iloc[i],
                                     z7=r7.iloc[i] / (sd30.iloc[i] * np.sqrt(7)) if sd30.iloc[i] > 0 else np.nan,
                                     sd=sd30.iloc[i]))
    d = pd.DataFrame(rows)
    d["sx"] = np.sign(d.f) * d.ex
    d["side"] = np.where(d.f > 0, "long", "short")
    out = {}
    def tstat(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    d1 = d[d.h == 1].copy()
    d1["m"] = d1.f / 10 * d1.ex
    perday = d1.groupby("day").m.sum()
    out["main_recomputed"] = tstat(perday)
    out["by_coin"] = d1.groupby("coin").sx.apply(tstat).unstack()
    out["by_year"] = d1.groupby("year").sx.apply(tstat).unstack()
    out["by_window"] = d1.groupby("w").sx.apply(tstat).unstack()
    out["by_side"] = d1.groupby("side").sx.apply(tstat).unstack()
    d1["fq"] = pd.qcut(d1.f.abs().rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_absf_tercile"] = d1.groupby("fq").sx.apply(tstat).unstack()
    d1["erq"] = pd.qcut(d1.er, 3, labels=["erlo", "ermid", "erhi"])
    out["by_er_tercile"] = d1.groupby("erq").sx.apply(tstat).unstack()
    d1["z7q"] = pd.qcut(d1.z7.abs(), 3, labels=["zlo", "zmid", "zhi"])
    out["by_absz7_tercile"] = d1.groupby("z7q").sx.apply(tstat).unstack()
    d1["sdq"] = pd.qcut(d1.sd, 3, labels=["vlo", "vmid", "vhi"])
    out["by_vol_tercile"] = d1.groupby("sdq").sx.apply(tstat).unstack()
    hh = d[d.grid]
    out["by_horizon_grid"] = hh.groupby(["h", "side"]).sx.apply(tstat).unstack()
    out["by_horizon_all"] = hh.groupby("h").sx.apply(tstat).unstack()
    return out

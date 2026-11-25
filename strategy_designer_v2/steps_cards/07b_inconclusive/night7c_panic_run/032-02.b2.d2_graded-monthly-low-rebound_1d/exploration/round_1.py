def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            allr.append(c[1:] / c[:-1] - 1)
        coinmean[coin] = np.concatenate(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            hi = df["high"].values.astype(float); lo = df["low"].values.astype(float)
            n = len(df)
            rng = pd.Series((hi - lo) / c)
            mr30 = rng.rolling(30).mean().values
            low30 = pd.Series(lo).shift(1).rolling(30).min().values
            ret30 = np.full(n, np.nan); ret30[30:] = c[30:] / c[:-30] - 1
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].values
            for t in range(n):
                fw = {}
                for h in (1, 2, 3, 5, 10):
                    fw[h] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                rows.append(dict(coin=coin, win=w, year=ts[t].year, day=ts[t].normalize(), f=f[t],
                                 depth=(low30[t] - c[t]) / (mr30[t] * c[t]) if mr30[t] > 0 else np.nan,
                                 ret30=ret30[t], mr30=mr30[t],
                                 **{f"r{h}": fw[h] for h in fw}))
    d = pd.DataFrame(rows)
    for h in (1, 2, 3, 5, 10):
        d[f"x{h}"] = d[f"r{h}"] - d["coin"].map(coinmean) * h
    cases = d[d.f > 0].copy()

    def summ(g, col="x1"):
        v = g[col].dropna()
        if len(v) < 3:
            return pd.Series(dict(n=len(v), mean=v.mean(), t=np.nan))
        return pd.Series(dict(n=len(v), mean=v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))), hit=(v > 0).mean()))

    out = {}
    out["by_coin"] = cases.groupby("coin").apply(summ)
    out["by_window"] = cases.groupby("win").apply(summ)
    out["by_year"] = cases.groupby("year").apply(summ)
    cases["fq"] = pd.qcut(cases.f.rank(method="first"), 4, labels=False)
    out["by_forecast_q"] = cases.groupby("fq").apply(summ)
    cases["dq"] = pd.qcut(cases.depth.rank(method="first"), 4, labels=False)
    out["by_depth_q"] = cases.groupby("dq").apply(summ)
    cases["first"] = cases.groupby(["coin", "win"]).day.diff().dt.days.fillna(99) > 1
    out["first_vs_consecutive"] = cases.groupby("first").apply(summ)
    # horizons on non-overlapping-ish: just all cases (report)
    hz = []
    for h in (1, 2, 3, 5, 10):
        s = summ(cases, f"x{h}"); s["h"] = h; hz.append(s)
    out["horizons_cases"] = pd.DataFrame(hz)
    # comparison: decline (ret30<0) no break
    base = d[(d.ret30 < 0) & ~(d.depth > 0)]
    out["decline_nobreak"] = pd.DataFrame([summ(base, f"x{h}").rename(h) for h in (1, 3, 5)])
    out["ret30_q_cases"] = cases.assign(rq=pd.qcut(cases.ret30, 3, labels=False)).groupby("rq").apply(summ)
    return out

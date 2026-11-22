def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    h = 18
    drift = {}
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - h, h)
            rr.extend(c[idx + h] / c[idx] - 1)
        drift[coin] = np.mean(rr); drift[(coin, "sd")] = np.std(rr)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            f = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            L = np.zeros(n, int)
            for t in range(1, n):
                L[t] = L[t-1] + 1 if r1[t] > 0 else 0
            # coin's own 30-day trend (180 bars) known at t
            for t in range(0, n - h, h):
                if not (f[t] > 0):
                    continue
                tr = c[t] / c[t-180] - 1 if t >= 180 else np.nan
                s = t - L[t] + 1
                vprior = np.nanmean(v[max(0, s-30):s]) if s > 0 else np.nan
                rows.append(dict(coin=coin, win=w, year=yr[t], f=f[t], L=L[t],
                                 ex=c[t+h]/c[t]-1-drift[coin],
                                 st=(c[t+h]/c[t]-1-drift[coin])/drift[(coin,"sd")],
                                 tr=tr,
                                 vrel=v[s:t+1].mean()/vprior if vprior and vprior > 0 else np.nan))
    d = pd.DataFrame(rows)
    def tt(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return pd.Series(dict(n=len(x), mean=np.nan, t=np.nan))
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))))
    out = {}
    d["top"] = d.f >= d.f.quantile(0.6)
    top = d[d.top]
    out["top_by_coin"] = top.groupby("coin").apply(lambda g: tt(g.ex))
    out["top_by_year"] = top.groupby("year").apply(lambda g: tt(g.ex))
    out["top_vs_rest"] = d.groupby("top").apply(lambda g: pd.concat([tt(g.ex), pd.Series({"strength": g.st.mean(), "fmean": g.f.mean()})]))
    d["trq"] = pd.qcut(d.tr, 3, labels=False, duplicates="drop")
    out["by_trend_tercile_top"] = d.groupby(["trq", "top"]).apply(lambda g: tt(g.ex))
    out["trend_tercile_mean"] = d.groupby("trq").tr.mean()
    d["vrq"] = pd.qcut(d.vrel, 3, labels=False, duplicates="drop")
    out["vrel_x_top"] = d.groupby(["vrq", "top"]).apply(lambda g: tt(g.ex))
    out["vrel_top_tercile_by_coin"] = d[d.vrq == 2].groupby("coin").apply(lambda g: tt(g.ex))
    return out

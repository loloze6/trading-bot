def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    # drift per coin, H=7 and H=6, non-overlapping grid of all windows
    drift = {}
    for coin, wins in bars.items():
        r7 = []; r6 = []; r1 = []
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            r7 += [c[i+7]/c[i]-1 for i in range(0, n-7, 7)]
            r6 += [c[i+6]/c[i]-1 for i in range(0, n-6, 6)]
            r1 += [c[i+1]/c[i]-1 for i in range(0, n-1)]
        drift[coin] = dict(d7=np.mean(r7), s7=np.std(r7, ddof=1), d6=np.mean(r6), d1=np.mean(r1))
    rows = []
    for coin, wins in bars.items():
        dd = drift[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values; o = df["open"].values
            f = df["forecast"].fillna(0).values
            n = len(df)
            rng = (h - l) / c
            medr = pd.Series(rng).rolling(30, min_periods=10).median().shift(1).values
            fprev = np.r_[0, f[:-1]]
            sig = (f - fprev) <= -2
            for s in range(0, n, 7):
                idx = [i for i in range(s, min(s+7, n)) if sig[i]]
                if not idx: continue
                i = idx[0]
                if i + 8 >= n: 
                    if i + 7 >= n: continue
                    r18 = np.nan
                else:
                    r18 = -(c[i+8]/c[i+1]-1 - dd["d7"])
                loc = (h[i]-c[i])/(h[i]-l[i]) if h[i] > l[i] else np.nan
                rows.append(dict(coin=coin, win=w, ts=str(df["timestamp"].iloc[i])[:10],
                    year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                    u07=-(c[i+7]/c[i]-1 - dd["d7"]), u01=-(c[i+1]/c[i]-1 - dd["d1"]),
                    u17=-(c[i+7]/c[i+1]-1 - dd["d6"]), u18=r18,
                    fc=abs(f[i]), loc=loc, wide=rng[i]/medr[i] if medr[i] > 0 else np.nan,
                    down=c[i] < o[i], ret_day=c[i]/o[i]-1))
    R = pd.DataFrame(rows)
    def tstat(sub, col):
        sub = sub[sub[col].notna()]
        g = sub.groupby("ts")[col].sum(); m = sub[col].mean(); n = len(sub)
        se = g.std(ddof=1)*np.sqrt(len(g))/n if len(g) > 1 else np.nan
        return pd.Series(dict(n=n, days=len(g), mean=m, t=m/se if se else np.nan))
    out = {}
    out["cases_all_horizons"] = pd.DataFrame({k: tstat(R, k) for k in ["u07", "u01", "u17", "u18"]}).T
    R["wq"] = pd.qcut(R["wide"], 3, labels=["narrow", "mid", "wide"])
    out["by_range_width"] = R.groupby("wq").apply(lambda s: pd.concat([tstat(s, "u07").add_prefix("07_"), tstat(s, "u18")[["mean", "t"]].add_prefix("18_")]))
    out["by_down_day"] = R.groupby("down").apply(lambda s: pd.concat([tstat(s, "u07").add_prefix("07_"), tstat(s, "u18")[["mean", "t"]].add_prefix("18_")]))
    R["fq"] = pd.qcut(R["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_forecast_tercile"] = R.groupby("fq").apply(lambda s: pd.concat([tstat(s, "u07").add_prefix("07_"), tstat(s, "u18")[["mean", "t"]].add_prefix("18_")]))
    out["by_year"] = R.groupby("year").apply(lambda s: pd.concat([tstat(s, "u07").add_prefix("07_"), tstat(s, "u18")[["mean", "t"]].add_prefix("18_")]))
    out["by_coin_07"] = R.groupby("coin").apply(lambda s: tstat(s, "u07"))
    return out

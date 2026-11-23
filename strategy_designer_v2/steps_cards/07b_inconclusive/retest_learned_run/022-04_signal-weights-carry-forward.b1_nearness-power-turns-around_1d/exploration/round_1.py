def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def cases(h):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(df) - h, h):
                    rows.append((coin, w, ts.iloc[i].year, f[i], c[i+h]/c[i]-1))
        d = pd.DataFrame(rows, columns=["coin","win","year","fc","ret"])
        d["drift"] = d.groupby("coin")["ret"].transform("mean")
        d["ex"] = d["ret"] - d["drift"]
        d["prod"] = d["fc"]/10*d["ex"]
        return d
    def summ(g):
        x = g["prod"].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    d5 = cases(5)
    out["all_h5"] = summ(d5)
    out["by_coin"] = d5.groupby("coin").apply(summ)
    out["by_year"] = d5.groupby("year").apply(summ)
    d5["side"] = np.where(d5["fc"] > 0, "long", np.where(d5["fc"] < 0, "short", "flat"))
    out["by_side"] = d5.groupby("side").apply(summ)
    a = d5[d5["fc"] != 0].copy()
    a["q"] = pd.qcut(a["fc"].abs(), 5, labels=False)
    out["by_absfc_quintile"] = a.groupby("q").apply(summ)
    a["vq"] = a.groupby("coin")["ret"].transform(lambda s: s.abs().rolling(1).mean())
    hz = {}
    for h in [1, 3, 5, 10, 20]:
        hz[h] = summ(cases(h))
    out["by_horizon"] = pd.DataFrame(hz).T
    # first half vs second half of each window
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            n = len(df)
            for i in range(0, n-5, 5):
                rows.append((coin, "first" if i < n/2 else "second", df["forecast"].iloc[i], df["close"].iloc[i+5]/df["close"].iloc[i]-1))
    e = pd.DataFrame(rows, columns=["coin","half","fc","ret"])
    e["ex"] = e["ret"] - e.groupby("coin")["ret"].transform("mean")
    e["prod"] = e["fc"]/10*e["ex"]
    out["by_window_half"] = e.groupby("half").apply(summ)
    out["corr_fc_ex_h5"] = float(stats.spearmanr(d5["fc"], d5["ex"], nan_policy="omit")[0])
    return out

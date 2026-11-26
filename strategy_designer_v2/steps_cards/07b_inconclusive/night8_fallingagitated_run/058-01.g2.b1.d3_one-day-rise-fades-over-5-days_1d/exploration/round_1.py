def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in [1, 2, 3, 5, 10]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            s1 = r1 / sd
            r3 = c / c.shift(3) - 1
            s3 = r3 / (sd * np.sqrt(3))
            act = (df["regime"] == "unknown").values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 2, 3, 5, 10]:
                for start in range(0, n, h):
                    for t in range(start, min(start + h, n)):
                        if act[t] and r1.iloc[t] > 0 and t + h < n and not np.isnan(s1.iloc[t]):
                            ret = c.iloc[t + h] / c.iloc[t] - 1
                            m, s = drift[(coin, h)]
                            rows.append(dict(coin=coin, w=w, h=h, day=str(df["timestamp"].iloc[t])[:10],
                                             year=yr[t], s1=s1.iloc[t], s3=s3.iloc[t],
                                             unus=-(ret - m), tot=-ret, strength=-(ret - m) / s))
                            break
    d = pd.DataFrame(rows)

    def clt(g):
        x = g["unus"]; mu = x.mean()
        dev = (x - mu).groupby(g["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(x) if D > 1 else np.nan
        return pd.Series(dict(n=len(x), days=D, mean_unus=mu, t=mu / se if se else np.nan,
                              mean_tot=g["tot"].mean(), strength=g["strength"].mean()))
    out = {}
    out["by_horizon"] = d.groupby("h").apply(clt)
    d5 = d[d.h == 5].copy()
    d5["q1"] = pd.qcut(d5["s1"], 4, labels=False)
    out["h5_by_s1_quartile"] = d5.groupby("q1").apply(clt)
    d5["q3"] = pd.qcut(d5["s3"], 4, labels=False)
    out["h5_by_s3_quartile"] = d5.groupby("q3").apply(clt)
    out["h5_by_coin"] = d5.groupby("coin").apply(clt)
    out["h5_by_year"] = d5.groupby("year").apply(clt)
    out["h5_by_window"] = d5.groupby("w").apply(clt)
    for h in [2, 10]:
        dh = d[d.h == h].copy()
        dh["q3"] = pd.qcut(dh["s3"], 4, labels=False)
        out[f"h{h}_by_s3_quartile"] = dh.groupby("q3").apply(clt)
    out["corr_s1_unus_h5"] = float(d5[["s1", "unus"]].corr().iloc[0, 1])
    out["corr_s3_unus_h5"] = float(d5[["s3", "unus"]].corr().iloc[0, 1])
    return out

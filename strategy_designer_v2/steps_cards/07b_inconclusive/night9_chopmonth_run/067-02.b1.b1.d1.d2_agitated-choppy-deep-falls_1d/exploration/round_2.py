def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r30 = c / c.shift(30) - 1
            for h in (3, 5, 7, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     day=str(df["timestamp"].iloc[i])[:10],
                                     inprof=(df["regime"].iloc[i] == "unknown"),
                                     fc=df["forecast"].iloc[i], r30=r30.iloc[i], fwd=fwd.iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["ex"] = d["fwd"] - d["drift"]
    out = {}

    def summ(g, sign=-1):
        x = sign * g["ex"]
        dd = (x - x.mean()).groupby(g["day"]).sum()
        K = len(dd)
        se = np.sqrt((dd ** 2).sum() * K / max(K - 1, 1)) / len(x) if len(x) > 1 else np.nan
        return pd.Series(dict(n=len(x), days=K, mean=x.mean(), t=x.mean() / se if se else np.nan,
                              total=(sign * g["fwd"]).mean()))

    p = d[d.inprof & d.r30.notna()].copy()
    f = p[p.r30 < 0].copy()
    out["fall_by_h"] = f.groupby("h").apply(summ)
    f5 = f[f.h == 5].copy()
    f5["bin"] = pd.qcut(f5.r30, 3, duplicates="drop")
    out["fall_h5_by_r30_tercile"] = f5.groupby("bin").apply(summ)
    out["fall_h5_by_coin"] = f5.groupby("coin").apply(summ)
    out["fall_h5_by_window"] = f5.groupby("w").apply(summ)
    f5["year"] = f5.day.str[:4]
    out["fall_h5_by_year"] = f5.groupby("year").apply(summ)
    out["corr_r30_ex_fall_h5"] = float(f5[["r30", "ex"]].corr().iloc[0, 1])
    out["corr_r30_ex_all_inprof_h5"] = float(p[p.h == 5][["r30", "ex"]].corr().iloc[0, 1])
    out["inprof_h5_counts_side"] = p[p.h == 5].assign(s=np.sign(p[p.h == 5].r30)).groupby("s").apply(summ)
    return out

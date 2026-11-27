def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        for H in [5, 10]:
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr.extend((c[idx + H] / c[idx] - 1).tolist())
            drift[(coin, H)] = np.mean(allr)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            st = (c / c.rolling(20).mean() - 1) / r.rolling(20).std()
            tr = (c / c.shift(60) - 1) * 100
            ts = pd.to_datetime(df["timestamp"])
            for H in [5, 10]:
                idx = np.arange(0, len(c) - H, H)
                fwd = c.values[idx + H] / c.values[idx] - 1
                for k, i in enumerate(idx):
                    rows.append(dict(coin=coin, w=w, H=H, year=ts.iloc[i].year,
                                     reg=df["regime"].iloc[i], st=st.iloc[i], tr=tr.iloc[i],
                                     fwd=fwd[k], ex=fwd[k] - drift[(coin, H)]))
    d = pd.DataFrame(rows).dropna(subset=["st", "tr"])
    d["trend"] = np.where(d.tr > 10, "rising", np.where(d.tr < -10, "falling", "choppy"))
    d["side"] = np.where(d.st < 0, "below", "above")
    d["dir_ex"] = np.where(d.st < 0, -d.ex, d.ex)  # carry direction
    def summ(g):
        n = len(g)
        x = g["dir_ex"]
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        rho = stats.spearmanr(g["st"], g["ex"])[0] if n > 5 else np.nan
        return pd.Series(dict(n=n, mean_ex=g["ex"].mean(), carry_ex=x.mean(), t_carry=t, spearman_st_ex=rho))
    out = {}
    out["by_H_trend_side"] = d.groupby(["H", "trend", "side"]).apply(summ)
    out["by_H_trend_all"] = d.groupby(["H", "trend"]).apply(summ)
    c5 = d[(d.trend == "choppy") & (d.H == 5)].copy()
    c5["q"] = pd.qcut(c5["st"], 5, labels=False)
    out["choppy_H5_quintiles"] = c5.groupby("q").apply(summ)
    out["choppy_H5_by_year"] = c5.groupby("year").apply(summ)
    out["choppy_H5_by_coin"] = c5.groupby("coin").apply(summ)
    out["choppy_H5_by_reg"] = c5.groupby(["reg", "side"]).apply(summ)
    ip = d[(d.H == 5) & (d.reg == "unknown")]
    out["inprof_H5_all_bars_mean_ex"] = pd.Series(dict(n=len(ip), mean_ex=ip.ex.mean(),
                                         t=ip.ex.mean() / (ip.ex.std() / np.sqrt(len(ip)))))
    return out

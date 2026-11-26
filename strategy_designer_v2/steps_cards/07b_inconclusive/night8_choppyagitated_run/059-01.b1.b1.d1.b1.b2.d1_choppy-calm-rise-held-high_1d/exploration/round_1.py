def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 3, 7, 14]
    # normal drift per coin per horizon (non-overlapping, all windows seen)
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            cl = df["close"].values
            n = len(df)
            r7 = pd.Series(cl).pct_change(7)
            sc = r7 / r7.abs().rolling(30).mean()
            hi7 = pd.Series(cl).rolling(7).max()
            yr = pd.Timestamp(df["timestamp"].iloc[0]).year
            low = 0.0; last_cell = -1
            for t in range(n):
                if f[t] <= 0:
                    low = 0.0
                    continue
                low = min(low, f[t])
                cell = t // 7
                if f[t] - low >= 2 and cell != last_cell and t + 7 < n:
                    last_cell = cell
                    rec = dict(coin=c, win=w, year=yr, fc=f[t], sc=sc.iloc[t],
                               wd=pd.Timestamp(df["timestamp"].iloc[t]).weekday(),
                               r7past=r7.iloc[t], day=str(df["timestamp"].iloc[t])[:10])
                    for h in H:
                        if t + h < n:
                            rec[f"u{h}"] = cl[t + h] / cl[t] - 1 - drift[(c, h)]
                            rec[f"tot{h}"] = cl[t + h] / cl[t] - 1
                    rec["str7"] = rec["u7"] / usual[(c, 7)]
                    rows.append(rec)
                    low = f[t]
    d = pd.DataFrame(rows)
    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by horizon"] = pd.DataFrame({f"u{h}": tstat(d[f"u{h}"]) for h in H} | {f"tot{h}": tstat(d[f"tot{h}"]) for h in H}).T
    dp = d.groupby("day")["u7"].sum()
    out["u7 day pooled"] = tstat(dp)
    out["by coin"] = d.groupby("coin")["u7"].apply(tstat).unstack()
    out["by window"] = d.groupby("win")["u7"].apply(tstat).unstack()
    out["by year"] = d.groupby("year")["u7"].apply(tstat).unstack()
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by forecast quartile"] = d.groupby("fq")[["u1", "u3", "u7", "u14"]].mean().join(d.groupby("fq")["u7"].apply(tstat).unstack())
    d["sq"] = pd.qcut(d["sc"].rank(method="first"), 4, labels=["s1", "s2", "s3", "s4"])
    out["by scaled rise quartile"] = d.groupby("sq")[["sc", "u1", "u3", "u7", "u14"]].mean().join(d.groupby("sq")["u7"].apply(tstat).unstack())
    out["corr"] = pd.Series({"spearman fc~u7": d[["fc", "u7"]].corr("spearman").iloc[0, 1],
                             "spearman sc~u7": d[["sc", "u7"]].corr("spearman").iloc[0, 1],
                             "spearman sc~u14": d[["sc", "u14"]].corr("spearman").iloc[0, 1],
                             "median u7": d["u7"].median(), "share u7>0": (d["u7"] > 0).mean(),
                             "mean str7": d["str7"].mean()})
    return out

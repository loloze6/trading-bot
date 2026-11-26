def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # drift: non-overlapping 20-bar returns over all visible windows
        dr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 20, 20):
                dr.append(c[i + 20] / c[i] - 1)
        drift = np.mean(dr) if dr else np.nan
        usual = np.std(dr, ddof=1) if len(dr) > 1 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            net = (c - c.shift(60)).abs()
            path = c.diff().abs().rolling(60).sum()
            er = net / path
            ph = h.shift(1).rolling(60).max()
            pl = l.shift(1).rolling(60).min()
            sit = (er <= 0.3) & (c > ph)
            fc = df["forecast"] if "forecast" in df else pd.Series(0, index=df.index)
            flat = narrow = None
            for col in df.columns:
                if "components" in col and "flat" in col and "post_pipeline" in col:
                    flat = df[col]
                if "components" in col and "narrow" in col and "post_pipeline" in col:
                    narrow = df[col]
            n = len(df)
            for start in range(0, n, 20):
                idx = [i for i in range(start, min(start + 20, n)) if bool(sit.iloc[i]) and i + 20 < n]
                if not idx:
                    continue
                i = idx[0]
                r = c.iloc[i + 20] / c.iloc[i] - 1
                rows.append(dict(coin=coin, window=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                                 ret=r, unusual=r - drift, strength=(r - drift) / usual,
                                 er=er.iloc[i], brk=c.iloc[i] / ph.iloc[i] - 1,
                                 width=(ph.iloc[i] - pl.iloc[i]) / c.iloc[i],
                                 fc=fc.iloc[i],
                                 flat=np.nan if flat is None else pd.to_numeric(flat.iloc[i], errors="coerce"),
                                 narrow=np.nan if narrow is None else pd.to_numeric(narrow.iloc[i], errors="coerce"),
                                 ret5=c.iloc[i + 5] / c.iloc[i] - 1 if i + 5 < n else np.nan,
                                 ret10=c.iloc[i + 10] / c.iloc[i] - 1 if i + 10 < n else np.nan))
    d = pd.DataFrame(rows)
    def summ(g):
        dd = g.groupby("day")["unusual"].sum()
        m = g["unusual"].mean()
        t = m / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(g)) if len(dd) > 1 else np.nan
        return pd.Series(dict(n=len(g), days=len(dd), mean_unusual=m, t=t, mean_total=g["ret"].mean(),
                              hit=(g["ret"] > 0).mean()))
    out = {"all": summ(d)}
    for v in ["er", "brk", "width", "fc", "flat", "narrow"]:
        x = d.dropna(subset=[v])
        if len(x) > 20 and x[v].nunique() > 3:
            x = x.assign(q=pd.qcut(x[v].rank(method="first"), 3, labels=["low", "mid", "high"]))
            res = x.groupby("q").apply(summ)
            res["var_mean"] = x.groupby("q")[v].mean()
            out["by_" + v] = res
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["horizons"] = pd.Series(dict(r5=d["ret5"].mean(), r10=d["ret10"].mean(), r20=d["ret"].mean()))
    out["corr_spearman"] = d[["unusual", "er", "brk", "width", "fc", "flat", "narrow"]].corr(method="spearman")["unusual"]
    return out

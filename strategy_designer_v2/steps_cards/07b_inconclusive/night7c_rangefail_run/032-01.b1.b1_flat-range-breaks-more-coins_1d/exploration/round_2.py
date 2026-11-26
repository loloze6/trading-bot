def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        dr = {10: [], 20: []}
        for w, df in wins.items():
            c = df["close"].values
            for H in (10, 20):
                for i in range(0, len(c) - H, H):
                    dr[H].append(c[i + H] / c[i] - 1)
        drift = {H: np.mean(dr[H]) for H in dr}
        usual = {H: np.std(dr[H], ddof=1) for H in dr}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            er = (c - c.shift(60)).abs() / c.diff().abs().rolling(60).sum()
            ph = h.shift(1).rolling(60).max(); pl = l.shift(1).rolling(60).min()
            ph180 = h.shift(2).rolling(180, min_periods=100).max(); pl180 = l.shift(2).rolling(180, min_periods=100).min()
            comp = (ph180 - pl180) / (ph - pl)
            sit = (er <= 0.3) & (c > ph)
            narrow = None
            for col in df.columns:
                if "components" in col and "narrow" in col and "post_pipeline" in col:
                    narrow = pd.to_numeric(df[col], errors="coerce")
            n = len(df)
            for H in (10, 20):
                for start in range(0, n, H):
                    idx = [i for i in range(start, min(start + H, n)) if bool(sit.iloc[i]) and i + H < n]
                    if not idx:
                        continue
                    i = idx[0]
                    r = c.iloc[i + H] / c.iloc[i] - 1
                    rows.append(dict(H=H, coin=coin, window=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                                     ret=r, unusual=r - drift[H], strength=(r - drift[H]) / usual[H],
                                     narrow=np.nan if narrow is None else narrow.iloc[i],
                                     comp=comp.iloc[i], width=(ph.iloc[i] - pl.iloc[i]) / c.iloc[i]))
    d = pd.DataFrame(rows)
    def summ(g):
        dd = g.groupby("day")["unusual"].sum()
        m = g["unusual"].mean()
        t = m / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(g)) if len(dd) > 1 else np.nan
        return pd.Series(dict(n=len(g), days=len(dd), mean_unusual=m, t=t, strength=g["strength"].mean()))
    out = {}
    for H in (10, 20):
        x = d[d.H == H]
        out[f"all_H{H}"] = summ(x)
        for v in ["narrow", "comp", "width"]:
            y = x.dropna(subset=[v])
            if len(y) > 15:
                y = y.assign(q=pd.qcut(y[v].rank(method="first"), 2, labels=["low", "high"]))
                out[f"H{H}_by_{v}"] = y.groupby("q").apply(summ)
                out[f"H{H}_{v}_by_year_half"] = y.groupby(["year", "q"]).apply(summ)[["n", "mean_unusual"]] if v == "comp" else "skip"
        out[f"H{H}_spearman"] = x[["unusual", "narrow", "comp", "width"]].corr(method="spearman")["unusual"]
    return out

def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}

    def ctime(df_, col):
        x = df_[col].values
        n = len(x)
        if n < 5:
            return np.nan
        m = x.mean()
        s = pd.Series(x - m).groupby(df_["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / n
        return m / se if se > 0 else np.nan

    def build(h):
        rows = []
        for coin, ws in bars.items():
            grid_rets = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    grid_rets.append(c[i + h] / c[i] - 1)
            drift = np.mean(grid_rets)
            usual = np.std(grid_rets, ddof=1)
            for w, df in ws.items():
                c = df["close"].values
                f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"])
                r20 = pd.Series(c).pct_change(20).values
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]):
                        continue
                    fr = c[i + h] / c[i] - 1
                    rows.append(dict(
                        coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                        f=f[i], val=f[i] / 10 * (fr - drift),
                        dirx=np.sign(f[i]) * (fr - drift),
                        tot=np.sign(f[i]) * fr,
                        strength=np.sign(f[i]) * (fr - drift) / usual,
                        r20=r20[i]))
        return pd.DataFrame(rows)

    def summ(g):
        return pd.Series({
            "n": len(g), "days": g["day"].nunique(),
            "main": g["val"].mean(), "t_main": ctime(g, "val"),
            "dirx": g["dirx"].mean(), "t_dirx": ctime(g, "dirx"),
            "tot": g["tot"].mean(), "strength": g["strength"].mean(),
        })

    hz = {}
    for h in [5, 10, 20]:
        d = build(h)
        hz[(h, "long")] = summ(d[d["f"] > 0])
        hz[(h, "short")] = summ(d[d["f"] < 0])
    out["by horizon x side"] = pd.DataFrame(hz).T

    d = build(10)
    L = d[d["f"] > 0].copy()
    S = d[d["f"] < 0].copy()
    out["long by year"] = L.groupby("year").apply(summ)
    out["short by year"] = S.groupby("year").apply(summ)
    L["fq"] = pd.qcut(L["f"], 4, labels=["q1", "q2", "q3", "q4"])
    out["long by forecast quartile"] = L.groupby("fq").apply(summ)
    S["fq"] = pd.qcut(S["f"].abs(), 4, labels=["q1", "q2", "q3", "q4"])
    out["short by |forecast| quartile"] = S.groupby("fq").apply(summ)
    out["long r20 quartile"] = L.groupby(pd.qcut(L["r20"], 4, labels=["a1","a2","a3","a4"])).apply(summ)
    # spearman of forecast vs drift-removed fwd ret on long side
    from scipy.stats import spearmanr
    out["long spearman f vs dirx"] = float(spearmanr(L["f"], L["dirx"]).correlation)
    out["short spearman |f| vs dirx"] = float(spearmanr(S["f"].abs(), S["dirx"]).correlation)
    out["long main excl 2021"] = summ(L[L["year"] != 2021])
    return out

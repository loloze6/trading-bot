def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}

    def ctime(df_, col):
        # day-clustered t of the mean of df_[col]
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
            # the coin's normal drift: mean h-bar return on the grid, over all its windows
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
                r60 = pd.Series(c).pct_change(60).values
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]):
                        continue
                    fr = c[i + h] / c[i] - 1
                    rows.append(dict(
                        coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                        f=f[i], val=f[i] / 10 * (fr - drift),
                        dirx=np.sign(f[i]) * (fr - drift),
                        strength=np.sign(f[i]) * (fr - drift) / usual,
                        r20=r20[i], r60=r60[i]))
        return pd.DataFrame(rows)

    def summ(g):
        return pd.Series({
            "n": len(g),
            "days": g["day"].nunique(),
            "main": g["val"].mean(),
            "t_main": ctime(g, "val"),
            "dirx": g["dirx"].mean(),
            "t_dirx": ctime(g, "dirx"),
            "strength": g["strength"].mean(),
        })

    # the main measure over other horizons
    hz = {}
    for h in [5, 10, 20, 30]:
        d = build(h)
        hz[h] = summ(d)
    out["by horizon"] = pd.DataFrame(hz).T

    d = build(10)
    d["side"] = np.where(d["f"] > 0, "long", "short")
    out["by side"] = d.groupby("side").apply(summ)
    out["by year"] = d.groupby("year").apply(summ)
    out["by coin"] = d.groupby("coin").apply(summ)

    d["fq"] = pd.qcut(d["f"].abs(), 4, labels=["q1", "q2", "q3", "q4"])
    out["by |forecast| quartile"] = d.groupby("fq").apply(summ)

    dd = d.dropna(subset=["r60"]).copy()
    dd["r60q"] = pd.qcut(dd["r60"].abs(), 4, labels=["a1", "a2", "a3", "a4"])
    out["by |r60| quartile"] = dd.groupby("r60q").apply(summ)

    dd["r60side"] = np.where(dd["r60"] > 0, "60d up", "60d down")
    out["by 60d side x |forecast| half"] = dd.groupby(
        ["r60side", dd["f"].abs() > dd["f"].abs().median()]).apply(summ)

    # forecast sign versus raw 20-day return sign, as a check of the regime
    out["share agree sign f vs r20"] = float(
        (np.sign(d["f"]) == np.sign(d["r20"])).mean())
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            near30 = s / s.rolling(30).max()
            vol30 = r1.rolling(30).std()
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], ret=c[i + h] / c[i] - 1,
                                     r1=r1.iloc[i], near=near30.iloc[i], vol=vol30.iloc[i],
                                     pos=i / n, year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    sd = d.groupby(["coin", "h"])["ret"].transform("std")
    d["str"] = d["ex"] / sd

    def tstat(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    out = {}
    # 1-day reversal size: ex return in direction of -r1, by quintile of |r1/vol|
    for h in [1, 5]:
        g = d[(d.h == h)].dropna(subset=["r1", "vol"]).copy()
        g["z"] = g.r1 / g.vol
        g["q"] = pd.qcut(g.z.abs(), 5, labels=False)
        g["sex"] = -np.sign(g.r1) * g.ex
        g["sstr"] = -np.sign(g.r1) * g["str"]
        t = g.groupby("q")["sex"].apply(tstat).unstack()
        t["strength"] = g.groupby("q")["sstr"].mean()
        out[f"reversal_by_absz_q_h{h}"] = t
    # near 30-day high: ex return by quintile of near, 5 and 10 days
    for h in [5, 10]:
        g = d[d.h == h].dropna(subset=["near"]).copy()
        g["q"] = pd.qcut(g.near, 5, labels=False, duplicates="drop")
        out[f"near30_q_h{h}"] = g.groupby("q")["ex"].apply(tstat).unstack()
        rows2 = []
        for coin, gg in g.groupby("coin"):
            rows2.append(dict(coin=coin, rho=stats.spearmanr(gg.near, gg.ex)[0], n=len(gg)))
        out[f"near30_ic_coin_h{h}"] = pd.DataFrame(rows2).set_index("coin")
        rows2 = []
        for y, gg in g.groupby("year"):
            rows2.append(dict(year=y, rho=stats.spearmanr(gg.near, gg.ex)[0], n=len(gg)))
        out[f"near30_ic_year_h{h}"] = pd.DataFrame(rows2).set_index("year")
    # composite: signed ex by forecast decile and by vol regime
    a5 = d[(d.h == 5) & (d.f != 0)].dropna(subset=["vol"]).copy()
    a5["sex"] = np.sign(a5.f) * a5.ex
    a5["vq"] = a5.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["composite_by_volterc"] = a5.groupby("vq")["sex"].apply(tstat).unstack()
    a5["half"] = np.where(a5.pos < 0.5, "first", "second")
    out["composite_by_windowhalf"] = a5.groupby("half")["sex"].apply(tstat).unstack()
    # forecast sign persistence
    out["mean_abs_forecast"] = float(d[d.h == 1].f.abs().mean())
    return out

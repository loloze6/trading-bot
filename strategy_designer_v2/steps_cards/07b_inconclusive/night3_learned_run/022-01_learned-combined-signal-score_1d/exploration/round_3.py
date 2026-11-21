def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            vol30 = r1.rolling(30).std()
            for h in [1, 5]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, h=h, f=f[i], ret=c[i + h] / c[i] - 1,
                                     r1=r1.iloc[i], vol=vol30.iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    d["sd"] = d.groupby(["coin", "h"])["ret"].transform("std")

    def tstat(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    out = {}
    for h in [1, 5]:
        g = d[d.h == h].dropna(subset=["r1", "vol"]).copy()
        g["z"] = g.r1 / g.vol
        g["q"] = pd.qcut(g.z.abs(), 5, labels=False)
        g["sex"] = -np.sign(g.r1) * g.ex
        g["sstr"] = -np.sign(g.r1) * g.ex / g.sd
        g["dir"] = np.where(g.r1 > 0, "up_day", "down_day")
        top = g[g.q == 4]
        out[f"top_rev_by_coin_h{h}"] = top.groupby("coin")["sex"].apply(tstat).unstack()
        out[f"top_rev_by_year_h{h}"] = top.groupby("year")["sex"].apply(tstat).unstack()
        out[f"rev_by_q_dir_h{h}"] = g.groupby(["dir", "q"])["sex"].apply(tstat).unstack()
    a5 = d[(d.h == 5) & (d.f != 0)].dropna(subset=["vol"]).copy()
    a5["sex"] = np.sign(a5.f) * a5.ex
    a5["vq"] = a5.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    lo = a5[a5.vq == 0]
    out["composite_lowvol_by_year"] = lo.groupby("year")["sex"].apply(tstat).unstack()
    out["composite_lowvol_by_coin"] = lo.groupby("coin")["sex"].apply(tstat).unstack()
    return out

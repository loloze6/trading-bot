def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [24, 72, 168]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(df)
            vs = pd.Series(v)
            tot = vs.rolling(72).sum().values
            top3 = vs.rolling(72).apply(lambda x: np.sort(x)[-3:].sum(), raw=True).values
            share = top3 / tot
            ret72 = np.full(n, np.nan); ret72[72:] = c[72:] / c[:-72] - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in hs:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr[i], regime=df["regime"].iat[i],
                                     fc=df["forecast"].iat[i], share=share[i], r72=ret72[i],
                                     fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    def split(g, col):
        g = g.dropna(subset=[col, "ex"])
        if len(g) < 20: return pd.Series(dict(n=len(g)))
        m = g[col].median()
        a = g[g[col] > m]["ex"]; b = g[g[col] <= m]["ex"]
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        return pd.Series(dict(n=len(g), diff=a.mean() - b.mean(), t=t, top=a.mean(), bot=b.mean()))
    mr = d[d.regime == "mean_reversion"]
    out["by_h_forecast"] = mr.groupby("h").apply(lambda g: split(g, "fc"))
    out["by_h_rawshare"] = mr.groupby("h").apply(lambda g: split(g, "share"))
    m72 = mr[mr.h == 72].copy()
    out["by_coin"] = m72.groupby("coin").apply(lambda g: split(g, "fc"))
    out["by_year"] = m72.groupby("year").apply(lambda g: split(g, "fc"))
    m72["fallq"] = pd.qcut(m72["r72"], 3, labels=["deep", "mid", "shallow"])
    out["by_fall_tercile"] = m72.groupby("fallq").apply(lambda g: split(g, "fc"))
    m72["fq"] = pd.qcut(m72["fc"].rank(method="first"), 5, labels=False)
    out["fc_quintile_mean_ex"] = m72.groupby("fq")["ex"].agg(["count", "mean", "std"])
    out["mr_mean_ex_by_h"] = mr.groupby("h")["ex"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    up = d[(d.h == 72) & (d.r72 > 0)]
    out["up_moves_share_split"] = split(up, "share").to_frame("up72")
    return out

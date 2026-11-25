def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 5, 5):
                g.append(c[i + 5] / c[i] - 1)
        drift[coin] = (np.mean(g), np.std(g))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            lr = c.pct_change()
            vol20 = lr.rolling(20).std()
            r5 = c / c.shift(5) - 1
            z = r5 / vol20
            r20 = c / c.shift(20) - 1
            n = len(df)
            for i in range(n):
                f = {}
                for h in (1, 3, 5, 10, 20):
                    f[h] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                rows.append(dict(coin=coin, win=w, pos=i, cell=i // 5,
                    year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                    day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                    regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                    z=z.iloc[i], r20=r20.iloc[i], vol20=vol20.iloc[i],
                    **{f"f{h}": f[h] for h in f}))
    R = pd.DataFrame(rows)
    R["dr"] = R.coin.map(lambda k: drift[k][0])
    R["sd"] = R.coin.map(lambda k: drift[k][1])
    # cases: forecast<0 first per 5 cell
    C = R[(R.fc < 0)].sort_values(["coin", "win", "pos"]).groupby(["coin", "win", "cell"]).head(1).copy()
    C = C[C.f5.notna()]
    C["u"] = -(C.f5 - C.dr)
    C["tot"] = -C.f5

    def tday(df, col="u"):
        d = df.dropna(subset=[col])
        if len(d) < 5:
            return pd.Series(dict(n=len(d), mean=d[col].mean(), t=np.nan, days=d.day.nunique()))
        m = d[col].mean()
        s = (d[col] - m).groupby(d.day).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), mean=m, t=m / se, days=D))

    out = {}
    out["all"] = tday(C)
    out["by_window"] = C.groupby("win").apply(tday)
    out["by_coin"] = C.groupby("coin").apply(tday)
    out["by_year"] = C.groupby("year").apply(tday)
    C["fq"] = pd.qcut(C.fc.abs().rank(method="first"), 4, labels=False)
    out["by_fc_quart"] = C.groupby("fq").apply(tday)
    C["zq"] = pd.qcut(C.z.rank(method="first"), 4, labels=False)
    out["by_rawz_quart(0=most neg)"] = C.groupby("zq").apply(tday)
    C["r20q"] = pd.qcut(C.r20.rank(method="first"), 4, labels=False)
    out["by_r20_quart"] = C.groupby("r20q").apply(tday)
    # horizons
    hz = {}
    for h in (1, 3, 5, 10, 20):
        dd = C.copy(); dd["uh"] = -(dd[f"f{h}"] - dd.dr * h / 5)
        hz[h] = tday(dd, "uh")
    out["horizons_on_cases"] = pd.DataFrame(hz).T
    # unconditioned: all bars, grid pos%5==0, by regime and z quartile among falls
    G = R[(R.pos % 5 == 0) & R.f5.notna() & R.z.notna()].copy()
    G["u"] = -(G.f5 - G.dr)
    G["fall"] = G.z < 0
    out["grid_by_regime_fall"] = G.groupby(["regime", "fall"]).apply(tday)
    Gf = G[G.z < 0].copy()
    Gf["zb"] = pd.cut(Gf.z, [-99, -3, -2, -1, 0])
    out["grid_falls_by_zbin_regime"] = Gf.groupby(["regime", "zb"]).apply(tday)
    return out

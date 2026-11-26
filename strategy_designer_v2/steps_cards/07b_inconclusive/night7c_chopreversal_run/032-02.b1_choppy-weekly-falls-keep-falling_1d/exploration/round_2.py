def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 7, 7)
            allr += list(c[idx + 7] / c[idx] - 1)
        dr = np.mean(allr); us = np.std(allr, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lr = np.log(df["close"]).diff()
            ret7 = df["close"] / df["close"].shift(7) - 1
            er = (df["close"] - df["close"].shift(30)).abs() / df["close"].diff().abs().rolling(30).sum()
            er_std = (er - er.rolling(60, min_periods=20).mean()) / er.rolling(60, min_periods=20).std()
            vol30 = lr.rolling(30).std()
            vpct = vol30.rolling(100).apply(lambda x: (x[:-1] < x[-1]).mean() if len(x) > 1 else np.nan, raw=True).rolling(5).mean()
            n = len(df)
            for i in range(0, n - 7, 7):
                r = c[i + 7] / c[i] - 1
                rows.append(dict(coin=coin, win=w, day=str(df["timestamp"].iloc[i])[:10],
                                 sit=df["regime"].iloc[i] == "mean_reversion",
                                 ret7=ret7.iloc[i], er=er.iloc[i], erstd=er_std.iloc[i],
                                 vpct=vpct.iloc[i], fc=df["forecast"].iloc[i],
                                 z7=ret7.iloc[i] / (vol30.iloc[i] * np.sqrt(7)) if vol30.iloc[i] > 0 else np.nan,
                                 unu=-(r - dr), tot=-r, strg=-(r - dr) / us))
    d = pd.DataFrame(rows)
    def summ(g, col="unu"):
        g = g.dropna(subset=[col])
        x = g[col]
        if len(x) < 5: return pd.Series(dict(n=len(x)))
        dd = g.groupby("day")[col].apply(lambda v: (v - x.mean()).sum())
        G = len(dd)
        se = np.sqrt((dd ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series(dict(n=len(x), days=G, mean=x.mean(), t_day=x.mean() / se, strength=g["strg"].mean(), tot=g["tot"].mean()))
    out = {}
    s = d[d.sit].copy()
    out["sit_all"] = summ(s).to_frame().T
    out["sit_fc_neg"] = summ(s[s.fc < 0]).to_frame().T
    out["sit_fc_zero"] = summ(s[s.fc == 0]).to_frame().T
    s2 = s[s.fc < 0].copy()
    s2["fq"] = pd.qcut(s2.fc.abs().rank(method="first"), 3, labels=["weakfc", "midfc", "strongfc"])
    out["by_fc_size"] = s2.groupby("fq").apply(summ)
    s["erq"] = pd.qcut(s.er, 2, labels=["lowER", "highER"])
    out["by_rawER_half"] = s.groupby("erq").apply(summ)
    out["corr_erstd_er"] = float(s[["erstd", "er"]].dropna().corr().iloc[0, 1])
    # falls in agitated, by ER only (no vol), and agitated by vol only
    f = d[(d.ret7 < 0)].copy()
    f["erb"] = pd.cut(f.er, [0, 0.15, 0.3, 0.5, 1.01])
    out["falls_by_ER_bins"] = f.groupby("erb").apply(summ)
    f2 = f[f.er < 0.3].copy()
    f2["vb"] = pd.cut(f2.vpct, [-0.01, 0.25, 0.5, 0.75, 1.01])
    out["chopfalls_by_volpct"] = f2.groupby("vb").apply(summ)
    # rises in the same agitated chop
    r = d[(d.ret7 > 0) & (d.er < 0.3) & (d.vpct >= 0.5)].copy()
    out["chop_rises_short"] = summ(r).to_frame().T
    out["sit_excl_XMR"] = summ(s[s.coin != "XMRUSD"]).to_frame().T
    return out

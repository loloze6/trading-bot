def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    drows = []
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            c = df["close"].reset_index(drop=True)
            r10 = c.shift(-10) / c - 1
            allret += list(r10.iloc[::10].dropna())
        drift = np.mean(allret) if allret else 0.0
        sd10 = np.std(allret, ddof=1) if len(allret) > 2 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            vol90 = r1.rolling(90, min_periods=60).std()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            f10 = c.shift(-10) / c - 1
            rng = (df["high"] - df["low"]) / c
            clpos = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            inprof = (df["regime"] == "unknown")
            for i in range(0, len(df), 10):
                if pd.isna(f10.iloc[i]):
                    continue
                rows.append(dict(coin=coin, w=w, inprof=bool(inprof.iloc[i]),
                                 r30=r30.iloc[i], r60=r60.iloc[i], r5=r5.iloc[i],
                                 z30=r30.iloc[i] / (vol30.iloc[i] * np.sqrt(30)) if vol30.iloc[i] > 0 else np.nan,
                                 volrat=vol30.iloc[i] / vol90.iloc[i] if vol90.iloc[i] > 0 else np.nan,
                                 ex=f10.iloc[i] - drift, f10=f10.iloc[i], sd10=sd10,
                                 day=str(df["timestamp"].iloc[i])[:10]))
            n1 = r1.shift(-1)
            z1 = r1 / vol30.shift(1)
            ts = pd.to_datetime(df["timestamp"])
            drows.append(pd.DataFrame(dict(coin=coin, w=w, z1=z1, n1=n1, inprof=inprof,
                                           wd=ts.dt.weekday, clpos=clpos,
                                           rngz=rng / rng.rolling(30).mean().shift(1))))
    g = pd.DataFrame(rows)
    d = pd.concat(drows).dropna(subset=["n1"])
    out = {}
    def tab(sub, col, q=5):
        s = sub.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        return s.groupby("q").agg(n=("ex", "size"), xmean=(col, "mean"), ex=("ex", "mean"),
                                  t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out["grid r30 quintile, all"] = tab(g, "r30")
    out["grid r30 quintile, in profile"] = tab(g[g.inprof], "r30", 3)
    out["grid r30 quintile, out of profile"] = tab(g[~g.inprof], "r30")
    ch = g[(g.r60.abs() <= 0.10)]
    out["grid r30 quintile, choppy (r60 in-window)"] = tab(ch, "r30", 4)
    out["grid r60 quintile, all"] = tab(g, "r60")
    out["grid r5 quintile, all"] = tab(g, "r5")
    out["grid volratio quintile, all"] = tab(g, "volrat")
    out["corr r30 vs ex, spearman"] = pd.Series({
        "all": stats.spearmanr(g.r30, g.ex, nan_policy="omit")[0],
        "inprof": stats.spearmanr(g[g.inprof].r30, g[g.inprof].ex, nan_policy="omit")[0],
        "n_all": g.r30.notna().sum(), "n_in": g[g.inprof].r30.notna().sum()})
    d["zq"] = pd.qcut(d.z1, 7, labels=False)
    out["daily next-day ret by z1 septile"] = d.groupby("zq").agg(n=("n1", "size"), z=("z1", "mean"),
        n1=("n1", "mean"), t=("n1", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["daily next-day by weekday"] = d.groupby("wd").agg(n=("n1", "size"), n1=("n1", "mean"),
        t=("n1", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    d["cq"] = pd.qcut(d.clpos, 5, labels=False, duplicates="drop")
    out["daily next-day by close position quintile"] = d.groupby("cq").agg(n=("n1", "size"),
        n1=("n1", "mean"), t=("n1", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    d["rq"] = pd.qcut(d.rngz, 5, labels=False, duplicates="drop")
    out["daily next-day abs by range-ratio quintile"] = d.groupby("rq").agg(n=("n1", "size"),
        n1=("n1", "mean"), absn1=("n1", lambda x: x.abs().mean()))
    out["share in profile grid"] = float(g.inprof.mean())
    return out

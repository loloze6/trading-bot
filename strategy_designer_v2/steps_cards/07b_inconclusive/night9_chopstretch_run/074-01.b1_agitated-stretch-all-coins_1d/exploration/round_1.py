def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 5, 10, 20]
    rows = []
    # coin mean h-return over all visible windows (non-overlapping)
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            r = cl.pct_change()
            sma = cl.rolling(20).mean()
            sd = r.rolling(20).std()
            stretch = (cl / sma - 1) / sd
            ret60 = cl / cl.shift(60) - 1
            ret5p = cl / cl.shift(5) - 1
            ts = pd.to_datetime(df["timestamp"])
            agit = df["regime"] != "chop"
            fc = df["forecast"].fillna(0)
            n = len(df)
            for i in range(0, n - 10, 10):
                rec = dict(coin=c, win=w, year=ts.iloc[i].year, day=str(ts.iloc[i].date()),
                           fc=fc.iloc[i], st=stretch.iloc[i], agit=bool(agit.iloc[i]),
                           r60=ret60.iloc[i], r5=ret5p.iloc[i])
                for h in H:
                    if i + h < n:
                        rec[f"x{h}"] = cl.iloc[i + h] / cl.iloc[i] - 1 - drift[(c, h)]
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="x10"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series(dict(n=len(g)))
        pd_ = g.groupby("day")[col].sum()
        dm = g.groupby("day")[col].apply(lambda s: (s - g[col].mean()).sum())
        se = np.sqrt((dm ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=g[col].mean(), t=g[col].mean() / se if se > 0 else np.nan))
    out = {}
    cases = d[d.fc > 0]
    out["cases_by_horizon"] = pd.DataFrame({h: summ(cases, f"x{h}") for h in H}).T
    below = d[d.st < 0].copy()
    below["grp"] = np.where(below.agit, "agit", "calm")
    out["below_agit_vs_calm_x10"] = below.groupby("grp").apply(summ)
    out["below_agit_vs_calm_x5"] = below.groupby("grp").apply(lambda g: summ(g, "x5"))
    ab = below[below.agit].copy()
    ab["q"] = pd.qcut(ab.st, 4, labels=["deepest", "q2", "q3", "shallow"])
    out["agit_below_by_depth_x10"] = ab.groupby("q").apply(summ)
    cb = below[~below.agit].copy()
    cb["q"] = pd.qcut(cb.st, 4, labels=["deepest", "q2", "q3", "shallow"])
    out["calm_below_by_depth_x10"] = cb.groupby("q").apply(summ)
    out["cases_by_coin"] = cases.groupby("coin").apply(summ)
    out["cases_by_year"] = cases.groupby("year").apply(summ)
    cs = cases.dropna(subset=["r60"]).copy()
    cs["trend"] = np.where(cs.r60 > 0.1, "rising", np.where(cs.r60 < -0.1, "falling", "choppy"))
    out["cases_by_trend"] = cs.groupby("trend").apply(summ)
    out["cases_by_trend_x5"] = cs.groupby("trend").apply(lambda g: summ(g, "x5"))
    out["corr_stretch_x10_agitbelow"] = pd.Series(dict(spearman=stats.spearmanr(ab.st, ab.x10, nan_policy="omit")[0], n=len(ab)))
    return out

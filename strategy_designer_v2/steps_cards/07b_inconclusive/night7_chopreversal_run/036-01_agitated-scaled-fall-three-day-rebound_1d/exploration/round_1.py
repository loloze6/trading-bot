def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allret = {h: [] for h in (1, 2, 3, 5, 7)}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for h in allret:
                for i in range(0, n - h, h):
                    allret[h].append((coin, c[i + h] / c[i] - 1))
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = (r1 / sd30).values
            r60 = (pd.Series(c) / pd.Series(c).shift(60) - 1).values
            fc = df["forecast"].astype(float).values
            reg = df["regime"].astype(str).values
            for i in range(0, n - 3, 3):
                d = dict(coin=coin, win=w, fc=fc[i], agit=reg[i] != "chop", z=z[i], r60=r60[i],
                         year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                         day=pd.Timestamp(df["timestamp"].iloc[i]).normalize())
                for h in (1, 3):
                    d[f"r{h}"] = c[i + h] / c[i] - 1
                d["r23"] = c[i + 3] / c[i + 1] - 1
                d["r7"] = c[i + 7] / c[i] - 1 if i + 7 < n else np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    drift = {h: pd.DataFrame(v, columns=["coin", "r"]).groupby("coin")["r"].mean() for h, v in allret.items()}
    for h in (1, 3, 7):
        X[f"e{h}"] = X[f"r{h}"] - X["coin"].map(drift[h])
    X["e23"] = X["r23"] - X["coin"].map(drift[2])
    out = {}
    cases = X[X.fc > 0].copy()
    def summ(g):
        return pd.Series({"n": len(g), "e1": g.e1.mean(), "e23": g.e23.mean(), "e3": g.e3.mean(),
                          "t3": g.e3.mean() / (g.e3.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "e7": g.e7.mean()})
    cases["fq"] = pd.qcut(cases.fc, 4, labels=False, duplicates="drop")
    out["cases by forecast quartile"] = cases.groupby("fq").apply(summ)
    out["cases by coin"] = cases.groupby("coin").apply(summ)
    out["cases by window"] = cases.groupby("win").apply(summ)
    out["cases by year"] = cases.groupby("year").apply(summ)
    cases["trend"] = np.where(cases.r60 > 0.1, "rising", np.where(cases.r60 < -0.1, "falling", "choppy"))
    out["cases by trend"] = cases.groupby("trend").apply(summ)
    # raw scaled fall, agitated vs calm, from prices
    F = X[(X.z < 0)].copy()
    F["fall"] = -F.z
    F["zb"] = pd.cut(F.fall, [0, 0.5, 1, 1.5, 2, 3, 20])
    out["falls by size x agitation (e3)"] = F.groupby(["agit", "zb"]).e3.agg(["count", "mean"]).unstack(0)
    res = {}
    for a in (True, False):
        g = F[F.agit == a].dropna(subset=["fall", "e3"])
        s = stats.linregress(g.fall, g.e3)
        res["agit" if a else "calm"] = {"n": len(g), "slope": s.slope, "t": s.slope / s.stderr}
        for h in ("e1", "e23", "e7"):
            gg = g.dropna(subset=[h]); s2 = stats.linregress(gg.fall, gg[h])
            res["agit" if a else "calm"][f"t_{h}"] = s2.slope / s2.stderr
    out["slope of excess on raw scaled fall"] = pd.DataFrame(res).T
    g = cases.dropna(subset=["e3"])
    s = stats.linregress(g.fc, g.e3)
    out["case slope e3 on fc (naive)"] = f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(g)}"
    out["fc vs raw z corr in cases"] = float(cases[["fc", "z"]].corr().iloc[0, 1])
    out["share of cases with z>=0 (up day)"] = float((cases.z >= 0).mean())
    return out

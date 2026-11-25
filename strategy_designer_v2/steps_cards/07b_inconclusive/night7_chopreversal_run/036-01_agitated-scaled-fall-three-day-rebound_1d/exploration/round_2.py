def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allret = {h: [] for h in (1, 2, 3)}
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
                d["r1"] = c[i + 1] / c[i] - 1
                d["r3"] = c[i + 3] / c[i] - 1
                d["r23"] = c[i + 3] / c[i + 1] - 1
                rows.append(d)
    X = pd.DataFrame(rows)
    drift = {h: pd.DataFrame(v, columns=["coin", "r"]).groupby("coin")["r"].mean() for h, v in allret.items()}
    X["e1"] = X.r1 - X.coin.map(drift[1]); X["e3"] = X.r3 - X.coin.map(drift[3]); X["e23"] = X.r23 - X.coin.map(drift[2])
    X["trend"] = np.where(X.r60 > 0.1, "rising", np.where(X.r60 < -0.1, "falling", "choppy"))
    out = {}
    F = X[(X.z < 0)].dropna(subset=["z", "e3", "r60"]).copy()
    F["fall"] = -F.z
    def clus_t(g, ycol, xcol):
        g = g.dropna(subset=[ycol, xcol])
        if len(g) < 10: return (len(g), np.nan, np.nan)
        x = g[xcol].values; y = g[ycol].values
        Xm = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(Xm, y, rcond=None)[0]
        u = y - Xm @ b
        XtX = np.linalg.inv(Xm.T @ Xm)
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = Xm[idx].T @ u[idx]; meat += np.outer(s, s)
        G = g.day.nunique()
        V = XtX @ meat @ XtX * G / (G - 1) * (len(x) - 1) / (len(x) - 2)
        return (len(g), b[1], b[1] / np.sqrt(V[1, 1]))
    res = {}
    for a in (True, False):
        for tr in ("falling", "choppy", "rising"):
            g = F[(F.agit == a) & (F.trend == tr)]
            n, b, t = clus_t(g, "e3", "fall")
            _, _, t1 = clus_t(g, "e1", "fall"); _, _, t23 = clus_t(g, "e23", "fall")
            res[f"{'agit' if a else 'calm'}-{tr}"] = {"n": n, "slope_e3": b, "t_e3": t, "t_e1": t1, "t_e23": t23,
                                                     "mean_e3": g.e3.mean(), "mean_e23": g.e23.mean()}
    out["raw fall slope by agitation x trend (clustered)"] = pd.DataFrame(res).T
    # cases (fc>0) in falling trend: by coin, window, forecast half
    C = X[(X.fc > 0)].copy()
    Cf = C[C.trend == "falling"]
    out["falling cases by coin"] = Cf.groupby("coin").agg(n=("e3", "size"), e1=("e1", "mean"), e23=("e23", "mean"), e3=("e3", "mean"))
    out["falling cases by window"] = Cf.groupby("win").agg(n=("e3", "size"), e3=("e3", "mean"))
    out["falling cases by year"] = Cf.groupby("year").agg(n=("e3", "size"), e3=("e3", "mean"))
    Cf2 = Cf.copy(); Cf2["half"] = pd.qcut(Cf2.fc, 2, labels=False)
    out["falling cases by forecast half"] = Cf2.groupby("half").agg(n=("e3", "size"), e1=("e1", "mean"), e23=("e23", "mean"), e3=("e3", "mean"))
    n, b, t = clus_t(Cf, "e3", "fc")
    out["falling cases slope e3 on fc"] = f"n {n} slope {b:.5f} t {t:.2f} days {Cf.day.nunique()}"
    m = Cf.e3.groupby(Cf.day).sum()
    out["falling cases mean e3 t (day-summed)"] = f"mean {Cf.e3.mean():.4f} t {Cf.e3.mean()/(m.std()*np.sqrt(len(m))/len(Cf)):.2f} days {len(m)}"
    out["cases by trend, slope e3 on fc (clustered)"] = pd.DataFrame({tr: dict(zip(["n", "slope", "t"], clus_t(C[C.trend == tr], "e3", "fc"))) for tr in ("falling", "choppy", "rising")}).T
    return out

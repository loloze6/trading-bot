import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values.astype(float))
            v = pd.Series(df["volume"].values.astype(float)) * c
            n = len(df)
            r30 = c.pct_change(30).values
            r60 = c.pct_change(60).values
            vr1 = (v.rolling(30).mean() / v.shift(30).rolling(60, min_periods=30).mean()).values
            vr2 = (v.rolling(10).mean() / v.shift(10).rolling(60, min_periods=30).mean()).values
            ts = pd.to_datetime(df["timestamp"])
            h = 5
            for t in range(0, n - h, h):
                rows.append(dict(coin=coin, day=ts.iloc[t].normalize(), year=ts.iloc[t].year,
                                 ret=c[t+h]/c[t]-1, fc=df["forecast"].iloc[t],
                                 reg=df["regime"].iloc[t], r30=r30[t], r60=r60[t],
                                 vr1=vr1[t], vr2=vr2[t]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["ret"].transform("mean")
    g["ex"] = g["ret"] - g["drift"]
    g["fall"] = (-g["r30"]).clip(lower=0)

    def slope_t(df, x, y="ex"):
        d = df.dropna(subset=[x, y])
        if len(d) < 15: return (len(d), np.nan, np.nan)
        X = np.column_stack([np.ones(len(d)), d[x].values])
        Y = d[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]
        e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = len(sc)
        V = XtXi @ (sc.T @ sc) @ XtXi * G / max(G - 1, 1)
        return (len(d), b[1], b[1] / np.sqrt(V[1, 1]))

    out = {}
    g["prof"] = np.where(g.r60 < -0.10, np.where(g.reg == "unknown", "falling_calm", "falling_agit"), "not_falling")
    res = []
    for p in ["falling_calm", "falling_agit", "not_falling"]:
        a = g[(g.prof == p) & (g.r30 < 0)]
        n, b, t = slope_t(a, "fall")
        res.append(dict(prof=p, n=n, days=a.day.nunique(), mean_ex=a.ex.mean(), slope_fall=b, t=t))
    out["slope_ex_on_fall_by_profile"] = pd.DataFrame(res)

    fc = g[(g.reg == "unknown") & (g.r30 < 0)].copy()
    res = []
    for vcol in ["vr1", "vr2"]:
        d = fc.dropna(subset=[vcol]).copy()
        med = d[vcol].median()
        for lab, s in [("quiet", d[d[vcol] <= med]), ("heavy", d[d[vcol] > med])]:
            n, b, t = slope_t(s, "fall")
            res.append(dict(vol=vcol, grp=lab, n=n, days=s.day.nunique(), mean_ex=s.ex.mean(), slope=b, t=t))
        # graded quiet-weighted fall: fall / vol ratio
        d["qfall"] = d["fall"] / d[vcol]
        n, b, t = slope_t(d, "qfall")
        res.append(dict(vol=vcol, grp="fall_div_vol", n=n, days=d.day.nunique(), mean_ex=d.ex.mean(), slope=b, t=t))
    out["falling_calm_volume_split"] = pd.DataFrame(res)

    d = fc.dropna(subset=["vr1"]).copy()
    d["qfall"] = d["fall"] / d["vr1"]
    d["q"] = pd.qcut(d["qfall"], 4, labels=False, duplicates="drop")
    out["falling_calm_qfall_quartiles"] = d.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                             fall=("fall", "mean"), vr=("vr1", "mean"))
    out["falling_calm_qfall_by_year"] = pd.DataFrame(
        [dict(year=y, **dict(zip(["n", "slope", "t"], slope_t(s, "qfall")))) for y, s in d.groupby("year")])
    return out

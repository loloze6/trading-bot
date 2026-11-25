def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        drift[coin] = pd.concat(allr).mean()
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            cl = (c - l) / rng.replace(0, np.nan)
            r = c.pct_change()
            sd = r.rolling(20).std()
            wide = (rng / c) / sd
            tr60 = c.pct_change(60) * 100
            active = b["regime"] != "chop"
            fc = b["forecast"].astype(float)
            for H in [1, 2, 3, 5]:
                fwd = c.shift(-H) / c - 1
                for i in range(len(b)):
                    if H > 1 and i % H != 0:
                        continue
                    if np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, i=i, H=H, ts=b["timestamp"].iloc[i],
                                     active=bool(active.iloc[i]), case=bool(fc.iloc[i] < 0),
                                     cl=cl.iloc[i], wide=wide.iloc[i], tr60=tr60.iloc[i],
                                     fwd=fwd.iloc[i], ex=fwd.iloc[i] - drift[coin] * H))
    d = pd.DataFrame(rows)
    out = {}
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series(dict(n=len(x), mean_ex=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    a = d[d.active & (d.H == 1)]
    out["H1 active by case(fc<0)"] = a.groupby("case").apply(summ)
    a = a.copy()
    a["cl_bin"] = pd.cut(a["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["H1 active bars by close loc bin (ex = unsigned next-day excess)"] = a.groupby("cl_bin").apply(summ)
    out["H1 cases by coin"] = a[a.case].groupby("coin").apply(summ)
    out["H1 cases by window"] = a[a.case].groupby("w").apply(summ)
    a["year"] = pd.to_datetime(a["ts"]).dt.year
    out["H1 cases by year"] = a[a.case].groupby("year").apply(summ)
    a["wide_bin"] = pd.qcut(a["wide"], 3, duplicates="drop")
    out["H1 cases by wide tercile"] = a[a.case].groupby("wide_bin").apply(summ)
    dd = d[d.active]
    out["active by horizon & case (grid)"] = dd.groupby(["H", "case"]).apply(summ)
    dd = dd.copy()
    dd["hi"] = dd["cl"] >= 0.67
    dd["lo"] = dd["cl"] <= 0.33
    out["active by horizon, top third cl"] = dd[dd.hi].groupby("H").apply(summ)
    out["active by horizon, bottom third cl"] = dd[dd.lo].groupby("H").apply(summ)
    # all falling (tr60<-10) days, not only wide/agitated, close loc bins at H1
    f = d[(d.H == 1) & (d.tr60 < -10)].copy()
    f["cl_bin"] = pd.cut(f["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["H1 all falling days by cl bin"] = f.groupby("cl_bin").apply(summ)
    return out

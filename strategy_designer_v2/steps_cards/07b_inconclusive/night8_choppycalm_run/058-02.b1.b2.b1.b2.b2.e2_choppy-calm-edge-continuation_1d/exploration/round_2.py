import numpy as np, pandas as pd

def clslope(x, y, g):
    x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
    X = np.column_stack([np.ones_like(x), x])
    XtX = np.linalg.inv(X.T @ X)
    b = XtX @ X.T @ y
    e = y - X @ b
    meat = np.zeros((2, 2)); G = 0
    for k in pd.unique(g):
        m = g == k
        s = X[m].T @ e[m]; meat += np.outer(s, s); G += 1
    n = len(y)
    V = XtX @ meat @ XtX * (G/(G-1)) * ((n-1)/(n-2))
    return b[1], b[1]/np.sqrt(V[1, 1]), n, G

def explore(data):
    rows = []; allg = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            raw = b.get("debug_info.components.range_pos.last_history_value")
            n = len(b)
            for h in (5, 10):
                for i in range(0, n-h, h):
                    r = c[i+h]/c[i]-1
                    allg.append((coin, h, r))
                    if b["regime"].iloc[i] == "unknown" and b["forecast"].iloc[i] != 0:
                        ts = pd.Timestamp(b["timestamp"].iloc[i])
                        rows.append(dict(coin=coin, w=w, h=h, ret=r, fc=b["forecast"].iloc[i],
                                         raw=raw.iloc[i] if raw is not None else np.nan,
                                         day=ts.normalize(), year=ts.year))
    g = pd.DataFrame(allg, columns=["coin", "h", "ret"]).groupby(["coin", "h"])["ret"].mean()
    d = pd.DataFrame(rows)
    d["ex"] = d.ret - [g.loc[(a, h)] for a, h in zip(d.coin, d.h)]
    out = {}
    res = []
    for h in (5, 10):
        for name, sub in [("all", d), ("no2021", d[d.year != 2021]), ("no_w18", d[d.w != "w18"]),
                          ("long_only", d[d.fc > 0]), ("short_only", d[d.fc < 0]),
                          ("edges_absraw>=10", d[d.raw.abs() >= 10]), ("middle_absraw<10", d[d.raw.abs() < 10])]:
            s = sub[sub.h == h].dropna(subset=["ex", "fc"])
            if len(s) > 10:
                sl, t, n, G = clslope(s.fc, s.ex, s.day)
                res.append(dict(h=h, sub=name, slope=sl, t_cl=t, n=n, days=G))
    out["clustered_slopes"] = pd.DataFrame(res)
    d10 = d[d.h == 10].copy()
    d10["sg"] = np.sign(d10.fc); d10["direx"] = d10.ex*d10.sg
    out["h10_by_year"] = d10.groupby("year")["direx"].agg(n="size", mean_pct=lambda x: 100*x.mean(),
                                                          t=lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
    return out

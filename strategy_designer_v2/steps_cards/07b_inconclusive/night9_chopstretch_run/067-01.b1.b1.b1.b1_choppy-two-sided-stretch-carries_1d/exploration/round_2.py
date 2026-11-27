import numpy as np, pandas as pd
from scipy import stats

def cl_t(x, y, g):
    X = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    meat = np.zeros((2, 2))
    for k in np.unique(g):
        m = g == k
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(np.unique(g)); n = len(x)
    V = XtXi @ meat @ XtXi * G / (G - 1) * (n - 1) / (n - 2)
    return b[1], b[1] / np.sqrt(V[1, 1])

def dmean_t(v, g):
    s = pd.Series(v).groupby(g).sum()
    n = len(v)
    m = v.mean()
    dev = (pd.Series(v - m).groupby(g).sum())
    se = np.sqrt((dev ** 2).sum()) / n
    return m, m / se, len(s)

def explore(data):
    bars = data["bars"]
    H = [2, 5, 10, 20]
    drift, usual = {}, {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs, ddof=1)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            ret60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").astype(str)
            f = df["forecast"].fillna(0)
            raw = df.get("debug_info.components.stretch.last_history_value")
            for h in H:
                for i in range(0, len(c) - h, h):
                    if f.iloc[i] == 0: continue
                    fr = c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)]
                    rows.append(dict(coin=coin, w=w, h=h, f=f.iloc[i],
                                     raw=raw.iloc[i] if raw is not None else np.nan,
                                     un=fr, unz=fr / usual[(coin, h)], yr=day.iloc[i][:4],
                                     day=day.iloc[i], r60=ret60.iloc[i], r20=ret20.iloc[i]))
    d = pd.DataFrame(rows)
    d["side"] = np.where(d.f > 0, "long", "short")
    def summ(g):
        if len(g) < 15: return pd.Series(dict(n=len(g)))
        sl, t = cl_t(g.f.values, g.un.values, g.day.values)
        dm, dt, nd = dmean_t((np.sign(g.f) * g.un).values, g.day.values)
        return pd.Series(dict(n=len(g), days=nd, slope=sl, slope_t=t, dir_mean=dm, dir_t=dt,
                              strength=(np.sign(g.f) * g.unz).mean()))
    out = {}
    out["by_h"] = d.groupby("h").apply(summ)
    out["by_h_side"] = d.groupby(["h", "side"]).apply(summ)
    d10 = d[d.h == 10].copy()
    d10["q"] = pd.qcut(d10.f, 6, labels=False)
    out["q_f_h10"] = d10.groupby("q").agg(n=("un", "size"), f=("f", "mean"), un=("un", "mean"), unz=("unz", "mean"))
    d10["absq"] = pd.qcut(d10.f.abs(), 3, labels=False)
    out["absq_side_h10"] = d10.groupby(["absq", "side"]).apply(summ)
    out["coin_h10"] = d10.groupby("coin").apply(summ)
    out["yr_h10"] = d10.groupby("yr").apply(summ)
    d10["r60s"] = np.where(d10.r60.isna(), "na", np.where(d10.r60 < 0, "neg", "pos"))
    out["r60s_side_h10"] = d10.groupby(["r60s", "side"]).apply(summ)
    d5 = d[d.h == 5].copy()
    d5["r60s"] = np.where(d5.r60.isna(), "na", np.where(d5.r60 < 0, "neg", "pos"))
    out["r60s_side_h5"] = d5.groupby(["r60s", "side"]).apply(summ)
    out["coin_side_h5"] = d5.groupby(["coin", "side"]).apply(summ)
    return out

import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 20
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = (np.mean(rets), np.std(rets, ddof=1))
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            seen = set()
            for t in range(61, n):
                prior = c[t - 60:t].max()
                if c[t] > prior:
                    cell = t // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    # break size in units of daily vol (20-day std of daily returns)
                    dr = np.diff(c[max(0, t - 60):t + 1]) / c[max(0, t - 60):t]
                    vol = np.std(dr, ddof=1)
                    brk = c[t] / prior - 1
                    rec = dict(coin=coin, w=w, day=str(df["timestamp"].iloc[t])[:10],
                               year=str(df["timestamp"].iloc[t])[:4],
                               R=c[t - 1] / c[t - 61] - 1, brk=brk, brkv=brk / vol if vol > 0 else np.nan)
                    for h in (10, 20, 40):
                        rec[f"f{h}"] = (c[t + h] / c[t] - 1 - drift[coin][0] * h / 20) if t + h < n else np.nan
                        rec[f"z{h}"] = rec[f"f{h}"] / (drift[coin][1] * np.sqrt(h / 20)) if t + h < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    out = {"n": len(d)}

    def clustered(x, y, day):
        m = pd.notna(x) & pd.notna(y)
        x, y, day = x[m].values, y[m].values, day[m].values
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for dday in np.unique(day):
            k = day == dday
            s = X[k].T @ e[k]
            meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return b[1], b[1] / np.sqrt(V[1, 1]), int(m.sum()), len(np.unique(day))

    res = {}
    for var in ("brk", "brkv", "R"):
        for h in (10, 20, 40):
            s = clustered(d[var], d[f"f{h}"], d["day"])
            res[f"{var}_f{h}"] = dict(slope=s[0], t_cl=s[1], n=s[2], days=s[3])
    out["slopes_clustered"] = pd.DataFrame(res).T
    dd = d.dropna(subset=["f20"]).copy()
    dd["bq"] = pd.qcut(dd["brkv"], 3, labels=["small", "mid", "large"])
    agg = lambda g: pd.Series(dict(n=len(g), mean20=g["f20"].mean(), z20=g["z20"].mean(),
                                    t=g["f20"].mean() / (g["f20"].std(ddof=1) / np.sqrt(len(g))) if len(g) > 1 else np.nan,
                                    mean_brkv=g["brkv"].mean()))
    out["by_brkv_tercile"] = dd.groupby("bq").apply(agg)
    out["by_year_brkv"] = dd.groupby(["year", "bq"]).apply(agg)[["n", "mean20"]]
    pc = {}
    for coin, g in dd.groupby("coin"):
        if len(g) >= 4:
            r = stats.linregress(g["brkv"], g["f20"])
            pc[coin] = dict(n=len(g), slope=r.slope, r=r.rvalue, mean20=g["f20"].mean())
    out["per_coin_brkv"] = pd.DataFrame(pc).T
    out["strength_all"] = dict(mean_z20=dd["z20"].mean(), n=len(dd))
    return out

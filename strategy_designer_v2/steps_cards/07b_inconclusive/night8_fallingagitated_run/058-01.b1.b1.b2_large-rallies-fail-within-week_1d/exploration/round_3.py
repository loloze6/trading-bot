import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [2, 3, 4, 5, 6]
    drift = {}
    rows = []
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            sd = c.pct_change().rolling(30, min_periods=30).std()
            sc = (c / c.shift(3) - 1) / sd
            inprof = (b["regime"] == "unknown").values
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    if not inprof[i] or not np.isfinite(sc.iloc[i]) or not np.isfinite(fwd.iloc[i]) or sc.iloc[i] <= 0:
                        continue
                    mu, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, w=w, h=h, sc=sc.iloc[i], ex=fwd.iloc[i] - mu,
                                     st=(fwd.iloc[i] - mu) / s,
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4]))
    df = pd.DataFrame(rows)

    def slope_cl(g, xcol="sc", ycol="ex"):
        g = g.reset_index(drop=True)
        x = g[xcol].values; y = g[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for dday, idx in g.groupby("day").groups.items():
            u = (X[idx] * e[idx][:, None]).sum(0)
            meat += np.outer(u, u)
        V = XtXi @ meat @ XtXi
        return beta[1], beta[1] / np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan

    res = []
    for h in H:
        g = df[df.h == h]
        b1, t1 = slope_cl(g)
        b2, t2 = slope_cl(g, ycol="st")
        res.append(dict(h=h, n=len(g), days=g.day.nunique(), slope_ex=b1, t_ex=t1, slope_strength=b2, t_strength=t2,
                        spearman=stats.spearmanr(g.sc, g.ex)[0]))
    out = {"rise_slope_by_h": pd.DataFrame(res)}
    g3 = df[df.h == 3]
    yr = []
    for y, g in g3.groupby("year"):
        b, t = slope_cl(g) if g.day.nunique() > 3 else (np.nan, np.nan)
        yr.append(dict(year=y, n=len(g), days=g.day.nunique(), slope=b, t=t, short_excess=-g.ex.mean()))
    out["rise3_slope_by_year"] = pd.DataFrame(yr)
    g3 = g3.copy()
    g3["half"] = (g3.sc > g3.sc.median()).map({True: "top", False: "bottom"})
    out["rise3_halves"] = g3.groupby("half").apply(lambda g: pd.Series(dict(n=len(g), days=g.day.nunique(),
                          short_excess=-g.ex.mean(), share_neg=(g.ex < 0).mean())))
    cn = []
    for cname, g in g3.groupby("coin"):
        cn.append(dict(coin=cname, n=len(g), spearman=stats.spearmanr(g.sc, g.ex)[0] if len(g) > 5 else np.nan))
    out["rise3_by_coin"] = pd.DataFrame(cn)
    return out

import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [3, 5, 7, 8, 10]
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
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=30).std()
            sc = (c / c.shift(3) - 1) / sd
            std60 = (sc - sc.rolling(60, min_periods=20).mean()) / sc.rolling(60, min_periods=20).std()
            inprof = (b["regime"] == "unknown").values
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    if not inprof[i] or not np.isfinite(sc.iloc[i]) or not np.isfinite(fwd.iloc[i]):
                        continue
                    mu, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, w=w, h=h, sc=sc.iloc[i], z=std60.iloc[i],
                                     ex=fwd.iloc[i] - mu, fc=b["forecast"].iloc[i],
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4]))
    df = pd.DataFrame(rows)

    def day_t(g, col="ex"):
        d = g.groupby("day")[col].apply(lambda x: (x - g[col].mean()).sum())
        se = np.sqrt((d ** 2).sum()) / len(g)
        return g[col].mean() / se if se > 0 else np.nan

    def slope_cl(g, xcol):
        g = g.dropna(subset=[xcol])
        x = g[xcol].values; y = g["ex"].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for dday, idx in g.reset_index(drop=True).groupby("day").groups.items():
            u = (X[idx] * e[idx][:, None]).sum(0)
            meat += np.outer(u, u)
        V = XtXi @ meat @ XtXi
        return beta[1], beta[1] / np.sqrt(V[1, 1])

    res = []
    for h in H:
        for side, g in [("rise", df[(df.h == h) & (df.sc > 0)]), ("fall", df[(df.h == h) & (df.sc <= 0)])]:
            g = g.reset_index(drop=True)
            b_sc, t_sc = slope_cl(g, "sc")
            b_z, t_z = slope_cl(g, "z")
            res.append(dict(h=h, side=side, n=len(g), days=g.day.nunique(),
                            short_excess=-g.ex.mean(), t_short_dayclust=-day_t(g),
                            slope_ex_on_sc=b_sc, t_slope_sc=t_sc, slope_ex_on_z=b_z, t_slope_z=t_z))
    out = {"by_h_side_clustered": pd.DataFrame(res)}
    allg = df[df.h == 5].reset_index(drop=True)
    b, t = slope_cl(allg, "sc")
    out["h5_both_sides_slope_ex_on_sc"] = pd.Series(dict(n=len(allg), slope=b, t=t))
    r8 = df[(df.h == 8) & (df.sc > 0)]
    out["rise8_by_year"] = r8.groupby("year").apply(lambda g: pd.Series(dict(
        n=len(g), days=g.day.nunique(), short_excess=-g.ex.mean())))
    r5 = df[(df.h == 5) & (df.sc > 0)].copy()
    r5["zq"] = pd.qcut(r5["z"], 3, labels=False, duplicates="drop")
    out["rise5_by_z_tercile"] = r5.groupby("zq").apply(lambda g: pd.Series(dict(
        n=len(g), days=g.day.nunique(), short_excess=-g.ex.mean(), t_dc=-day_t(g.reset_index(drop=True)))))
    return out

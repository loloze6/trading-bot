import numpy as np, pandas as pd
from scipy import stats

def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y); x = x[m]; y = y[m]
    n = len(x)
    if n < 8 or np.std(x) == 0:
        return (np.nan, np.nan, n)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    s2 = r @ r / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    return (b[1], b[1] / np.sqrt(cov[1, 1]), n)

def explore(data):
    bars = data["bars"]
    out = {}
    def grid(h):
        rows = []
        for c, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                fc = df["forecast"].values
                lhv = df["debug_info.components.hpm.last_history_value"].values
                ts = pd.to_datetime(df["timestamp"])
                runmax = pd.Series(cl).cummax().values
                for p in range(0, len(df), h):
                    if p + h >= len(df):
                        break
                    if p < 30:
                        continue
                    fwd = cl[p + h] / cl[p] - 1
                    past = cl[p] / cl[p - 30] - 1
                    prox = cl[p] / runmax[p]
                    rows.append(dict(coin=c, year=ts.iloc[p].year, fwd=fwd, fc=fc[p],
                                     past=past, lhv=lhv[p], W=lhv[p] / past if past != 0 else np.nan,
                                     prox=prox))
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        return g
    g = grid(30)
    out["corr_checks"] = pd.Series({
        "spearman_W_prox": stats.spearmanr(g.W, g.prox, nan_policy="omit")[0],
        "spearman_lhv_fc": stats.spearmanr(g.lhv, g.fc, nan_policy="omit")[0],
        "spearman_lhv_past": stats.spearmanr(g.lhv, g.past, nan_policy="omit")[0],
        "share_W_neg": (g.W < 0).mean(),
        "n": len(g)})
    g["pq"] = pd.qcut(g.prox.rank(method="first"), 3, labels=["far", "mid", "near"])
    r = []
    for k, s in g.groupby("pq"):
        r.append([f"past_{k}", *ols(s.past, s.ex), s.prox.mean()])
    out["past_slope_by_inwindow_prox"] = pd.DataFrame(r, columns=["grp", "slope", "t", "n", "meanprox"])
    g["Wq"] = pd.qcut(g.W.rank(method="first"), 3, labels=["far", "mid", "near"])
    r = []
    nr = g[g.Wq == "near"]
    for k, s in nr.groupby("coin"):
        r.append([k, *ols(s.past, s.ex)])
    nr2 = nr.copy(); nr2["half"] = np.where(nr2.year <= 2021, "2018-21", "2022-25")
    for k, s in nr2.groupby("half"):
        r.append([k, *ols(s.past, s.ex)])
    out["near_W_past_slope_by_coin_half"] = pd.DataFrame(r, columns=["grp", "slope", "t", "n"])
    r = []
    for h in [10, 20, 30, 60]:
        gh = grid(h)
        gh["Wq"] = pd.qcut(gh.W.rank(method="first"), 3, labels=["far", "mid", "near"])
        for k, s in gh.groupby("Wq"):
            r.append([h, k, *ols(s.past, s.ex)])
    out["past_slope_W_by_horizon"] = pd.DataFrame(r, columns=["h", "Wq", "slope", "t", "n"])
    return out

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
                lhv = df["debug_info.components.hpm.last_history_value"].values if "debug_info.components.hpm.last_history_value" in df else np.full(len(df), np.nan)
                ts = pd.to_datetime(df["timestamp"])
                for p in range(0, len(df), h):
                    if p + h >= len(df):
                        break
                    fwd = cl[p + h] / cl[p] - 1
                    past = cl[p] / cl[p - 30] - 1 if p >= 30 else np.nan
                    W = lhv[p] / past if (p >= 30 and past != 0) else np.nan
                    rows.append(dict(coin=c, win=w, year=ts.iloc[p].year, pos=p,
                                     fwd=fwd, fc=fc[p], past=past, W=W))
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        return g

    g = grid(30)
    out["main_check"] = pd.Series(ols(g.fc / 10, g.ex), index=["slope", "t", "n"])

    by = []
    for k, s in g.groupby("coin"):
        by.append([k, *ols(s.fc / 10, s.ex)])
    for k, s in g.groupby("year"):
        by.append([str(k), *ols(s.fc / 10, s.ex)])
    s = g[g.fc > 0]
    by.append(["fc>0", *ols(s.fc / 10, s.ex)])
    s = g[g.fc < 0]
    by.append(["fc<0", *ols(s.fc / 10, s.ex)])
    out["main_by_group"] = pd.DataFrame(by, columns=["grp", "slope", "t", "n"])

    gg = g.dropna(subset=["past", "W"]).copy()
    gg["Wq"] = pd.qcut(gg.W, 3, labels=["far", "mid", "near"])
    r = [["all_past", *ols(gg.past, gg.ex)]]
    for k, s in gg.groupby("Wq"):
        r.append([f"past_{k}", *ols(s.past, s.ex)])
    for k, s in gg.groupby("Wq"):
        r.append([f"fc_{k}", *ols(s.fc / 10, s.ex)])
    out["slopes_by_W_tercile"] = pd.DataFrame(r, columns=["grp", "slope", "t", "n"])
    out["W_tercile_stats"] = gg.groupby("Wq").agg(meanW=("W", "mean"), mean_ex=("ex", "mean"),
                                                 mean_fwd=("fwd", "mean"), n=("ex", "size"))

    gg["side"] = np.where(gg.past > 0, "up", "down")
    r = []
    for (k, sd), s in gg.groupby(["Wq", "side"]):
        r.append([f"{k}_{sd}", s.ex.mean(), s.ex.std() / np.sqrt(len(s)), len(s)])
    out["ex_by_W_and_side"] = pd.DataFrame(r, columns=["grp", "mean_ex", "se", "n"])

    hz = []
    for h in [5, 10, 20, 30, 60]:
        gh = grid(h)
        hz.append([h, *ols(gh.fc / 10, gh.ex)])
    out["horizons"] = pd.DataFrame(hz, columns=["h", "slope", "t", "n"])
    return out

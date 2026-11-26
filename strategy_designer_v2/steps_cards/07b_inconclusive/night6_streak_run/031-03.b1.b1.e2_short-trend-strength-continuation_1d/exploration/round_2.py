import numpy as np, pandas as pd
from scipy import stats

def clustered_t(x, y, g):
    x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    meat = np.zeros((2, 2))
    G = 0
    for k in pd.unique(g):
        m = g == k
        s = X[m].T @ e[m]
        meat += np.outer(s, s); G += 1
    n = len(y)
    c = G / (G - 1) * (n - 1) / (n - 2)
    V = c * XtX_inv @ meat @ XtX_inv
    return b[1], b[1] / np.sqrt(V[1, 1]), n, G

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["debug_info.components.scaled_rise.post_pipeline_value"].astype(float).values
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(60, min_periods=40).std().values
            r10 = pd.Series(c).pct_change(10).values
            z = r10 / (sd * np.sqrt(10))
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            day = ts.dt.floor("D").astype("int64").values
            n = len(c)
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    rows.append((coin, w, h, i, yr[i], day[i], f[i], z[i], c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "i", "yr", "day", "f", "z", "ret"])
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    out = {}

    res = []
    for h in [5, 10]:
        for name, sel, xcol in [
            ("f>0, on f", lambda s: s.f > 0, "f"),
            ("z>0, on z", lambda s: s.z > 0, "z"),
            ("all, on z", lambda s: s.z.notna(), "z"),
            ("z>1, on z", lambda s: s.z > 1, "z"),
            ("z>0, on z^2", lambda s: s.z > 0, "z2"),
        ]:
            s = d[d.h == h].dropna(subset=["z", "ex"]).copy()
            s["z2"] = s.z ** 2
            s = s[sel(s)].dropna(subset=[xcol])
            b, t, n, G = clustered_t(s[xcol], s.ex, s.day)
            res.append((h, name, n, G, b, t, s.ex.mean()))
    out["clustered_slopes"] = pd.DataFrame(res, columns=["h", "set", "n", "days", "slope", "t_cl", "mean_ex"])

    # top bucket by raw z on h=10 and h=5, z>0, graded within
    for h in [5, 10]:
        s = d[(d.h == h) & (d.z > 0)].dropna(subset=["z", "ex"]).copy()
        s["zq"] = pd.qcut(s.z, 6, labels=False)
        agg = []
        for q, g in s.groupby("zq"):
            b, t, n, G = (np.nan, np.nan, len(g), g.day.nunique())
            dm = g.groupby("day").ex.sum()
            tday = g.ex.mean() / (dm.std() * np.sqrt(len(dm)) / len(g)) if len(dm) > 2 else np.nan
            agg.append((q, g.z.mean(), len(g), g.ex.mean(), tday, (g.ret).mean()))
        out[f"h{h}_by_z_sextile_zpos"] = pd.DataFrame(agg, columns=["q", "z", "n", "ex", "t_day", "total"])

    # strongest rises by year and by coin (h=10, z top sextile among z>0)
    s = d[(d.h == 10) & (d.z > 0)].dropna(subset=["z", "ex"]).copy()
    thr = s.z.quantile(5 / 6)
    top = s[s.z >= thr]
    out["h10_top_by_year"] = top.groupby("yr").ex.agg(["size", "mean"])
    out["h10_top_by_coin_share_pos"] = pd.Series({
        "coins": top.coin.nunique(),
        "coins_mean_ex_pos": (top.groupby("coin").ex.mean() > 0).mean(),
        "years_mean_ex_pos": (top.groupby("yr").ex.mean() > 0).mean(),
        "z_threshold": thr})
    return out

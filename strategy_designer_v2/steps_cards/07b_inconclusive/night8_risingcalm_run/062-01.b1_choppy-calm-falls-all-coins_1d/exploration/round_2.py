import pandas as pd, numpy as np
from scipy import stats

def cl_t(x, y, g):
    x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
    X = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    meat = np.zeros((2, 2))
    ug = pd.unique(g)
    for k in ug:
        m = g == k
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(ug); n = len(x)
    V = XtXi @ meat @ XtXi * (G / (G - 1)) * ((n - 1) / (n - 2))
    return b[1], b[1] / np.sqrt(V[1, 1]), G

def explore(data):
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        for h in (3, 5, 10):
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
    out = {}
    allrows = []
    for off in range(5):
        for coin, ws in bars.items():
            for w, df in ws.items():
                c = df["close"].values; n = len(c)
                ret = pd.Series(c).pct_change()
                sd30 = ret.rolling(30).std().values
                f = df["forecast"].values; reg = df["regime"].values
                ts = pd.to_datetime(df["timestamp"])
                for i in range(off, n - 5, 5):
                    if reg[i] != "unknown" or i < 30 or np.isnan(sd30[i]):
                        continue
                    r = {"off": off, "coin": coin, "w": w, "day": str(ts.iloc[i].date()), "f": f[i],
                         "z": (c[i] / c[i - 5] - 1) / (sd30[i] * np.sqrt(5)),
                         "z10": (c[i] / c[i - 10] - 1) / (sd30[i] * np.sqrt(10)) if i >= 10 else np.nan}
                    for h in (3, 5, 10):
                        if i + h < n:
                            r["ex%d" % h] = c[i + h] / c[i] - 1 - drift[(coin, h)][0]
                    allrows.append(r)
    d = pd.DataFrame(allrows)
    d0 = d[d.off == 0]
    res = {}
    for name, sub, xc in [("f<0 forecast", d0[d0.f < 0], "f"), ("z<0 raw scaled", d0[d0.z < 0], "z"),
                          ("all z", d0, "z"), ("z10<0 raw", d0[d0.z10 < 0], "z10")]:
        for h in (3, 5, 10):
            s = sub.dropna(subset=[xc, "ex%d" % h])
            b, t, G = cl_t(s[xc], s["ex%d" % h], s["day"])
            res[(name, h)] = {"n": len(s), "days": G, "slope": b, "t_cl": t,
                              "short_unusual": -s["ex%d" % h].mean()}
    out["slopes"] = pd.DataFrame(res).T
    s = d0[d0.z < 0].dropna(subset=["ex5"]).copy()
    s["zb"] = pd.cut(s.z, [-10, -1.5, -1, -0.5, 0])
    out["z_bins_ex5"] = s.groupby("zb").apply(lambda g: pd.Series({"n": len(g), "z": g.z.mean(), "ex5": g.ex5.mean(), "ex10": g.ex10.mean(),
                                                                    "t": g.ex5.mean() / (g.ex5.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan}))
    ofs = {}
    for off in range(5):
        x = d[(d.off == off) & (d.f < 0)].dropna(subset=["ex5"])
        b, t, G = cl_t(x.f, x.ex5, x.day)
        ofs[off] = {"n": len(x), "slope_t_cl": t, "short_unusual": -x.ex5.mean(),
                    "t_mean": -x.ex5.mean() / (x.ex5.std() / np.sqrt(len(x)))}
    out["grid_offsets_f<0"] = pd.DataFrame(ofs).T
    out["corr_f_z_on_neg"] = float(d0[d0.f < 0][["f", "z"]].corr().iloc[0, 1])
    return out

import numpy as np, pandas as pd
from scipy import stats

def cl_slope(x, y, g):
    x = np.asarray(x, float); y = np.asarray(y, float); g = np.asarray(g)
    X = np.column_stack([np.ones(len(x)), x])
    XtX = np.linalg.inv(X.T @ X)
    b = XtX @ X.T @ y
    e = y - X @ b
    meat = np.zeros((2, 2))
    G = pd.Series(range(len(g))).groupby(g).indices
    for k, idx in G.items():
        s = X[idx].T @ e[idx]
        meat += np.outer(s, s)
    nG = len(G); n = len(x)
    V = XtX @ meat @ XtX * nG / (nG - 1) * (n - 1) / (n - 2)
    return b[1], b[1] / np.sqrt(V[1, 1]), n, nG

def cl_mean(v, g):
    v = np.asarray(v, float)
    m = v.mean()
    s = pd.Series(v - m).groupby(np.asarray(g)).sum()
    se = np.sqrt((s ** 2).sum()) / len(v)
    return m, m / se, len(v), len(s)

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(60, min_periods=20).std()
            s = np.sign(r).fillna(0).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0: st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]: st[i] = st[i-1] + s[i]
                else: st[i] = s[i]
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": r / sd,
                "sd": sd, "streak": st, "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "wd": ts.dt.weekday, "yr": ts.dt.year, "day": ts.dt.floor("D"),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1}))
    d = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 5):
        col = "f%d" % h
        mu = d[d.pos % h == 0].groupby("coin")[col].mean()
        d["ex%d" % h] = d[col] - d.coin.map(mu)
    out = {}
    # weekday, day-clustered, by halves
    g1 = d.dropna(subset=["ex1"])
    res = []
    for wd in range(7):
        x = g1[g1.wd == wd]
        m, t, n, nd = cl_mean(x.ex1, x.day)
        e = x[x.yr <= 2021]; l = x[x.yr >= 2022]
        res.append([wd, m, t, nd, cl_mean(e.ex1, e.day)[1], cl_mean(l.ex1, l.day)[1]])
    out["weekday ex1 clustered (t all, t 2018-21, t 2022-25)"] = pd.DataFrame(res, columns=["wd", "mean", "t", "days", "t_early", "t_late"]).set_index("wd")
    # rises -> 5-day continuation
    g5 = d[d.pos % 5 == 0].dropna(subset=["z", "ex5", "z3"])
    res = {}
    up = g5[g5.z > 0]
    res["rise z -> ex5"] = cl_slope(up.z, up.ex5, up.day)
    dn = g5[g5.z < 0]
    res["fall -z -> ex5"] = cl_slope(-dn.z, dn.ex5, dn.day)
    res["all z -> ex5"] = cl_slope(g5.z, g5.ex5, g5.day)
    res["all z3 -> ex5"] = cl_slope(g5.z3, g5.ex5, g5.day)
    for yrs, lab in [((2018, 2021), "early"), ((2022, 2025), "late")]:
        x = up[(up.yr >= yrs[0]) & (up.yr <= yrs[1])]
        res["rise z -> ex5 " + lab] = cl_slope(x.z, x.ex5, x.day)
    out["5-day slopes (slope, t, n, days)"] = pd.DataFrame(res, index=["slope", "t", "n", "days"]).T
    out["rise z -> ex5 by coin t"] = up.groupby("coin").apply(lambda x: cl_slope(x.z, x.ex5, x.day)[1])
    # up streak length -> ex2
    g2 = d[d.pos % 2 == 0].dropna(subset=["z", "ex2"])
    u = g2[g2.streak > 0]
    res = {"up streak len -> ex2": cl_slope(u.streak.clip(upper=7), u.ex2, u.day)}
    dd = g2[g2.streak < 0]
    res["down streak len -> ex2"] = cl_slope(-dd.streak.clip(lower=-7), dd.ex2, dd.day)
    # fall rebound interacted with vol tercile
    g2 = g2.assign(vq=g2.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 3, labels=False)))
    f = g2[g2.z < 0]
    for q in range(3):
        x = f[f.vq == q]
        res["fall -z -> ex2 volq%d" % q] = cl_slope(-x.z, x.ex2, x.day)
    # graded interaction: fall size in raw return (not vol-scaled)
    res["fall -r(raw) -> ex2"] = cl_slope(-f.z * f.sd, f.ex2, f.day)
    out["2-day slopes (slope, t, n, days)"] = pd.DataFrame(res, index=["slope", "t", "n", "days"]).T
    return out

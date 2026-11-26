import pandas as pd, numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["ret6"] = c / c.shift(6) - 1
            d["r1"] = c / c.shift(1) - 1
            d["vr"] = v / v.shift(1).rolling(20).mean() - 1
            d["fwd3"] = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]) / c
            d["rngr"] = rng / rng.shift(1).rolling(20).mean()
            d["sd20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["sd20"].shift(1)
            d["z6"] = d["ret6"] / (d["sd20"] * np.sqrt(6))
            d["alloc"] = b["postRebalance_current_allocation"]
            d["grid"] = (np.arange(len(b)) % 3 == 0)
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    g = df[df.grid & df.fwd3.notna() & df.vr.notna() & df.rngr.notna()].copy()
    g["ex"] = g.fwd3 - g.groupby("coin").fwd3.transform("mean")
    g["str"] = g.ex / g.groupby("coin").fwd3.transform("std")
    g["day"] = g.ts.dt.floor("D"); g["year"] = g.ts.dt.year

    def summ(sub):
        x = sub.ex; n = len(x)
        if n < 10: return pd.Series({"n": n})
        m = x.mean(); ds = (x - m).groupby(sub.day).sum()
        se = np.sqrt((ds**2).sum()) / n
        return pd.Series({"n": n, "mean_ex%": 100*m, "t_day": m/se, "strength": sub.str.mean()})

    def ols_t(sub, cols):
        X = np.column_stack([np.ones(len(sub))] + [sub[c].values for c in cols])
        y = sub.ex.values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(sub.day.values).sum().values
        G = sc.shape[0]
        V = XtXi @ (sc.T @ sc) @ XtXi * G / (G - 1)
        return pd.Series(beta[1:] / np.sqrt(np.diag(V))[1:], index=cols)

    out = {}
    g["lvr"] = np.log1p(g.vr.clip(lower=-0.99)); g["lrng"] = np.log(g.rngr.clip(lower=0.01))
    up = g[g.ret6 > 0]; dn = g[g.ret6 <= 0]
    out["up6: t of log vol ratio and log range ratio jointly"] = ols_t(up, ["lvr", "lrng"])
    out["down6: t jointly"] = ols_t(dn, ["lvr", "lrng"])
    out["all: t jointly"] = ols_t(g, ["lvr", "lrng"])
    out["up6 by range quintile"] = up.groupby(pd.qcut(up.rngr, 5), observed=True).apply(summ)
    out["down6 by range quintile"] = dn.groupby(pd.qcut(dn.rngr, 5), observed=True).apply(summ)
    hv = up[up.vr > 0]
    out["up6 heavy by z6 tercile"] = hv.groupby(pd.qcut(hv.z6, 3), observed=True).apply(summ)
    out["up6 heavy by sign of last day"] = hv.groupby(np.sign(hv.r1)).apply(summ)
    out["all by range quintile x year (top quintile only)"] = g[g.rngr > g.rngr.quantile(0.8)].groupby("year").apply(summ)
    out["held vs not: grid ex"] = g.groupby(g.alloc.fillna(0) > 0).apply(summ)
    return out

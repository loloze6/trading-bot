def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, b in data["bars"][coin].items():
        c = b["close"].astype(float).reset_index(drop=True)
        r = c.pct_change()
        d = pd.DataFrame({"w": w, "r": r})
        d["s30"] = r.rolling(30, min_periods=20).std()
        d["s5"] = r.rolling(5, min_periods=5).std()
        d["z"] = r / d["s30"]
        d["vr"] = d["s5"] / d["s30"]
        for h in (1, 2, 3, 5):
            d[f"f{h}"] = c.shift(-h) / c - 1
        d["pos"] = b["postRebalance_current_allocation"].values
        d["gain"] = d["pos"] * d["f1"]
        d["i"] = np.arange(len(d))
        ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
        d["yr"] = ts.dt.year.values
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    mus = {h: D[f"f{h}"][(D.i % h) == 0].mean() for h in (1, 2, 3, 5)}
    def reg(df, xcol, h):
        g = df[(df.i % h) == 0].dropna(subset=[f"f{h}", xcol])
        y = g[f"f{h}"] - mus[h]
        sl = stats.linregress(g[xcol], y)
        return {"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(g)}
    res = {}
    for h in (1, 2, 3, 5):
        res[f"down_z_h{h}"] = reg(D[D.z < 0], "z", h)
        res[f"up_z_h{h}"] = reg(D[D.z > 0], "z", h)
    out["fwd on z, down days vs up days"] = pd.DataFrame(res).T
    # down-day magnitude bins
    dn = D[D.z < 0].copy()
    dn["e1"] = dn.f1 - mus[1]
    dn["zb"] = pd.cut(dn.z, [-99, -2.5, -1.5, -1, -0.5, 0])
    t = dn.groupby("zb", observed=True)["e1"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next day after down days by z bin"] = t[["mean", "count", "t"]]
    up = D[D.z > 0].copy()
    up["e1"] = up.f1 - mus[1]
    up["zb"] = pd.cut(up.z, [0, 0.5, 1, 1.5, 2.5, 99])
    t = up.groupby("zb", observed=True)["e1"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next day after up days by z bin"] = t[["mean", "count", "t"]]
    # down-day reversal in raw return terms, graded by s30 tercile
    dn["s30q"] = pd.qcut(dn.s30.rank(method="first"), 3, labels=False)
    res = {}
    for q in range(3):
        res[q] = reg(dn[dn.s30q == q], "z", 1)
    out["down days: f1 on z by s30 tercile"] = pd.DataFrame(res).T
    # multiple regression all days: z, z*vr, z*s30 (std)
    g = D.dropna(subset=["f1", "z", "vr", "s30"]).copy()
    y = g.f1 - mus[1]
    X = np.column_stack([np.ones(len(g)), g.z, g.z * (g.vr - g.vr.mean()), g.z * (g.s30 - g.s30.mean()) / g.s30.std(), np.minimum(g.z, 0)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid.var(ddof=X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint regression f1"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z", "z*vr", "z*s30std", "min(z,0)"])
    # down-day fade by year
    big = dn[dn.z < -1]
    t = big.groupby("yr")["e1"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next day after z<-1 by year"] = t[["mean", "count", "t"]]
    return out

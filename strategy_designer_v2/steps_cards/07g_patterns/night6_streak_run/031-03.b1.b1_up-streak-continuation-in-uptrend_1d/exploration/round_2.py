import numpy as np, pandas as pd

def _cslope(x, y, days):
    d = pd.DataFrame({"x": x.values, "y": y.values, "d": days.values}).dropna()
    N = len(d)
    if N < 30: return (np.nan, np.nan, N, 0)
    X = np.column_stack([np.ones(N), d.x.values])
    beta = np.linalg.lstsq(X, d.y.values, rcond=None)[0]
    e = d.y.values - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    S = pd.DataFrame(X * e[:, None]).groupby(d.d.values).sum().values
    G = S.shape[0]
    V = XtXi @ (S.T @ S) @ XtXi * G / (G - 1)
    return (beta[1], beta[1] / np.sqrt(V[1, 1]), N, G)

def _ct(dev, days):
    d = pd.DataFrame({"v": dev.values, "d": days.values}).dropna()
    N = len(d)
    if N < 5: return (np.nan, np.nan, N, 0)
    m = d.v.mean(); g = d.groupby("d").v.agg(["sum", "count"]); G = len(g)
    r = g["sum"] - m * g["count"]
    se = np.sqrt(G / (G - 1) * (r ** 2).sum()) / N
    return (m, m / se, N, G)

def build(data, off):
    rows = []
    for coin, wins in data["bars"].items():
        parts = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            df = pd.DataFrame({"coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret30": c / c.shift(30) - 1, "ret5": c / c.shift(5) - 1,
                "ret10": c / c.shift(10) - 1,
                "fwd5": c.shift(-5) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float)})
            df["pos"] = np.arange(len(df))
            parts.append(df)
        cd = pd.concat(parts)
        g0 = cd[cd.pos % 5 == 0]
        drift = g0["fwd5"].mean()
        cd = cd[cd.pos % 5 == off].copy()
        cd["dev"] = cd["fwd5"] - drift
        rows.append(cd)
    A = pd.concat(rows).dropna(subset=["fwd5"])
    for col in ["ret30", "ret5", "ret10"]:
        A[col + "_p"] = A.groupby("coin")[col].rank(pct=True) - 0.5
    return A

def explore(data):
    out = []
    for off in range(5):
        A = build(data, off)
        dn = A[A.ret30 < 0]; up = A[A.ret30 > 0]
        tests = {
            "ret30pct_all": (A.ret30_p, A.dev, A.day),
            "ret5pct_r30neg": (dn.ret5_p, dn.dev, dn.day),
            "ret5pct_r30pos": (up.ret5_p, up.dev, up.day),
            "ret10pct_r30neg": (dn.ret10_p, dn.dev, dn.day),
            "ret10pct_r30pos": (up.ret10_p, up.dev, up.day),
        }
        for k, (x, y, d) in tests.items():
            s, t, n, G = _cslope(x, y, d)
            out.append({"offset": off, "test": k, "slope": round(s, 4), "t": round(t, 2), "n": n, "days": G})
    res = {"slopes_by_grid_offset": pd.DataFrame(out)}
    A = build(data, 0)
    dn = A[A.ret30 < 0].copy()
    dn["q"] = pd.qcut(dn.ret5_p, 5, labels=False)
    r = []
    for k, g in dn.groupby("q"):
        m, t, n, G = _ct(g.dev, g.day); r.append({"q": k, "mean_dev": round(m, 4), "t": round(t, 2), "n": n, "days": G})
    res["r30neg_ret5_quint"] = pd.DataFrame(r)
    A["yr"] = A.day.dt.year
    r = []
    for y, g in A.groupby("yr"):
        s, t, n, G = _cslope(g.ret30_p, g.dev, g.day); r.append({"yr": y, "slope": round(s, 4), "t": round(t, 2), "n": n})
    res["ret30_slope_by_year"] = pd.DataFrame(r)
    # book: in-position vs out mean coin return, trades by entry forecast
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tl.append(t)
    T = pd.concat(tl)
    T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
    res["trades_by_entry_fc_q"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), med_net=("net_profit_loss_percent", "median"),
        fc=("entry_forecast", "mean"), dur_d=("duration_minutes", lambda s: s.mean() / 1440))
    return res

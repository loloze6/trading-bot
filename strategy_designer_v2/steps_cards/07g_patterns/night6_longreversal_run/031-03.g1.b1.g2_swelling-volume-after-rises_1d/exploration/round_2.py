import numpy as np, pandas as pd

def _ct(vals, days):
    v = pd.Series(np.asarray(vals, float)); d = pd.Series(np.asarray(days))
    m = v.notna(); v = v[m]; d = d[m]
    n = len(v)
    if n < 5: return (np.nan, np.nan, n, 0)
    mu = v.mean(); s = (v - mu).groupby(d.values).sum()
    se = np.sqrt((s**2).sum()) / n
    return (mu, mu/se if se > 0 else np.nan, n, len(s))

def _slope_ct(x, y, days):
    x = np.asarray(x, float); y = np.asarray(y, float); d = np.asarray(days)
    m = ~np.isnan(x) & ~np.isnan(y); x, y, d = x[m], y[m], d[m]
    xc = x - x.mean(); b = (xc*(y-y.mean())).sum()/(xc**2).sum()
    e = (y - y.mean() - b*xc)
    s = pd.Series(xc*e).groupby(d).sum()
    se = np.sqrt((s**2).sum())/(xc**2).sum()
    return b, b/se, len(x)

def _grid(data, H):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "day": ts.dt.floor("D"), "yr": ts.dt.year,
                "ret14": c/c.shift(14)-1,
                "vr": v.rolling(14).mean()/v.rolling(30).mean()-1,
                "vr7": v.rolling(7).mean()/v.rolling(30).mean()-1,
                "fwd": c.shift(-H)/c-1, "pos": np.arange(len(b)),
            })
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows); g = g[g["fwd"].notna()].copy()
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    return g

def explore(data):
    out = {}
    res = []
    for H in (7, 14, 28):
        g = _grid(data, H)
        for col in ("vr", "vr7"):
            b, t, n = _slope_ct(g[col], g["ex"], g["day"])
            lo = g[g[col] <= g[col].quantile(0.2)]
            hi = g[g[col] >= g[col].quantile(0.8)]
            ml, tl, nl, dl = _ct(lo["ex"], lo["day"])
            mh, th, nh, dh = _ct(hi["ex"], hi["day"])
            res.append({"H_days": H, "x": col, "slope": b, "t": t, "n": n,
                        "low20_ex": ml, "low20_t": tl, "high20_ex": mh, "high20_t": th})
    out["volswell all bars by horizon"] = pd.DataFrame(res)
    g = _grid(data, 14)
    res = []
    for k, gg in g.groupby(g["yr"] <= 2021):
        b, t, n = _slope_ct(gg["vr"], gg["ex"], gg["day"])
        res.append({"early(<=2021)": k, "slope": b, "t": t, "n": n})
    out["vr slope by period half"] = pd.DataFrame(res)
    res = []
    for k, gg in g.groupby("coin"):
        if len(gg) < 30: continue
        b, t, n = _slope_ct(gg["vr"], gg["ex"], gg["day"])
        res.append({"coin": k, "slope": b, "t": t, "n": n})
    pc = pd.DataFrame(res)
    out["vr slope per coin"] = pc
    out["share coins slope>0"] = float((pc["slope"] > 0).mean())
    # vol swell with 14d return interaction: low swell & up vs down
    g["q"] = pd.qcut(g["vr"].rank(method="first"), 5, labels=False)
    res = []
    for (q, up), gg in g.groupby([g["q"], g["ret14"] > 0]):
        mu, t, n, nd = _ct(gg["ex"], gg["day"])
        res.append({"vr_q": q, "up14": up, "ex": mu, "t": t, "n": n})
    out["vr q x up14"] = pd.DataFrame(res)
    return out

import numpy as np, pandas as pd

def explore(data):
    out = {}
    rows = []
    H = [1, 2, 4, 6, 8]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=360).std()
            vr = v / v.rolling(720, min_periods=360).mean()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "z": r / sd, "vr": vr, "pos": np.arange(len(b)),
                              "year": ts.dt.year.values, "hour": ts.dt.hour.values,
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "fc": b["forecast"].astype(float)})
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    usual = {}
    for h in H:
        g = D[D.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean(); sdv = g.groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = D[f"f{h}"] - D.coin.map(dr)
        usual[h] = sdv
    out["usual 4h move by coin"] = usual[4]
    def st(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    # down hours: graded by (-z)*vr, horizons 2,4,6
    res = []
    for h in [2, 4, 6]:
        g = D[(D.pos % h == 0) & (D.z < 0)].dropna(subset=["z", "vr", f"x{h}"]).copy()
        g["s"] = -g.z * g.vr
        g["q"] = pd.qcut(g.s, [0, .5, .8, .9, .95, .98, .99, 1.0])
        for q, gg in g.groupby("q", observed=True):
            s = st(gg[f"x{h}"]); s["h"] = h; s["q"] = str(q); res.append(s)
    out["down hours: excess return by (-z*vr) quantile"] = pd.DataFrame(res)
    # top 2% down surges at h4: by coin, by year
    g = D[(D.pos % 4 == 0) & (D.z < 0)].dropna(subset=["z", "vr", "x4"]).copy()
    g["s"] = -g.z * g.vr
    thr = g.s.quantile(0.95)
    top = g[g.s >= thr]
    out["top 5% down surge x4 by coin"] = top.groupby("coin").x4.apply(st).unstack()
    out["top 5% down surge x4 by year"] = top.groupby("year").x4.apply(st).unstack()
    out["corr s vs x4 among down hours with vr>2 (spearman)"] = float(g[g.vr > 2][["s", "x4"]].corr("spearman").iloc[0, 1])
    # same for up hours (fade?)
    u = D[(D.pos % 4 == 0) & (D.z > 0)].dropna(subset=["z", "vr", "x4"]).copy()
    u["s"] = u.z * u.vr
    u["q"] = pd.qcut(u.s, [0, .5, .8, .9, .95, .98, .99, 1.0])
    out["up hours x4 by (z*vr) quantile"] = u.groupby("q", observed=True).x4.apply(st).unstack()
    # book: forecast persistence — how long forecast stays >0 after a signal
    D["inpos"] = D.alloc.abs() > 0.01
    out["share of in-position bars where this hour's z>0 & vr>1"] = float(((D.z > 0) & (D.vr > 1))[D.inpos].mean())
    out["share in-position bars whose forecast>=10"] = float((D.fc[D.inpos] >= 10).mean())
    # days: book vs coin by year
    dd = pd.concat([t.assign(coin=c, w=w) for c, ws in data["days"].items() for w, t in ws.items()])
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book & coin mean daily bp by year"] = dd.groupby("year")[["book_return", "coin_return"]].mean() * 1e4
    return out

import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [5, 10]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            hi = c.rolling(20).max()
            sd = r.rolling(20).std()
            depth = (c / hi - 1) / sd
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64"),
                              "depth": depth, "fc": b["forecast"].astype(float),
                              "raw": pd.to_numeric(b.get("debug_info.components.depth.last_history_value"), errors="coerce"),
                              "chop": (b["regime"] == "unknown")})
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {h: D[D.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in H}

    def clus(x, y, day):
        X = np.column_stack([np.ones(len(x)), x]); beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta; XtX = np.linalg.inv(X.T @ X)
        S = np.zeros((2, 2))
        for _, idx in pd.Series(np.arange(len(x))).groupby(day.values):
            s = X[idx.values].T @ e[idx.values]; S += np.outer(s, s)
        G = len(np.unique(day)); n = len(x)
        V = XtX @ S @ XtX * G / (G - 1) * (n - 1) / (n - 2)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), n, G

    res = []
    for h in H:
        g = D[(D.pos % h == 0) & D.chop].dropna(subset=["depth", f"f{h}"]).copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
        for name, sub, xcol in [("depth<0 on depth", g[g.depth < 0], "depth"),
                                ("fc!=0 on fc", g[g.fc != 0], "fc"),
                                ("fc!=0 on depth", g[g.fc != 0], "depth"),
                                ("all chop on depth", g, "depth")]:
            s, t, n, G = clus(sub[xcol].values, sub.ex.values, sub.day)
            res.append({"h": h, "set": name, "slope": s, "t_clustered": t, "n": n, "days": G,
                        "mean_ex": sub.ex.mean()})
    out["slopes"] = pd.DataFrame(res)
    a = D[D.chop & (D.fc != 0)].dropna(subset=["depth"])
    out["corr_fc_depth_active"] = float(a[["fc", "depth"]].corr().iloc[0, 1])
    a2 = D[D.chop].dropna(subset=["depth", "raw"])
    out["corr_raw_depth"] = float(a2[["raw", "depth"]].corr().iloc[0, 1])
    out["share_chop_depth_lt0_with_fc0"] = float((D[D.chop & (D.depth < 0)].fc == 0).mean())
    g = D[(D.pos % 5 == 0) & D.chop & (D.depth < 0)].dropna(subset=["f5"]).copy()
    g["ex"] = g.f5 - g.coin.map(drift[5])
    g["dq"] = pd.qcut(g.depth, 4, labels=False)
    out["h5_depth_quartile"] = g.groupby("dq").agg(n=("ex", "size"), depth=("depth", "mean"), mean_ex=("ex", "mean"))
    out["h5_by_coin_slope"] = g.groupby("coin").apply(lambda x: pd.Series({"n": len(x),
        "slope": stats.linregress(x.depth, x.ex).slope, "t": stats.linregress(x.depth, x.ex).slope / stats.linregress(x.depth, x.ex).stderr}))
    return out

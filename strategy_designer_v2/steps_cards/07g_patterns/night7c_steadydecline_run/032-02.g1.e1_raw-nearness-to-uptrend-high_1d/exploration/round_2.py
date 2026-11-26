import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            v = b["volume"].astype(float); r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                "ret28": c / c.shift(28) - 1,
                "dist": 1 - c / c.rolling(28).max(),
                "vol20": r1.rolling(20).std(),
                "vratio": r1.rolling(20).std() / r1.rolling(90, min_periods=40).std(),
                "vrel": v.rolling(28).mean() / v.rolling(90, min_periods=40).mean(),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def prep(H):
        G = A[(A["pos"] % H == 0) & A[f"f{H}"].notna()].copy()
        G["ex"] = G[f"f{H}"] - G.groupby("coin")[f"f{H}"].transform("mean")
        return G
    def slope(s, col):
        s = s.dropna(subset=[col, "ex"])
        if len(s) < 20: return [len(s), np.nan, np.nan]
        lr = stats.linregress(s[col], s["ex"])
        return [len(s), lr.slope, lr.slope / lr.stderr]
    def qtab(s, col, q=5):
        s = s.dropna(subset=[col, "ex"]).copy()
        s["q"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        t = s.groupby("q").agg(n=("ex", "size"), xmean=(col, "mean"), ex_mean=("ex", "mean"),
                               ex_t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
        return t
    G5 = prep(5); G10 = prep(10)
    for nm, G in [("h5", G5), ("h10", G10)]:
        tr = G[G["ret28"] > 0]; nt = G[G["ret28"] <= 0]
        res = {}
        for col in ["dist", "vol20", "vratio", "vrel"]:
            res["trend " + col] = slope(tr, col)
            res["down " + col] = slope(nt, col)
            res["all " + col] = slope(G, col)
        out[f"{nm} univariate slopes [n,slope,t]"] = pd.DataFrame(res, index=["n", "slope", "t"]).T
        # multivariate in trend
        s = tr.dropna(subset=["dist", "vratio", "vrel", "ex"])
        X = np.column_stack([np.ones(len(s)), s["dist"], s["vratio"], s["vrel"]])
        beta, *_ = np.linalg.lstsq(X, s["ex"].values, rcond=None)
        resid = s["ex"].values - X @ beta
        se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * resid.var(ddof=4))
        out[f"{nm} trend multivar"] = pd.DataFrame({"beta": beta, "t": beta / se},
                                                  index=["const", "dist", "vratio", "vrel"])
    tr = G5[G5["ret28"] > 0]
    out["h5 trend vratio quintiles"] = qtab(tr, "vratio")
    out["h5 down vratio quintiles"] = qtab(G5[G5["ret28"] <= 0], "vratio")
    out["h5 all dist quintiles"] = qtab(G5, "dist")
    out["h5 trend dist slope by year"] = pd.DataFrame({y: slope(g, "dist") for y, g in tr.groupby("yr")},
                                                       index=["n", "slope", "t"]).T
    out["h5 trend dist slope by coin"] = pd.DataFrame({y: slope(g, "dist") for y, g in tr.groupby("coin")},
                                                       index=["n", "slope", "t"]).T
    out["h5 trend vratio slope by coin"] = pd.DataFrame({y: slope(g, "vratio") for y, g in tr.groupby("coin")},
                                                       index=["n", "slope", "t"]).T
    out["h5 trend vrel slope by coin"] = pd.DataFrame({y: slope(g, "vrel") for y, g in tr.groupby("coin")},
                                                       index=["n", "slope", "t"]).T
    return out

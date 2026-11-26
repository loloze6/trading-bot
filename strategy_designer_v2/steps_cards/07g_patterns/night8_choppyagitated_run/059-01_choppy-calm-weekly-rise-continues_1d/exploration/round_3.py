import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            vol90 = r1.rolling(90, min_periods=45).std()
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(df)), "day": ts.dt.floor("D"), "yr": ts.dt.year,
                "s7": (c / c.shift(7) - 1) / (vol30 * np.sqrt(7)),
                "s3": (c / c.shift(3) - 1) / (vol30 * np.sqrt(3)),
                "tr60": c / c.shift(60) - 1, "ag": vol30 / vol90,
                "f7": c.shift(-7) / c - 1, "f3": c.shift(-3) / c - 1,
                "inprof": (df["regime"] == "unknown").astype(int)}))
    A = pd.concat(rows, ignore_index=True)
    A["trend"] = pd.cut(A["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    A["agq"] = np.where(A["ag"] > 1, "agit", "calm"); A.loc[A["ag"].isna(), "agq"] = np.nan

    def clslope(g, x, y):
        g = g.dropna(subset=[x, y])
        X = np.column_stack([np.ones(len(g)), g[x].values]); Y = g[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        S = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            v = (X[idx] * e[idx, None]).sum(0); S += np.outer(v, v)
        G = g["day"].nunique(); V = XtXi @ S @ XtXi * G / max(G - 1, 1)
        return len(g), G, b[1], b[1] / np.sqrt(V[1, 1])

    res = {}
    out = []
    for h, sc, fc in [(7, "s7", "f7"), (3, "s3", "f3")]:
        g = A[A["pos"] % h == 0].copy()
        g["x"] = g[fc] - g["coin"].map(g.groupby("coin")[fc].mean())
        for k, gg in g.groupby(["trend", "agq"], observed=True):
            n, G, b, t = clslope(gg, sc, "x"); out.append((f"{h}d", k[0], k[1], n, G, b, t))
        if h == 7:
            G7 = g
        else:
            G3 = g
    res["clustered slopes"] = pd.DataFrame(out, columns=["h", "trend", "agit", "n", "days", "slope", "t_clu"]).round(4)
    # falling calm 7d: by year, by sign of s7
    fc_ = G7[(G7["trend"] == "fall") & (G7["agq"] == "calm")].dropna(subset=["x", "s7"])
    out = []
    for y, gg in fc_.groupby("yr"):
        if len(gg) > 10: n, G, b, t = clslope(gg, "s7", "x"); out.append((y, n, b, t))
    res["fall calm 7d slope by year"] = pd.DataFrame(out, columns=["yr", "n", "slope", "t"]).round(4)
    fc_ = fc_.copy(); fc_["q"] = pd.qcut(fc_["s7"], 4, labels=False)
    res["fall calm 7d excess by s7 quartile"] = fc_.groupby("q").agg(n=("x", "size"), s7=("s7", "mean"), mean=("x", "mean")).round(4)
    out = []
    for sgn, gg in fc_.groupby(np.sign(fc_["s7"])):
        n, G, b, t = clslope(gg, "s7", "x"); out.append((sgn, n, gg["x"].mean(), b, t))
    res["fall calm 7d by s7 sign"] = pd.DataFrame(out, columns=["sign", "n", "mean_x", "slope", "t"]).round(4)
    # chop agit 3d by year and quartile
    ca = G3[(G3["trend"] == "chop") & (G3["agq"] == "agit")].dropna(subset=["x", "s3"]).copy()
    out = []
    for y, gg in ca.groupby("yr"):
        if len(gg) > 8: n, G, b, t = clslope(gg, "s3", "x"); out.append((y, n, b, t))
    res["chop agit 3d slope by year"] = pd.DataFrame(out, columns=["yr", "n", "slope", "t"]).round(4)
    ca["q"] = pd.qcut(ca["s3"], 4, labels=False)
    res["chop agit 3d excess by s3 quartile"] = ca.groupby("q").agg(n=("x", "size"), s3=("s3", "mean"), mean=("x", "mean")).round(4)
    # fall agit 7d reversal by year
    fa = G7[(G7["trend"] == "fall") & (G7["agq"] == "agit")].dropna(subset=["x", "s7"])
    out = []
    for y, gg in fa.groupby("yr"):
        if len(gg) > 10: n, G, b, t = clslope(gg, "s7", "x"); out.append((y, n, b, t))
    res["fall agit 7d slope by year"] = pd.DataFrame(out, columns=["yr", "n", "slope", "t"]).round(4)
    # in-profile slope (tested idea, all s7 sign) clustered
    ip = G7[G7["inprof"] == 1]
    res["in-profile 7d slope all signs"] = str(tuple(np.round(clslope(ip, "s7", "x"), 4)))
    return res

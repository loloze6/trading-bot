import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            day = ts.dt.floor("D").astype("int64").values
            lr = np.log(c)
            n = len(c)
            h = 10
            for i in range(0, n, h):
                if i + h >= n:
                    break
                r20 = c[i]/c[i-20]-1 if i >= 20 else np.nan
                vol = np.std(np.diff(lr[max(0, i-60):i+1]), ddof=1)*np.sqrt(20) if i >= 30 else np.nan
                rows.append((coin, w, i, yr[i], day[i], f[i], c[i+h]/c[i]-1, r20, vol))
    d = pd.DataFrame(rows, columns=["coin","win","i","year","day","fc","fwd","r20","vol20"])
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["z20"] = d["r20"]/d["vol20"]

    def cl_t(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 20 or g[x].std() == 0:
            return pd.Series({"n": len(g), "days": np.nan, "slope": np.nan, "t_cl": np.nan})
        X = np.column_stack([np.ones(len(g)), g[x].values])
        y = g["ex"].values
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        S = np.zeros((2, 2))
        for _, idx in pd.Series(np.arange(len(g))).groupby(g["day"].values):
            s = (X[idx.values] * e[idx.values, None]).sum(0)
            S += np.outer(s, s)
        G = g["day"].nunique(); N = len(g)
        V = XtX @ S @ XtX * G/(G-1)*(N-1)/(N-2)
        return pd.Series({"n": N, "days": G, "slope": b[1], "t_cl": b[1]/np.sqrt(V[1, 1])})

    out = {}
    out["clustered t, h10, by predictor"] = pd.DataFrame(
        {x: cl_t(d, x) for x in ["fc", "r20", "z20"]}).T
    d["side"] = np.sign(d["r20"])
    out["z20 by side (clustered)"] = d.groupby("side").apply(lambda g: cl_t(g, "z20"))
    out["r20 by side (clustered)"] = d.groupby("side").apply(lambda g: cl_t(g, "r20"))
    dd = d.dropna(subset=["z20"]).copy()
    dd["q"] = pd.qcut(dd["z20"], 6, labels=False)
    out["z20 sextiles: mean z20, mean ex, t, n"] = dd.groupby("q").apply(
        lambda g: pd.Series({"z20": g.z20.mean(), "r20": g.r20.mean(), "ex": g.ex.mean(),
                             "t": g.ex.mean()/(g.ex.std(ddof=1)/np.sqrt(len(g))), "n": len(g)}))
    out["z20 by year (clustered)"] = d.groupby("year").apply(lambda g: cl_t(g, "z20"))
    out["z20 by coin (clustered)"] = d.groupby("coin").apply(lambda g: cl_t(g, "z20"))
    out["corr fc vs z20"] = float(d[["fc", "z20"]].dropna().corr().iloc[0, 1])
    return out

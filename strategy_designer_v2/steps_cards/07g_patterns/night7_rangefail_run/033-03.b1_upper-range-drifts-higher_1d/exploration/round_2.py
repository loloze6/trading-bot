def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["ret1"] = c.pct_change()
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            b["rpos"] = (c - lo20) / (hi20 - lo20) - 0.5
            b["vol30"] = b["ret1"].rolling(30).std()
            b["vol10"] = b["ret1"].rolling(10).std()
            b["vrank"] = b["vol30"].rolling(200, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            b["vratio"] = b["vol10"] / b["vol30"]
            b["tr60"] = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            b["day"] = ts.dt.floor("D"); b["coin"] = coin; b["win"] = w
            rows.append(b.iloc[::H])
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    out = {}
    def cl_t(d, x):
        d = d.dropna(subset=[x, "ex"])
        X = d[x] - d[x].mean(); y = d["ex"]
        b = (X * y).sum() / (X ** 2).sum()
        a = y.mean()
        e = y - a - b * X
        s = (X * e).groupby(d["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return len(d), d["day"].nunique(), round(b, 4), round(b / se, 2)
    G["calm_own"] = np.where(G["vrank"] <= 0.5, "calm", "agit")
    r = {}
    for k, d in G.dropna(subset=["vrank"]).groupby("calm_own"):
        r[k] = cl_t(d, "rpos")
    out["rpos slope clustered by own-vol-rank calm/agit (n,days,slope,t)"] = pd.DataFrame(r, index=["n", "days", "slope", "t"]).T
    G["vrq"] = pd.qcut(G["vrank"], 4, labels=False, duplicates="drop")
    r = {}
    for k, d in G.dropna(subset=["vrq"]).groupby("vrq"):
        r[k] = cl_t(d, "rpos")
    out["rpos slope by vol-rank quartile"] = pd.DataFrame(r, index=["n", "days", "slope", "t"]).T
    calm = G[G["calm_own"] == "calm"]
    r = {}
    for k, d in calm.groupby("win"):
        if len(d) > 10:
            r[k] = cl_t(d, "rpos")
    out["calm: rpos slope by window"] = pd.DataFrame(r, index=["n", "days", "slope", "t"]).T
    r = {}
    for k, d in calm.groupby("coin"):
        r[k] = cl_t(d, "rpos")
    out["calm: rpos slope by coin"] = pd.DataFrame(r, index=["n", "days", "slope", "t"]).T
    calm = calm.copy(); calm["rq"] = pd.qcut(calm["rpos"], 4, labels=False, duplicates="drop")
    out["calm: ex by rpos quartile"] = calm.groupby("rq")["ex"].agg(["count", "mean"]).round(4)
    # vol10 effect clustered
    G["lv10"] = np.log(G["vol10"]); G["lvr"] = np.log(G["vratio"])
    out["slope ex on log vol10 (n,days,slope,t)"] = pd.Series(cl_t(G, "lv10"), index=["n", "days", "slope", "t"])
    out["slope ex on log vol10/vol30"] = pd.Series(cl_t(G, "lvr"), index=["n", "days", "slope", "t"])
    r = {}
    for k, d in G.groupby("win"):
        r[k] = cl_t(d, "lvr")
    out["vol ratio slope by window"] = pd.DataFrame(r, index=["n", "days", "slope", "t"]).T
    G["vrq2"] = pd.qcut(G["vratio"], 4, labels=False, duplicates="drop")
    out["ex by vol10/vol30 quartile"] = G.groupby("vrq2")["ex"].agg(["count", "mean", "std"]).round(4)
    r = {}
    for k, d in G.groupby("coin"):
        r[k] = cl_t(d, "lvr")
    out["vol ratio slope by coin"] = pd.DataFrame(r, index=["n", "days", "slope", "t"]).T
    return out

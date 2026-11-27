def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in (1, 2, 3, 5, 10):
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs) if rs else np.nan, np.std(rs) if rs else np.nan)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(n):
                if f[i] < 0 and (i == 0 or f[i - 1] >= 0):
                    loc = (c[i] - lo[i]) / (hi[i] - lo[i]) if hi[i] > lo[i] else np.nan
                    r5 = c[i] / c[i - 5] - 1 if i >= 5 else np.nan
                    d = {"coin": coin, "win": w, "i": i, "day": str(df["timestamp"].iloc[i])[:10],
                         "f": f[i], "loc": loc, "r5": r5,
                         "year": pd.Timestamp(df["timestamp"].iloc[i]).year}
                    for h in (1, 2, 3, 5, 10):
                        if i + h < n:
                            d[f"ex{h}"] = -(c[i + h] / c[i] - 1 - drift[(coin, h)][0])
                            d[f"tot{h}"] = -(c[i + h] / c[i] - 1)
                        else:
                            d[f"ex{h}"] = np.nan; d[f"tot{h}"] = np.nan
                    rows.append(d)
    E = pd.DataFrame(rows)

    def tday(s, days):
        g = pd.DataFrame({"v": s, "d": days}).dropna()
        dev = g["v"] - g["v"].mean()
        sd = dev.groupby(g["d"]).sum()
        D = len(sd)
        se = np.sqrt((sd ** 2).sum() * D / (D - 1)) / len(g) if D > 1 else np.nan
        return g["v"].mean(), g["v"].mean() / se if se else np.nan, len(g), D

    out = {}
    hz = []
    for h in (1, 2, 3, 5, 10):
        m, t, n, D = tday(E[f"ex{h}"], E["day"])
        mt, tt, _, _ = tday(E[f"tot{h}"], E["day"])
        hz.append({"h": h, "ex_mean": m, "t": t, "n": n, "days": D, "tot_mean": mt, "tot_t": tt})
    out["by_horizon_entries"] = pd.DataFrame(hz)

    def grp(key):
        r = []
        for k, g in E.groupby(key):
            m, t, n, D = tday(g["ex3"], g["day"])
            m1, t1, _, _ = tday(g["ex1"], g["day"])
            r.append({"grp": k, "ex3": m, "t3": t, "ex1": m1, "t1": t1, "n": n, "days": D})
        return pd.DataFrame(r)
    out["by_coin"] = grp("coin")
    out["by_year"] = grp("year")
    E["fq"] = pd.qcut(E["f"], 4, labels=False, duplicates="drop")
    E["locq"] = pd.qcut(E["loc"], 4, labels=False, duplicates="drop")
    E["r5q"] = pd.qcut(E["r5"], 4, labels=False, duplicates="drop")
    out["by_forecast_q (0=most negative)"] = grp("fq")
    out["by_loc_q (3=nearest high)"] = grp("locq")
    out["by_r5_q (0=deepest)"] = grp("r5q")
    out["regimes"] = pd.Series({r: sum((df["regime"].astype(str) == r).sum() for ws in bars.values() for df in ws.values()) for r in set(str(x) for ws in bars.values() for df in ws.values() for x in df["regime"].unique())})
    return out

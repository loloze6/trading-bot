def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            allr.append(pd.Series(df["close"].values.astype(float)).pct_change().dropna().values)
        mu = np.concatenate(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values.astype(float)
            raw = df.get("debug_info.components.scaled_week.last_history_value")
            raw = raw.values.astype(float) if raw is not None else np.full(len(c), np.nan)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "i": i, "f": f[i], "raw": raw[i],
                     "day": ts.iloc[i].normalize()}
                for h in (1, 3, 7):
                    r[f"r{h}"] = c[i+h]/c[i]-1 - h*mu if i+h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    a = d[d.f != 0].copy()
    a["s"] = np.sign(a.f)

    def cl_slope(sub, xcol, ycol):
        sub = sub.dropna(subset=[xcol, ycol])
        x = sub[xcol].values; y = sub[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        S = pd.DataFrame(X * e[:, None], index=sub["day"].values).groupby(level=0).sum().values
        V = XtX @ (S.T @ S) @ XtX
        return b[1], b[1]/np.sqrt(V[1, 1]), len(sub), sub["day"].nunique()

    def tday(sub, col):
        sub = sub.dropna(subset=[col])
        m = sub[col].mean()
        g = sub.groupby("day")[col].agg(["sum", "count"])
        se = np.sqrt(((g["sum"] - g["count"]*m)**2).sum())/len(sub)
        return m, m/se, len(sub), g.shape[0]

    out = {}
    res = {}
    for h in (1, 3, 7):
        sub = a[a.i % h == 0].copy()
        sub["x"] = sub.s * sub[f"r{h}"]
        sub["fx"] = sub.f/10
        sub["rawabs"] = sub.raw.abs()
        res[f"h{h} slope f/10"] = cl_slope(sub, "fx", f"r{h}")
        res[f"h{h} slope raw"] = cl_slope(sub, "raw", f"r{h}")
        res[f"h{h} signed |raw| slope"] = cl_slope(sub, "rawabs", "x")
        res[f"h{h} signed mean"] = tday(sub, "x")
    out["clustered slopes (b,t,n,days)"] = pd.DataFrame(res, index=["b", "t", "n", "days"]).T

    a7 = a[a.i % 7 == 0].copy()
    a7["x"] = a7.s * a7.r7
    yr = {}
    for y, sub in a7.groupby("year"):
        yr[str(y)] = tday(sub, "x")
    for coin, sub in a7.groupby("coin"):
        yr[coin] = tday(sub, "x")
    a7["q"] = pd.qcut(a7.raw.abs(), 4, labels=False, duplicates="drop")
    for q, sub in a7.groupby("q"):
        yr[f"|raw| q{int(q)}"] = tday(sub, "x")
    out["h7 signed mean by year/coin/|raw| q"] = pd.DataFrame(yr, index=["mean", "t", "n", "days"]).T

    a1 = a.copy()
    a1["x"] = a1.s * a1.r1
    a1["q"] = pd.qcut(a1.raw.abs(), 4, labels=False, duplicates="drop")
    out["h1 signed mean by |raw| q"] = pd.DataFrame({f"q{int(q)}": tday(s, "x") for q, s in a1.groupby("q")},
                                                    index=["mean", "t", "n", "days"]).T
    out["raw recorded share"] = float(a.raw.notna().mean())
    return out

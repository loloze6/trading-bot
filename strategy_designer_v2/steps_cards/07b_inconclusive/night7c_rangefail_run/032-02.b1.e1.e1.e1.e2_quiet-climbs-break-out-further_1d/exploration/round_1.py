def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    allret = {}
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            for h in (5, 10, 20, 40):
                idx = np.arange(0, n - h, h)
                if len(idx):
                    allret.setdefault((coin, h), []).extend(list(c.values[idx + h] / c.values[idx] - 1))
            prevmax = c.shift(1).rolling(60).max()
            r60 = c.shift(1) / c.shift(61) - 1
            m = r60.abs().rolling(120, min_periods=60).mean()
            vol20 = np.log(c).diff().rolling(20).std()
            dist = (c / prevmax - 1)
            brk = c > prevmax
            seen = set()
            for t in range(n):
                if not brk.iloc[t] or t + 40 >= n:
                    continue
                cell = t // 20
                if cell in seen:
                    continue
                seen.add(cell)
                d = {"coin": coin, "w": w, "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[t]).date()),
                     "r60": r60.iloc[t], "m": m.iloc[t], "dist": dist.iloc[t],
                     "distv": dist.iloc[t] / vol20.iloc[t] if vol20.iloc[t] > 0 else np.nan,
                     "wgt": max(0, 1 - r60.iloc[t] / m.iloc[t]) if m.iloc[t] > 0 else np.nan}
                for h in (5, 10, 20, 40):
                    d[f"f{h}"] = c.iloc[t + h] / c.iloc[t] - 1
                rows.append(d)
    X = pd.DataFrame(rows)
    for h in (5, 10, 20, 40):
        X[f"e{h}"] = X[f"f{h}"] - X["coin"].map(lambda k: np.mean(allret[(k, h)]))
    X["r60m"] = X["r60"] / X["m"]
    out = {}
    out["n"] = len(X)
    def slope_t(x, y):
        ok = ~(np.isnan(x) | np.isnan(y))
        r = stats.linregress(x[ok], y[ok]); return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": ok.sum()})
    tab = {}
    for h in (5, 10, 20, 40):
        for v in ("wgt", "r60m", "r60", "dist", "distv"):
            tab[f"e{h}~{v}"] = slope_t(X[v].values, X[f"e{h}"].values)
        e = X[f"e{h}"]; tab[f"e{h}_mean"] = pd.Series({"slope": e.mean(), "t": e.mean() / e.std() * np.sqrt(len(e)), "n": len(e)})
    out["slopes"] = pd.DataFrame(tab).T
    X["q"] = pd.qcut(X["r60m"], 4, labels=["q1low", "q2", "q3", "q4high"])
    out["by_runup_q"] = X.groupby("q")[["e5", "e10", "e20", "e40", "r60m"]].agg(["mean", "count"]).iloc[:, [0, 2, 4, 6, 8, 9]]
    X["dq"] = pd.qcut(X["distv"], 4, labels=["d1", "d2", "d3", "d4"])
    out["by_dist_q"] = X.groupby("dq")[["e10", "e20", "e40", "distv"]].mean()
    out["by_coin"] = X.groupby("coin")["e20"].agg(["mean", "count"])
    out["by_year"] = X.groupby("year")["e20"].agg(["mean", "count"])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["r0"] = c.pct_change()
            d["n1"] = c.shift(-1) / c - 1
            d["n2"] = c.shift(-2) / c - 1
            rng = (b["high"] - b["low"]).astype(float)
            d["cl"] = (c - b["low"]) / rng.replace(0, np.nan)
            d["range"] = rng / c.shift(1)
            d["agit"] = (b["regime"] == "unknown").astype(int)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["vol20"] = d["r0"].rolling(20).std()
            d["vol30"] = d["r0"].rolling(30).std()
            d["vol365med"] = d["vol30"].rolling(365, min_periods=60).median()
            d["vratio"] = d["vol30"] / d["vol365med"]
            vol = b["volume"].astype(float)
            d["vrel"] = vol / vol.rolling(20).mean().shift(1)
            d["r5p"] = c.shift(1) / c.shift(6) - 1
            d["r60"] = c / c.shift(60) - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["n1"].mean()
    D["x1"] = D["n1"] - D["coin"].map(mu)
    sd = D.groupby("coin")["r0"].std()
    D["z0"] = D["r0"] / D["coin"].map(sd)
    D["zl"] = D["r0"] / D["vol20"]
    D["rr"] = D["range"] / D["vol20"]
    D["wick"] = D["range"] / D["r0"].abs().replace(0, np.nan)
    out = {}
    def ols(df, ys, xs):
        df = df.dropna(subset=[ys] + xs)
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs])
        y = df[ys].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + xs).assign(n=len(y))
    A = D[D.agit == 1]
    falls = A[A.r0 < 0].copy()
    falls["fall"] = -falls["zl"]
    falls["fallz"] = -falls["z0"]
    falls["rrx"] = falls["rr"]
    out["agit falls: x1 on fallz + range/vol20"] = ols(falls, "x1", ["fallz", "rrx"])
    out["agit falls: x1 on fallz + fall/vol20"] = ols(falls, "x1", ["fallz", "fall"])
    out["agit falls: x1 on fallz + vrel"] = ols(falls, "x1", ["fallz", "vrel"])
    out["agit falls: x1 on fallz + vratio"] = ols(falls, "x1", ["fallz", "vratio"])
    out["agit falls: x1 on fallz + prior5d ret"] = ols(falls, "x1", ["fallz", "r5p"])
    # range beyond fall: lower wick (close above low) vs range
    falls["lowwick"] = (falls["cl"] * falls["range"]) / falls["vol20"]
    out["agit falls: x1 on fallz + lowwick/vol20"] = ols(falls, "x1", ["fallz", "lowwick"])
    # up days agitated: reversal graded
    ups = A[A.r0 > 0].copy(); ups["upz"] = ups["z0"]
    out["agit ups: x1 on upz"] = ols(ups, "x1", ["upz"])
    cu = D[(D.agit == 0) & (D.r0 > 0)].copy(); cu["upz"] = cu["z0"]
    out["calm ups: x1 on upz"] = ols(cu, "x1", ["upz"])
    cf = D[(D.agit == 0) & (D.r0 < 0)].copy(); cf["fallz"] = -cf["z0"]
    out["calm falls: x1 on fallz"] = ols(cf, "x1", ["fallz"])
    # agitated ups by coin, year
    ups["yr"] = None
    def tab(df, key, val):
        g = df.dropna(subset=[key, val]).groupby(key)[val]
        r = g.agg(["mean", "count", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    out["agit ups 0.3<z<1 by coin"] = tab(A[(A.z0 > 0.3) & (A.z0 < 1)], "coin", "x1")
    # trend split of agitated falls
    falls["tr"] = pd.cut(falls["r60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    falls["big"] = (falls["fallz"] > 1).astype(int)
    out["agit falls z<-1 by trend"] = tab(falls[falls.big == 1], "tr", "x1")
    out["agit falls slope by trend"] = pd.concat({k: ols(g, "x1", ["fallz"]).loc["fallz"] for k, g in falls.groupby("tr")}, axis=1).T
    # vratio grading of big falls
    bf = falls[falls.big == 1].copy()
    bf["vq"] = pd.qcut(bf["vratio"], 3, duplicates="drop")
    out["agit z<-1 falls next1 by vratio tercile"] = tab(bf, "vq", "x1")
    # weekday on agit falls
    out["weekday x1, all bars, calm only"] = tab(D[D.agit == 0], "wd", "x1")
    out["weekday x1, agit only"] = tab(A, "wd", "x1")
    return out

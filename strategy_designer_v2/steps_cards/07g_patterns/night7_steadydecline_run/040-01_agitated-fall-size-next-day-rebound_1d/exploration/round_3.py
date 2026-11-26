def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["r0"] = c.pct_change()
            d["n1"] = c.shift(-1) / c - 1
            d["n2"] = c.shift(-2) / c - 1
            d["agit"] = (b["regime"] == "unknown").astype(int)
            d["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            d["r60"] = c / c.shift(60) - 1
            vol = b["volume"].astype(float)
            d["vrel"] = vol / vol.rolling(20).mean().shift(1)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in [1, 2]:
        mu = D[D.pos % h == 0].groupby("coin")["n%d" % h].mean()
        D["x%d" % h] = D["n%d" % h] - D["coin"].map(mu)
    sd = D.groupby("coin")["r0"].std()
    D["fallz"] = -D["r0"] / D["coin"].map(sd)
    D["tr"] = pd.cut(D["r60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    def ols(df, ys, xs):
        df = df.dropna(subset=[ys] + xs)
        if len(df) < 10:
            return pd.Series({"beta": np.nan, "t": np.nan, "n": len(df)})
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs])
        y = df[ys].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.Series({"beta": beta[1], "t": beta[1] / se[1], "n": len(y)})
    F = D[D.r0 < 0]
    out = {}
    out["slope x1 on fallz by agit x trend"] = pd.DataFrame({f"{a}_{t}": ols(g, "x1", ["fallz"]) for (a, t), g in F.groupby(["agit", "tr"])}).T
    FA = F[(F.agit == 1) & (F.tr == "falling")]
    out["falling agit slope by coin"] = pd.DataFrame({k: ols(g, "x1", ["fallz"]) for k, g in FA.groupby("coin")}).T
    out["falling agit slope by year"] = pd.DataFrame({k: ols(g, "x1", ["fallz"]) for k, g in FA.groupby("yr")}).T
    out["falling agit slope by window"] = pd.DataFrame({k: ols(g, "x1", ["fallz"]) for k, g in FA.groupby("win")}).T
    FA2 = FA[FA.pos % 2 == 0]
    out["falling agit 2-day slope (grid 2)"] = ols(FA2, "x2", ["fallz"])
    RA = F[(F.agit == 1) & (F.tr == "rising")]
    out["share of book position bars by trend (agit)"] = D[(D.alloc > 0)].groupby("tr")["alloc"].agg(["count", "mean"])
    out["falling agit: x1 on fallz + vrel"] = ols(FA, "x1", ["fallz", "vrel"])
    return out

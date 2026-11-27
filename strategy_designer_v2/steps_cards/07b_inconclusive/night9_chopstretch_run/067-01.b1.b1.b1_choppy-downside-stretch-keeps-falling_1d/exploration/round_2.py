def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    hs = [1, 2, 3, 5, 10]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in hs:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            sma = c.rolling(20).mean()
            sd = c.pct_change().rolling(20).std()
            stretch = (c - sma) / sma / sd
            n = len(df)
            for i in range(0, n - 5, 5):
                rec = {"coin": coin, "win": w, "fc": df["forecast"].iloc[i], "stretch": stretch.iloc[i],
                       "regime": df["regime"].iloc[i], "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date())}
                for h in hs:
                    if i + h < n:
                        rec[f"ex{h}"] = c.iloc[i + h] / c.iloc[i] - 1 - drift[h]
                rows.append(rec)
    d = pd.DataFrame(rows)
    ch = d[(d["regime"] == "unknown")].dropna(subset=["stretch", "ex5"]).copy()
    out = {}
    def ols_cl(x, y, g):
        x = np.asarray(x, float); y = np.asarray(y, float)
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for gg in pd.unique(g):
            m = (g == gg)
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        G = len(pd.unique(g)); N = len(x)
        V = XtXi @ meat @ XtXi * G / (G - 1) * (N - 1) / (N - 2)
        return b[1], b[1] / np.sqrt(V[1, 1]), N
    res = {}
    for h in hs:
        s = ch.dropna(subset=[f"ex{h}"])
        neg = s[s["stretch"] < 0]
        b, t, n = ols_cl(s["stretch"], s[f"ex{h}"], s["day"].values)
        b2, t2, n2 = ols_cl(neg["stretch"], neg[f"ex{h}"], neg["day"].values)
        pos = s[s["stretch"] > 0]
        b3, t3, n3 = ols_cl(pos["stretch"], pos[f"ex{h}"], pos["day"].values)
        res[f"h{h}"] = {"all_slope": b, "all_t": t, "n": n, "neg_slope": b2, "neg_t": t2, "n_neg": n2,
                        "pos_slope": b3, "pos_t": t3, "n_pos": n3}
    out["choppy slope of excess on raw stretch, clustered by day"] = pd.DataFrame(res).T
    negf = ch[ch["fc"] < 0]
    b, t, n = ols_cl(negf["fc"], negf["ex5"], negf["day"].values)
    out["choppy fc<0: slope on forecast (my sample)"] = f"slope={b:.5f}, t={t:.2f}, n={n}"
    b, t, n = ols_cl(negf["stretch"], negf["ex5"], negf["day"].values)
    out["choppy fc<0: slope on raw stretch"] = f"slope={b:.5f}, t={t:.2f}, n={n}"
    out["corr fc vs raw stretch, fc<0"] = float(negf[["fc", "stretch"]].corr().iloc[0, 1])
    def wsl(g):
        if len(g) < 6: return pd.Series({"n": len(g), "corr": np.nan, "mean_ex5_deep": np.nan})
        deep = g[g["stretch"] < -1.5]["ex5"]
        return pd.Series({"n": len(g), "corr": g[["stretch", "ex5"]].corr().iloc[0, 1],
                          "mean_ex5_deep": deep.mean(), "n_deep": len(deep)})
    out["choppy by window"] = ch.groupby("win").apply(wsl)
    out["choppy by coin"] = ch.groupby("coin").apply(wsl)
    ch["sb"] = pd.cut(ch["stretch"], [-10, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 10])
    out["choppy by raw stretch band"] = ch.groupby("sb").agg(n=("ex5", "size"), ex1=("ex1", "mean"), ex5=("ex5", "mean"), ex10=("ex10", "mean"))
    return out

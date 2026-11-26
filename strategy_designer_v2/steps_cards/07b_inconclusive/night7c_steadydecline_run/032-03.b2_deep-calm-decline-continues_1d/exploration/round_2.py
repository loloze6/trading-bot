def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        means = {}
        for h in (5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            means[h] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ret28 = pd.Series(c).pct_change(28).values
            ret14 = pd.Series(c).pct_change(14).values
            yr = pd.Timestamp(df["timestamp"].iloc[0]).year
            for i in range(0, len(c) - 10, 10):
                r = {"coin": coin, "win": w, "year": yr, "fc": df["forecast"].iloc[i],
                     "thin": df["regime"].iloc[i] == "trending", "ret28": ret28[i], "ret14": ret14[i],
                     "day": pd.Timestamp(df["timestamp"].iloc[i]).normalize()}
                for h in (5, 10, 20):
                    r[f"s{h}"] = -(c[i + h] / c[i] - 1 - means[h]) if i + h < len(c) else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def cl_slope(sub, x, y):
        s = sub[[x, y, "day"]].dropna()
        if len(s) < 15:
            return pd.Series({"n": len(s)})
        X = np.column_stack([np.ones(len(s)), s[x].values])
        Y = s[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]
        e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in s.groupby("day").indices.items():
            g = X[idx].T @ e[idx]
            meat += np.outer(g, g)
        G = s["day"].nunique()
        n = len(s)
        V = XtXi @ meat @ XtXi * G / (G - 1) * (n - 1) / (n - 2)
        return pd.Series({"n": n, "days": G, "slope": b[1], "t_cl": b[1] / np.sqrt(V[1, 1]), "mean_y": Y.mean()})

    out = {}
    cases = d[(d.thin) & (d.fc < 0)].copy()
    cases["nfc"] = -cases["fc"]
    cases["f28"] = -cases["ret28"]
    out["std_fc_clustered"] = pd.DataFrame({h: cl_slope(cases, "nfc", f"s{h}") for h in (5, 10, 20)}).T
    out["raw28_clustered"] = pd.DataFrame({h: cl_slope(cases, "f28", f"s{h}") for h in (5, 10, 20)}).T
    thinfall = d[(d.thin) & (d.ret28 < 0)].copy()
    thinfall["f28"] = -thinfall["ret28"]
    out["thin_all_falls_raw28"] = pd.DataFrame({h: cl_slope(thinfall, "f28", f"s{h}") for h in (5, 10, 20)}).T
    thinfall["q"] = pd.qcut(thinfall["f28"], 4, labels=False)
    out["thin_raw28_quartiles"] = thinfall.groupby("q").agg(n=("s10", "size"), ret28=("ret28", "mean"),
                                                             s5=("s5", "mean"), s10=("s10", "mean"), s20=("s20", "mean"))
    out["thin_raw28_by_year"] = thinfall.groupby("year").apply(lambda g: cl_slope(g, "f28", "s10"))
    out["corr_fc_ret28"] = float(cases[["nfc", "f28"]].corr().iloc[0, 1])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        # normal drift per horizon: non-overlapping grid over all windows
        for h in H:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ret = c.pct_change()
            sd = ret.rolling(20).std()
            z = ret / sd
            f = df["forecast"].fillna(0)
            fprev = f.shift(1).fillna(0)
            ret90 = c / c.shift(90) - 1
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(n):
                rec = {"coin": coin, "w": w, "i": i, "z": z.iloc[i], "f": f.iloc[i],
                       "case": (f.iloc[i] <= -2) and (fprev.iloc[i] - f.iloc[i] >= 2),
                       "falling": df["regime"].iloc[i] == "mean_reversion",
                       "ret90": ret90.iloc[i], "year": ts.iloc[i].year}
                for h in H:
                    rec[f"r{h}"] = (c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                    rec[f"tot{h}"] = (c.iloc[i + h] / c.iloc[i] - 1) if i + h < n else np.nan
                rows.append(rec)
    A = pd.DataFrame(rows)
    out = {}
    # step-5-like cases (first per 5-bar grid cell), short direction
    C = A[A.case].copy()
    C["cell"] = C.i // 5
    C = C.groupby(["coin", "w", "cell"]).head(1)
    def summ(g, col="r5", sign=-1):
        x = sign * g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["cases_all"] = summ(C)
    C["fb"] = pd.cut(C.f, [-20.01, -19.99, -10, -5, -2.0001], labels=["-20", "-20..-10", "-10..-5", "-5..-2"])
    out["cases_by_fbucket"] = C.groupby("fb").apply(summ)
    C["zb"] = pd.cut(C.z, [-np.inf, 1, 1.5, 2, 3, np.inf])
    out["cases_by_z"] = C.groupby("zb").apply(summ)
    hz = {}
    for h in H:
        hz[h] = summ(C, f"r{h}")
    out["cases_by_horizon"] = pd.DataFrame(hz).T
    out["cases_by_coin"] = C.groupby("coin").apply(summ)
    out["cases_by_year"] = C.groupby("year").apply(summ)
    C["d90"] = pd.qcut(C.ret90, 4)
    out["cases_by_ret90_quartile"] = C.groupby("d90").apply(summ)
    # generic event study: rises by z, falling vs not, deduped per 5-bar cell
    E = A[A.z > 0].copy()
    E["zb"] = pd.cut(E.z, [0, 0.5, 1, 1.5, 2, 3, np.inf])
    E["cell"] = E.i // 5
    E = E.groupby(["coin", "w", "cell", "zb", "falling"], observed=True).head(1)
    out["rises_z_by_regime_r5_shortdir"] = E.groupby(["falling", "zb"], observed=True).apply(summ)
    out["rises_z_by_regime_r1_shortdir"] = E.groupby(["falling", "zb"], observed=True).apply(lambda g: summ(g, "r1"))
    return out

def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 5, 10]
    rows = []
    for coin, ws in bars.items():
        drift = {}
        for h in H:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr) if rr else np.nan
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret = pd.Series(c).pct_change()
            sd = ret.rolling(20).std()
            z = (ret / sd).values
            fall = (df["regime"] == "mean_reversion").values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 5):
                rec = {"coin": coin, "w": w, "z": z[i], "falling": fall[i], "year": ts.iloc[i].year}
                for h in H:
                    rec[f"r{h}"] = (c[i + h] / c[i] - 1 - drift[h]) if i + h < n else np.nan
                rows.append(rec)
    A = pd.DataFrame(rows)
    def summ(g, col="r5", sign=-1):
        x = sign * g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    A["zb"] = pd.cut(A.z, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["grid_by_regime_z_r5_shortdir"] = A.groupby(["falling", "zb"], observed=True).apply(summ)
    out["grid_by_regime_r5_shortdir"] = A.groupby("falling").apply(summ)
    out["grid_by_regime_r10_shortdir"] = A.groupby("falling").apply(lambda g: summ(g, "r10"))
    out["grid_falling_by_year_r5"] = A[A.falling].groupby("year").apply(summ)
    out["grid_rising_by_year_r5"] = A[~A.falling].groupby("year").apply(summ)
    F = A[A.falling & (A.z > 0)].dropna(subset=["r5", "z"])
    out["falling_rises_corr_z_r5"] = float(np.corrcoef(F.z, -F.r5)[0, 1])
    F2 = A[A.falling].dropna(subset=["r5", "z"])
    out["falling_all_corr_z_r5"] = float(np.corrcoef(F2.z, -F2.r5)[0, 1])
    return out

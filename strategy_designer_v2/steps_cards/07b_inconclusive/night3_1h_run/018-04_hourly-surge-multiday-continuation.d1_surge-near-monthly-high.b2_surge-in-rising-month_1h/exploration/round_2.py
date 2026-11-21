def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 240
    rows = []
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rr.extend(list(c[idx + H] / c[idx] - 1))
        dr, sd = np.mean(rr), np.std(rr)
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values
            n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r2160 = np.full(n, np.nan); r2160[2160:] = c[2160:] / c[:-2160] - 1
            r720 = np.full(n, np.nan); r720[720:] = c[720:] / c[:-720] - 1
            # distance below the 30-day high
            hi720 = pd.Series(c).rolling(720, min_periods=720).max().values
            for start in range(0, n - H, H):
                seg = np.where(f[start:start + H] >= 2)[0]
                if len(seg) == 0:
                    continue
                t = start + seg[0]
                if t + H >= n:
                    continue
                rows.append({"coin": coin, "win": w, "year": yr[t], "fc": f[t],
                             "r2160": r2160[t], "r720": r720[t], "nearhi": c[t] / hi720[t] - 1,
                             "ex": c[t + H] / c[t] - 1 - dr,
                             "ex120": (c[t + 120] / c[t] - 1) if t + 120 < n else np.nan})
    R = pd.DataFrame(rows)
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    top = R[R.fc >= R.fc.quantile(0.75)]
    rest = R[R.fc < R.fc.quantile(0.75)]
    out["top_by_year"] = top.groupby("year").apply(summ)
    out["rest_by_year"] = rest.groupby("year").apply(summ)
    out["top_by_coin"] = top.groupby("coin").apply(summ)
    out["fc_eq20_vs_below"] = pd.DataFrame({"eq20": summ(R[R.fc >= 19.99]), "below": summ(R[R.fc < 19.99])}).T
    R2 = R.dropna(subset=["r2160"]).copy()
    R2["q90"] = pd.qcut(R2["r2160"].rank(method="first"), 4, labels=False)
    out["by_90d_return_q"] = R2.groupby("q90").apply(lambda g: pd.concat([summ(g), pd.Series({"mid": g.r2160.median()})]))
    out["by_90d_sign"] = R2.groupby(R2.r2160 > 0).apply(summ)
    out["top_by_90d_sign"] = R2[R2.fc >= R.fc.quantile(0.75)].groupby(R2.r2160 > 0).apply(summ)
    R3 = R.dropna(subset=["nearhi"]).copy()
    R3["qh"] = pd.qcut(R3["nearhi"].rank(method="first"), 4, labels=False)
    out["by_near_30d_high_q"] = R3.groupby("qh").apply(lambda g: pd.concat([summ(g), pd.Series({"mid": g.nearhi.median()})]))
    out["slope_ex_on_fc"] = pd.Series({"slope": np.polyfit(R.fc, R.ex, 1)[0],
                                       "corr": np.corrcoef(R.fc, R.ex)[0, 1], "n": len(R)})
    return out

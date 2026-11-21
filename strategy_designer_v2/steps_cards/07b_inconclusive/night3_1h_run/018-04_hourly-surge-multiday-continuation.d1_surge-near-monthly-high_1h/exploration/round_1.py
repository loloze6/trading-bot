def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [24, 72, 120, 240]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, b in ws.items():
            c = b["close"].values.astype(float)
            f = b["forecast"].fillna(0).values.astype(float)
            raw = b["debug_info.components.surge_near_high.last_history_value"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            hi = pd.Series(c).rolling(720, min_periods=24).max().values
            prox = c / hi
            r720 = pd.Series(c).pct_change(720).values
            r24 = pd.Series(c).pct_change(24).values
            trough = 0.0; taken = set()
            for i in range(len(c)):
                fi = max(f[i], 0)
                if fi < trough: trough = fi
                if fi - trough >= 2:
                    trough = fi
                    cell = i // 120
                    if cell in taken: continue
                    taken.add(cell)
                    d = dict(coin=coin, win=w, year=ts.iloc[i].year, fc=f[i], raw=raw[i],
                             prox=prox[i], r720=r720[i], r24=r24[i])
                    for h in H:
                        d[f"u{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < len(c) else np.nan
                    rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"n{h}"] = len(x)
            out[f"m{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["all"] = summ(df).to_frame().T
    res["by_coin"] = df.groupby("coin").apply(summ)
    res["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["fc"].rank(method="first"), 5, labels=False)
    res["by_forecast_quintile"] = df.groupby("fq").apply(summ)
    df["pq"] = pd.qcut(df["prox"].rank(method="first"), 5, labels=False)
    res["by_proximity_quintile"] = df.groupby("pq").apply(summ)
    df["tq"] = pd.qcut(df["r720"].rank(method="first"), 5, labels=False)
    res["by_30d_return_quintile"] = df.groupby("tq").apply(summ)
    res["quintile_edges"] = pd.DataFrame({
        "fc": df.groupby("fq")["fc"].median(), "prox": df.groupby("pq")["prox"].median(),
        "r720": df.groupby("tq")["r720"].median()})
    return res

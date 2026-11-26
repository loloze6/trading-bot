def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    # normal drift per coin per horizon, non-overlapping grid
    H = [1, 3, 5, 10]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values; op = df["open"].values
            rng = pd.Series(hi - lo)
            rm = (rng / rng.rolling(20).mean()).values
            r5 = pd.Series(cl).pct_change(5).values
            r60 = pd.Series(cl).pct_change(60).values
            body = np.abs(cl - op) / np.where(hi - lo > 0, hi - lo, np.nan)
            n = len(df); low = 0.0; cell_used = set()
            for t in range(n):
                if f[t] <= 0:
                    low = 0.0; continue
                low = min(low, f[t])
                if f[t] - low >= 2:
                    cell = t // 3
                    if cell not in cell_used:
                        cell_used.add(cell)
                        d = {"coin": c, "w": w, "t": t, "fc": f[t], "rm": rm[t], "r5": r5[t], "r60": r60[t],
                             "body": body[t], "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                             "day": pd.Timestamp(df["timestamp"].iloc[t]).floor("D")}
                        for h in H:
                            d[f"u{h}"] = (cl[t + h] / cl[t] - 1 - drift[(c, h)]) if t + h < n else np.nan
                        rows.append(d)
                    low = f[t]
    cs = pd.DataFrame(rows)
    def tpool(s, days):
        g = pd.DataFrame({"v": s - s.mean() + s.mean(), "d": days}).dropna()
        m = g["v"].mean()
        dev = (g["v"] - m).groupby(g["d"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g) if D > 1 else np.nan
        return m, m / se if se else np.nan, len(g), D
    def summ(sub):
        out = {}
        for h in H:
            m, t, n, D = tpool(sub[f"u{h}"], sub["day"])
            out[f"m{h}"] = m; out[f"t{h}"] = t
        out["n"] = len(sub)
        return pd.Series(out)
    res = {}
    res["all"] = summ(cs).to_frame().T
    res["by_coin"] = cs.groupby("coin").apply(summ)
    res["by_year"] = cs.groupby("year").apply(summ)
    cs["fq"] = pd.qcut(cs["fc"].rank(method="first"), 4, labels=False)
    res["by_fc_quart"] = cs.groupby("fq").apply(summ)
    cs["rmq"] = pd.qcut(cs["rm"], 4, labels=False)
    res["by_rangemult_quart"] = cs.groupby("rmq").apply(summ)
    cs["r5q"] = pd.qcut(cs["r5"], 4, labels=False)
    res["by_r5_quart"] = cs.groupby("r5q").apply(summ)
    cs["r60q"] = pd.qcut(cs["r60"], 4, labels=False)
    res["by_r60_quart"] = cs.groupby("r60q").apply(summ)
    cs["bq"] = pd.qcut(cs["body"], 3, labels=False)
    res["by_body_terc"] = cs.groupby("bq").apply(summ)
    res["quart_edges"] = pd.DataFrame({"rm": cs["rm"].quantile([.25,.5,.75]).values, "r5": cs["r5"].quantile([.25,.5,.75]).values,
                                       "r60": cs["r60"].quantile([.25,.5,.75]).values, "body": cs["body"].quantile([1/3,2/3]).values.tolist()+[np.nan]})
    return res

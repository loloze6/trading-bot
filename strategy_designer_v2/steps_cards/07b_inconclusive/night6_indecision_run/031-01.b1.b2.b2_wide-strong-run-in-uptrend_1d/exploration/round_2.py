def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [3, 5, 10]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = pd.Series(hi - lo)
            rm = (rng / rng.rolling(20).mean()).values
            r5 = pd.Series(cl).pct_change(5).values
            n = len(df); low = 0.0; used = set()
            for t in range(n):
                if f[t] <= 0:
                    low = 0.0; continue
                low = min(low, f[t])
                if f[t] - low >= 2:
                    if t // 3 not in used:
                        used.add(t // 3)
                        d = {"coin": c, "fc": f[t], "rm": rm[t], "r5": r5[t],
                             "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                             "day": pd.Timestamp(df["timestamp"].iloc[t]).floor("D")}
                        for h in H:
                            d[f"u{h}"] = (cl[t + h] / cl[t] - 1 - drift[(c, h)]) if t + h < n else np.nan
                        rows.append(d)
                    low = f[t]
    cs = pd.DataFrame(rows)
    def tpool(s, days):
        g = pd.DataFrame({"v": s, "d": days}).dropna()
        m = g["v"].mean()
        dev = (g["v"] - m).groupby(g["d"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g) if D > 1 else np.nan
        return m, m / se, len(g), D
    def summ(sub):
        out = {}
        for h in H:
            m, t, n, D = tpool(sub[f"u{h}"], sub["day"])
            out[f"m{h}"] = m; out[f"t{h}"] = t
        out["n"] = len(sub); out["days"] = sub["day"].nunique()
        return pd.Series(out)
    res = {}
    med = cs["fc"].median()
    top = cs[cs["fc"] > med]
    res["top_half_fc"] = summ(top).to_frame().T
    res["top_half_by_coin"] = top.groupby("coin").apply(summ)
    res["top_half_by_year"] = top.groupby("year").apply(summ)
    res["all_exZEC"] = summ(cs[cs["coin"] != "ZECUSD"]).to_frame().T
    res["top_half_exZEC"] = summ(top[top["coin"] != "ZECUSD"]).to_frame().T
    cs["fq"] = pd.qcut(cs["fc"].rank(method="first"), 4, labels=False)
    from scipy import stats
    res["spearman_fc_u"] = pd.DataFrame({h: [stats.spearmanr(cs["fc"], cs[f"u{h}"], nan_policy="omit")[0]] for h in H})
    res["r5_x_rm_u10"] = cs.assign(a=pd.qcut(cs["r5"], 2, labels=False), b=pd.qcut(cs["rm"], 2, labels=False)).groupby(["a", "b"])["u10"].agg(["mean", "count"])
    return res

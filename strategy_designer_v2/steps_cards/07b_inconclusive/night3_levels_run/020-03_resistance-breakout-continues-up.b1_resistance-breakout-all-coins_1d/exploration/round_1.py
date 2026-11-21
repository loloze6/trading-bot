def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [1, 5, 10, 20]
    for coin, wd in bars.items():
        # drift per horizon on grid
        drift = {}
        for h in hs:
            rr = []
            for w, df in wd.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[h] = (np.mean(rr), np.std(rr))
        for w, df in wd.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.break_touches.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            n = len(c)
            ret30 = pd.Series(c).pct_change(30).values
            seen = set()
            for t in range(n):
                prev = f[t - 1] if t > 0 else 0
                if f[t] >= 2 and prev < 2:
                    cell = t // 5
                    if cell in seen:
                        continue
                    seen.add(cell)
                    r = {"coin": coin, "w": w, "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                         "fc": f[t], "raw": raw[t], "ret30": ret30[t]}
                    for h in hs:
                        if t + h < n:
                            r[f"u{h}"] = c[t + h] / c[t] - 1 - drift[h][0]
                            r[f"s{h}"] = (c[t + h] / c[t] - 1 - drift[h][0]) / drift[h][1]
                        else:
                            r[f"u{h}"] = np.nan; r[f"s{h}"] = np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(d, f"u{h}") for h in hs}).T
    out["strength_by_h"] = d[[f"s{h}" for h in hs]].mean()
    out["fc_dist"] = d["fc"].describe()
    out["fc_share_at_cap"] = float((d["fc"] >= 19.99).mean())
    out["raw_dist"] = d["raw"].describe()
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fcq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=False)
    out["by_fc_quart"] = d.groupby("fcq").apply(summ)
    d["rawq"] = pd.qcut(d["raw"].rank(method="first"), 4, labels=False)
    out["by_raw_quart"] = d.groupby("rawq").apply(summ)
    d["trq"] = pd.qcut(d["ret30"].rank(method="first"), 4, labels=False)
    out["by_ret30_quart"] = d.groupby("trq").apply(summ)
    out["by_ret30_quart_u10"] = d.groupby("trq").apply(lambda g: summ(g, "u10"))
    return out

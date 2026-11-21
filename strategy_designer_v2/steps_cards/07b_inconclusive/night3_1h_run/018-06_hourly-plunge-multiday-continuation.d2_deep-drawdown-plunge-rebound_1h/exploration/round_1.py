def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (24, 72, 168)}
        for w, df in wins.items():
            c = df["close"].values
            for h in (24, 72, 168):
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        for h in allr:
            drift[(coin, h)] = np.mean(allr[h]); usual[(coin, h)] = np.std(allr[h])
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(c)
            hi = pd.Series(c).rolling(720, min_periods=720).max().values
            depth = (c - hi) / hi * 100
            r24 = np.full(n, np.nan); r24[24:] = c[24:] / c[:-24] - 1
            r720 = np.full(n, np.nan); r720[720:] = c[720:] / c[:-720] - 1
            lowest = 0.0; lastcell = -1
            for t in range(n):
                lowest = min(lowest, f[t])
                if f[t] - lowest >= 2:
                    cell = t // 72
                    if cell != lastcell:
                        lastcell = cell
                        rec = {"coin": coin, "win": w, "f": f[t], "depth": depth[t],
                               "r24": r24[t], "r720": r720[t], "year": df["timestamp"].iloc[t].year if hasattr(df["timestamp"].iloc[t], "year") else pd.Timestamp(df["timestamp"].iloc[t]).year}
                        for h in (24, 72, 168):
                            if t + h < n:
                                rec["u%d" % h] = c[t + h] / c[t] - 1 - drift[(coin, h)]
                                rec["s%d" % h] = rec["u%d" % h] / usual[(coin, h)]
                        rows.append(rec)
                    lowest = f[t]
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["u72"].dropna()
        return pd.Series({"n": len(x), "mean72": x.mean(), "t72": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean24": g["u24"].mean(), "mean168": g["u168"].mean(),
                          "t168": g["u168"].mean() / (g["u168"].std() / np.sqrt(g["u168"].notna().sum()))})
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=False)
    out["by_forecast_q"] = d.groupby("fq").apply(summ)
    d["dq"] = pd.qcut(d["depth"], 4, labels=False)
    out["by_depth_q"] = d.groupby("dq").apply(summ)
    d["tq"] = pd.qcut(d["r720"], 4, labels=False)
    out["by_30d_return_q"] = d.groupby("tq").apply(summ)
    d["rq"] = pd.qcut(d["r24"], 4, labels=False)
    out["by_24h_ret_q"] = d.groupby("rq").apply(summ)
    out["spearman_f_u72"] = stats.spearmanr(d["f"], d["u72"], nan_policy="omit")[0]
    out["spearman_r24_u72"] = stats.spearmanr(d["r24"], d["u72"], nan_policy="omit")[0]
    out["depth_q_ranges"] = d.groupby("dq")["depth"].agg(["min", "max"])
    return out

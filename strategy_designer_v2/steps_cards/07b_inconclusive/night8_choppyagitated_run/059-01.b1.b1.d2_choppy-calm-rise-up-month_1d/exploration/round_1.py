def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in (7, 14, 21, 28):
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for g in range(0, n, 14):
                idx = [i for i in range(g, min(g + 14, n)) if f[i] >= 2]
                if not idx:
                    continue
                i = idx[0]
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "fc": f[i], "day": ts.iloc[i].normalize()}
                for h in (7, 14, 21, 28):
                    r[f"u{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                    r[f"t{h}"] = (c[i + h] / c[i] - 1) if i + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u14"):
        x = g[col].dropna()
        if len(x) < 3:
            return pd.Series({"n": len(x), "mean": x.mean(), "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in (7, 14, 21, 28)}).T
    out["total_by_horizon"] = pd.DataFrame({h: summ(d, f"t{h}") for h in (7, 14, 21, 28)}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    d["fq"] = pd.qcut(d["fc"], 3, labels=["low", "mid", "high"])
    out["by_fc_tercile_u14"] = d.groupby("fq").apply(summ)
    out["by_fc_tercile_u7"] = d.groupby("fq").apply(lambda g: summ(g, "u7"))
    out["by_fc_tercile_u28"] = d.groupby("fq").apply(lambda g: summ(g, "u28"))
    x = d.dropna(subset=["u14"])
    out["corr_fc_u14"] = pd.Series(stats.spearmanr(x["fc"], x["u14"]), index=["rho", "p"])
    # median vs mean: outliers
    out["u14_median_share_pos"] = pd.Series({"median": x["u14"].median(), "share_pos": (x["u14"] > 0).mean(),
                                             "mean_trim5": stats.trim_mean(x["u14"], 0.05)})
    return out

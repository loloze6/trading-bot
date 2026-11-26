def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 5, 10, 20]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            fc = df["forecast"].fillna(0).values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for s in range(0, n, 10):
                for i in range(s, min(s + 10, n)):
                    prev = fc[i - 1] if i > 0 else 0.0
                    if fc[i] - prev >= 2 and fc[i] > 0:
                        r = {"coin": c, "win": w, "year": yr[i], "dayidx": str(df["timestamp"].iloc[i])[:10],
                             "gain": cl[i] / cl[i - 1] - 1 if i > 0 else np.nan, "fc": fc[i]}
                        # 20-day prior return and range position
                        r["ret20"] = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                        for h in H:
                            r["u%d" % h] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                        rows.append(r)
                        break
    d = pd.DataFrame(rows)
    def summ(g, col="u10"):
        x = g[col].dropna()
        if len(x) < 2:
            return pd.Series({"n": len(x), "mean": x.mean() if len(x) else np.nan, "t": np.nan, "hit": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), "hit": (x > 0).mean()})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: summ(d, "u%d" % h) for h in H}).T
    d["gain_q"] = pd.qcut(d["gain"], 3, labels=["low", "mid", "high"])
    out["by_gain_tercile_u10"] = d.groupby("gain_q").apply(summ)
    out["by_gain_tercile_u5"] = d.groupby("gain_q").apply(lambda g: summ(g, "u5"))
    out["by_gain_tercile_u20"] = d.groupby("gain_q").apply(lambda g: summ(g, "u20"))
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    d["r20_q"] = pd.qcut(d["ret20"], 3, labels=["low", "mid", "high"])
    out["by_ret20_tercile"] = d.groupby("r20_q").apply(summ)
    dd = d.dropna(subset=["gain", "u10"])
    out["spearman_gain_u10"] = str(stats.spearmanr(dd["gain"], dd["u10"]))
    dd = d.dropna(subset=["gain", "u20"])
    out["spearman_gain_u20"] = str(stats.spearmanr(dd["gain"], dd["u20"]))
    out["gain_tercile_edges"] = d["gain"].quantile([0, 1/3, 2/3, 1]).to_frame()
    return out

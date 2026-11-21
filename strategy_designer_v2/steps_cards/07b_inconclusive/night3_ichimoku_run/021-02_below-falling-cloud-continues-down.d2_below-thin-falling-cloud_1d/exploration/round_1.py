def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 26
    # drift per coin for several horizons
    hs = [5, 10, 26, 40]
    drift = {}; usual = {}
    for c in bars:
        for h in hs:
            r = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    r.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(r); usual[(c, h)] = np.std(r)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            cl = df["close"].values; fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            # trailing 26-day coin return as a regime
            for i in range(0, n - H, H):
                if not (fc[i] < 0):
                    continue
                rec = {"coin": c, "win": w, "year": yr[i], "absf": abs(fc[i]),
                       "past26": cl[i] / cl[i - 26] - 1 if i >= 26 else np.nan}
                for h in hs:
                    if i + h < n:
                        rr = cl[i + h] / cl[i] - 1
                        rec[f"ex{h}"] = -(rr - drift[(c, h)])
                        rec[f"tot{h}"] = -rr
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="ex26"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_pos": (x > 0).mean()})
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["absf"], 4, labels=False, duplicates="drop")
    out["by_thin_quartile"] = d.groupby("fq").apply(summ)
    out["by_horizon"] = pd.DataFrame({h: summ(d, f"ex{h}") for h in hs}).T
    out["by_horizon_total"] = pd.DataFrame({h: summ(d, f"tot{h}") for h in hs}).T
    d["pq"] = pd.qcut(d["past26"], 3, labels=False, duplicates="drop")
    out["by_past26_tercile"] = d.groupby("pq").apply(summ)
    out["past26_tercile_means"] = d.groupby("pq")["past26"].mean()
    out["drift26"] = pd.Series({c: drift[(c, 26)] for c in bars})
    out["usual26"] = pd.Series({c: usual[(c, 26)] for c in bars})
    out["trimmed"] = pd.Series({"mean_clip_1_99": d["ex26"].clip(d["ex26"].quantile(.01), d["ex26"].quantile(.99)).mean(),
                                "std": d["ex26"].std(), "skew": d["ex26"].skew()})
    return out

def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 30
    # coin drift over horizon on non-overlapping grid, per horizon
    hs = [5, 10, 20, 30, 45]
    drift = {}
    usual = {}
    for c in bars:
        for h in hs:
            r = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    r.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(r) if r else np.nan
            usual[(c, h)] = np.std(r, ddof=1) if len(r) > 1 else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            cl = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            depth = df.get("debug_info.components.depth.last_history_value")
            low = 0.0
            taken = set()
            n = len(df)
            for i in range(n):
                low = min(low, f[i])
                if f[i] - low >= 2:
                    cell = i // H
                    low = f[i]
                    if cell in taken:
                        continue
                    taken.add(cell)
                    rec = {"coin": c, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                           "fc": f[i], "depth": (depth.iloc[i] if depth is not None else np.nan),
                           "pos": i}
                    for h in hs:
                        rec[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                        rec[f"s{h}"] = rec[f"u{h}"] / usual[(c, h)] if i + h < n else np.nan
                    rec["past10"] = cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan
                    rec["past30"] = cl[i] / cl[i - 30] - 1 if i >= 30 else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)

    def tday(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3:
            return pd.Series({"n": len(x), "mean": x[col].mean(), "t": np.nan, "days": x["day"].nunique()})
        m = x[col].mean()
        g = (x[col] - m).groupby(x["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t": m / se, "days": G})

    out = {}
    out["horizons"] = pd.DataFrame({f"u{h}": tday(d, f"u{h}") for h in hs}).T
    out["by_coin_u30"] = d.groupby("coin").apply(lambda x: tday(x, "u30"))
    out["by_year_u30"] = d.groupby("year").apply(lambda x: tday(x, "u30"))
    d["fcq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_fc_tercile"] = d.groupby("fcq").apply(lambda x: pd.concat([tday(x, "u30"), pd.Series({"fc_mean": x["fc"].mean(), "u10": x["u10"].mean(), "s30": x["s30"].mean()})]))
    d["p10q"] = pd.qcut(d["past10"], 3, labels=["fell_most", "mid", "rose"])
    out["by_past10"] = d.groupby("p10q").apply(lambda x: pd.concat([tday(x, "u30"), pd.Series({"past10": x["past10"].mean()})]))
    d["p30q"] = pd.qcut(d["past30"], 3, labels=["fell_most", "mid", "rose"])
    out["by_past30"] = d.groupby("p30q").apply(lambda x: pd.concat([tday(x, "u30"), pd.Series({"past30": x["past30"].mean()})]))
    out["corr_fc_u30_spearman"] = float(d[["fc", "u30"]].dropna().corr("spearman").iloc[0, 1])
    out["median_u30"] = float(d["u30"].median())
    out["share_pos_u30"] = float((d["u30"].dropna() > 0).mean())
    out["u30_trim_mean_10pct"] = float(pd.Series(d["u30"].dropna()).clip(*d["u30"].quantile([.05, .95])).mean())
    return out

def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std(ddof=1)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "fc": b["regime"].astype(str) != "chop",
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["z1"] = r / sd
            df["z5"] = (c / c.shift(5) - 1) / (sd * np.sqrt(5))
            df["tr60"] = c / c.shift(60) - 1
            df["clv"] = (c - lo) / (hi - lo).replace(0, np.nan)
            df["dd20"] = c / c.rolling(20).max() - 1
            for h in (1, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["f1"].mean()
    res = {}
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    for h in (1, 3, 5):
        d[f"u{h}"] = d[f"f{h}"] - h * d["coin"].map(drift)
    fc = d[d["fc"]]
    summ = []
    for h in (1, 3, 5):
        g = fc[fc["pos"] % h == 0]
        summ.append({"h": h, "n": g[f"u{h}"].count(), "mean_u": g[f"u{h}"].mean(), "t_u": tt(g[f"u{h}"]),
                     "mean_total": g[f"f{h}"].mean(), "t_total": tt(g[f"f{h}"])})
    res["fc forward unusual, grid"] = pd.DataFrame(summ)
    out = []
    for feat in ("z1", "z5", "tr60", "clv", "dd20"):
        for h in (1, 3, 5):
            g = fc[fc["pos"] % h == 0][[feat, f"u{h}"]].dropna()
            if len(g) < 20: continue
            q = pd.qcut(g[feat], 3, labels=False, duplicates="drop")
            m = g.groupby(q)[f"u{h}"].mean()
            out.append({"feat": feat, "h": h, "n": len(g),
                        "spearman": g.corr("spearman").iloc[0, 1],
                        "low3": m.iloc[0], "mid3": m.iloc[1] if len(m) > 2 else np.nan, "high3": m.iloc[-1],
                        "t_high_minus_low": (m.iloc[-1] - m.iloc[0]) / np.sqrt(
                            g[f"u{h}"][q == q.max()].var() / (q == q.max()).sum() + g[f"u{h}"][q == q.min()].var() / (q == q.min()).sum())})
    res["fc feature terciles (unusual, long dir)"] = pd.DataFrame(out)
    g5 = fc[fc["pos"] % 5 == 0]
    res["fc u5 by coin"] = g5.groupby("coin")["u5"].agg(["count", "mean", tt])
    res["fc u5 by year"] = g5.groupby("year")["u5"].agg(["count", "mean"])
    res["fc u5 by window"] = g5.groupby("win")["u5"].agg(["count", "mean"])
    g3 = fc[fc["pos"] % 3 == 0]
    res["fc u3 by z5 sign"] = g3.groupby(np.sign(g3["z5"]))["u3"].agg(["count", "mean", tt])
    return res

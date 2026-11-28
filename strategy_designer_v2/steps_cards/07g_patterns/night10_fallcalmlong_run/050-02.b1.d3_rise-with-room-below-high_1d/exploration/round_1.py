def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "inprof": (b["regime"] != "chop").astype(int),
                "regime": b["regime"],
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "r1": r1,
                "s7": c.pct_change(7) / (vol20 * np.sqrt(7)),
                "s3": c.pct_change(3) / (vol20 * np.sqrt(3)),
                "d30": c / c.rolling(30).max() - 1,
                "dlow30": c / c.rolling(30).min() - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c / vol20,
                "vrel": b["volume"] / b["volume"].rolling(20).mean(),
                "vol20": vol20,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            for h in (3, 7):
                f[f"fwd{h}"] = c.shift(-h) / c - 1
            f["g7"] = (f["pos"] % 7 == 0)
            f["g3"] = (f["pos"] % 3 == 0)
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    out["profile share by coin"] = df.groupby("coin")["inprof"].mean()
    m7 = df.loc[df.g7, "fwd7"].mean(); m3 = df.loc[df.g3, "fwd3"].mean()
    out["drift 7d / 3d all"] = f"{m7:.4f} / {m3:.4f}"
    P7 = df[df.g7 & (df.inprof == 1)].dropna(subset=["fwd7"]).copy()
    P3 = df[df.g3 & (df.inprof == 1)].dropna(subset=["fwd3"]).copy()
    P7["u"] = P7.fwd7 - m7; P3["u"] = P3.fwd3 - m3
    def tab(P, col, q=5):
        d = P.dropna(subset=[col]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("b")
        t = g["u"].agg(["count", "mean"])
        t["t"] = g["u"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
        t["xmean"] = g[col].mean()
        rho = stats.spearmanr(d[col], d["u"])
        t.loc["spearman", "mean"] = rho.correlation; t.loc["spearman", "t"] = rho.pvalue
        return t
    out["in-profile all 7d u: n,mean,t"] = f"{len(P7)}, {P7.u.mean():.4f}, {P7.u.mean()/(P7.u.std()/np.sqrt(len(P7))):.2f}"
    for col in ["s7", "s3", "d30", "dlow30", "r1", "clv", "rng", "vrel", "vol20"]:
        out[f"7d u by {col}"] = tab(P7, col)
    for col in ["s3", "r1", "clv", "rng", "vrel"]:
        out[f"3d u by {col}"] = tab(P3, col)
    out["7d u by weekday"] = P7.groupby("wd")["u"].agg(["count", "mean"])
    out["7d u by regime"] = P7.groupby("regime")["u"].agg(["count", "mean"])
    out["7d u by coin"] = P7.groupby("coin")["u"].agg(["count", "mean"])
    return out

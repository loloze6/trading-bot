def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    # coin mean h-bar returns over all windows (non-overlapping grid)
    hs = [1, 3, 5, 10]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in hs:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            sma = c.rolling(20).mean()
            sd = c.pct_change().rolling(20).std()
            stretch = (c - sma) / sma / sd
            fc = df["forecast"]
            raw = df.get("debug_info.components.stretch.last_history_value")
            n = len(df)
            for i in range(0, n - 5, 5):
                rec = {"coin": coin, "win": w, "fc": fc.iloc[i], "stretch": stretch.iloc[i],
                       "regime": df["regime"].iloc[i],
                       "raw": raw.iloc[i] if raw is not None else np.nan,
                       "yr": pd.Timestamp(df["timestamp"].iloc[i]).year}
                for h in hs:
                    if i + h < n:
                        rec[f"ex{h}"] = c.iloc[i + h] / c.iloc[i] - 1 - drift[h]
                rows.append(rec)
    d = pd.DataFrame(rows)
    ch = d[d["regime"] == "unknown"]
    neg = ch[ch["fc"] < 0].copy()
    out = {}
    out["n_choppy_grid, n_neg"] = f"{len(ch)}, {len(neg)}"
    def summ(g):
        x = g["ex5"].dropna()
        return pd.Series({"n": len(x), "mean_ex5": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean_ex1": g["ex1"].mean(), "mean_ex3": g["ex3"].mean(), "mean_ex10": g["ex10"].mean()})
    neg["fcb"] = pd.cut(neg["fc"], [-20.1, -15, -10, -5, -2, 0])
    out["neg by forecast bucket"] = neg.groupby("fcb").apply(summ)
    ch = ch.copy()
    ch["sb"] = pd.qcut(ch["stretch"], 6)
    out["all choppy by raw stretch sextile"] = ch.groupby("sb").apply(summ)
    out["neg by coin"] = neg.groupby("coin").apply(summ)
    out["neg by year"] = neg.groupby("yr").apply(summ)
    out["all choppy by coin"] = ch.groupby("coin").apply(summ)
    # correlations stretch vs ex returns (choppy, all)
    cr = {}
    for h in hs:
        s = ch[["stretch", f"ex{h}"]].dropna()
        r = s.corr().iloc[0, 1]; n = len(s)
        cr[f"h{h}"] = f"r={r:.3f}, n={n}, t={r*np.sqrt(n-2)/np.sqrt(1-r*r):.2f}"
    out["choppy stretch vs excess corr"] = pd.Series(cr)
    # non-choppy for comparison
    nc = d[d["regime"] != "unknown"].copy()
    nc["sb"] = pd.qcut(nc["stretch"], 6)
    out["non-choppy by stretch sextile"] = nc.groupby("sb").apply(summ)
    return out

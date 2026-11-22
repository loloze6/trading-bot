def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            H = c.rolling(30).max(); L = c.rolling(30).min()
            pos = (c - L) / (H - L)
            d = 2 * pos - 1
            flat = 1 - (c - c.shift(30)).abs() / (H - L)
            past30 = c / c.shift(30) - 1
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            for h in (5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    rows.append(dict(coin=coin, w=w, wn=int(w[1:]), h=h, d=d.iloc[i], flat=flat.iloc[i],
                                     p30=past30.iloc[i], p30z=past30.iloc[i] / (vol30.iloc[i] * np.sqrt(30)) if vol30.iloc[i] > 0 else np.nan,
                                     fwd=fwd.iloc[i], yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows).dropna(subset=["fwd", "d", "flat", "p30"])
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    def slope(g, xcol):
        g = g.dropna(subset=[xcol])
        if len(g) < 20: return pd.Series({"n": len(g), "corr": np.nan, "t": np.nan})
        r = stats.linregress(g[xcol], g["ex"])
        return pd.Series({"n": len(g), "corr": r.rvalue, "t": r.slope / r.stderr})
    for h in (5, 10):
        s = df[df.h == h]
        out[f"h{h} pooled slopes"] = pd.DataFrame({k: slope(s, k) for k in ["d", "p30", "p30z"]}).T
        out[f"h{h} d slope by coin"] = s.groupby("coin").apply(lambda g: slope(g, "d"))
        out[f"h{h} d slope by year"] = s.groupby("yr").apply(lambda g: slope(g, "d"))
        s2 = s.copy(); s2["blk"] = pd.cut(s2["wn"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
        out[f"h{h} d slope by window block"] = s2.groupby("blk").apply(lambda g: slope(g, "d"))
        s2["fh"] = pd.qcut(s2["flat"], 3, labels=["trendy", "mid", "flat"])
        out[f"h{h} d slope by flatness tercile"] = s2.groupby("fh").apply(lambda g: slope(g, "d"))
        loyo = {}
        for y in sorted(s["yr"].unique()):
            loyo[y] = slope(s[s.yr != y], "d")
        out[f"h{h} d slope leave-one-year-out"] = pd.DataFrame(loyo).T
    return out

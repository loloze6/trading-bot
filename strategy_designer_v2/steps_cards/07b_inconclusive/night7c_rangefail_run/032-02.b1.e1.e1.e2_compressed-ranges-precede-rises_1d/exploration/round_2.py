def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change().abs()
            hi = c.shift(1).rolling(60).max(); lo = c.shift(1).rolling(60).min()
            mad = r1.rolling(60).mean()
            W = (hi - lo) / c / mad
            pos = (c - (hi + lo) / 2) / (hi - lo)
            brk = np.where(c > hi, (c - hi) / c / mad, np.where(c < lo, (c - lo) / c / mad, 0.0))
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (10, 20):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], W=W.iloc[i], pos=pos.iloc[i],
                                     brk=brk[i], fwd=fwd.iloc[i], fc=b["forecast"].iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    d = d.dropna(subset=["W", "pos", "ex"])
    d["cp"] = d["pos"] / d["W"]
    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series({"n": len(g), "corr": np.nan, "t": np.nan})
        r, p = stats.pearsonr(g[x], g["ex"])
        t = r * np.sqrt((len(g) - 2) / (1 - r * r))
        return pd.Series({"n": len(g), "corr": r, "t": t})
    out = {}
    for h in (10, 20):
        g = d[d.h == h].copy()
        out[f"h{h}_cp_by_year"] = g.groupby("year").apply(lambda x: slope(x, "cp"))
        out[f"h{h}_cp_by_coin"] = g.groupby("coin").apply(lambda x: slope(x, "cp"))
        g["side"] = np.where(g["pos"] > 0, "upper", "lower")
        out[f"h{h}_pos_by_side"] = g.groupby("side").apply(lambda x: slope(x, "pos"))
        g["q"] = pd.qcut(g["cp"], 5, labels=False, duplicates="drop")
        out[f"h{h}_cp_quint"] = g.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"), cp=("cp", "mean"))
        b2 = g[g["brk"] != 0]
        out[f"h{h}_breaks"] = pd.DataFrame({"n": [len(b2)], "share_up": [(b2.brk > 0).mean()],
            "mean_signed_ex": [(np.sign(b2.brk) * b2.ex).mean()],
            "t_signed_ex": [stats.ttest_1samp(np.sign(b2.brk) * b2.ex, 0).statistic if len(b2) > 2 else np.nan]})
        out[f"h{h}_fc_vs_cp_corr"] = float(g[["fc", "cp"]].corr().iloc[0, 1])
    return out

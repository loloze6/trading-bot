import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    hs = [7, 14, 21]
    drift = {}
    for coin, wins in bars.items():
        for h in hs:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(vals) if vals else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values; reg = df["regime"].values
            n = len(c)
            r = pd.Series(c).pct_change()
            sd = r.rolling(30).std().values
            r14 = pd.Series(c).pct_change(14).values
            vs = r14 / (sd * np.sqrt(14))
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in hs:
                for i in range(0, n - h, h):
                    if reg[i] != "unknown" or not np.isfinite(vs[i]) or vs[i] == 0:
                        continue
                    rows.append({"h": h, "coin": coin, "w": w, "year": yr[i], "day": day[i],
                                 "vs": vs[i], "f": f[i],
                                 "u": np.sign(vs[i]) * (c[i + h] / c[i] - 1 - drift[(coin, h)])})
    t = pd.DataFrame(rows)
    t["avs"] = t["vs"].abs()
    t["side"] = np.where(t["vs"] > 0, "long", "short")

    def ct(g, wcol=None):
        x = g["u"].values
        wts = g[wcol].values if wcol else np.ones(len(x))
        m = (x * wts).sum() / wts.sum()
        dev = pd.Series(wts * (x - m)).groupby(g["day"].values).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / wts.sum()
        return pd.Series({"n": len(x), "days": D, "mean": m, "t_day": m / se if se > 0 else np.nan})

    res = {}
    res["raw_vs_all_by_h"] = t.groupby("h").apply(ct)
    res["raw_vs_weighted_by_h"] = t.groupby("h").apply(lambda g: ct(g, "avs"))
    t["q"] = t.groupby("h")["avs"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res["by_h_tercile_avs"] = t.groupby(["h", "q"]).apply(ct)
    res["tercile_ranges_avs"] = t[t.h == 7].groupby("q")["avs"].agg(["min", "max"])
    res["by_h_side_top_tercile"] = t[t.q == 2].groupby(["h", "side"]).apply(ct)
    res["by_h_side"] = t.groupby(["h", "side"]).apply(ct)
    res["top_tercile_by_year_h14"] = t[(t.q == 2) & (t.h == 14)].groupby("year").apply(ct)
    res["weighted_by_year_h14"] = t[t.h == 14].groupby("year").apply(lambda g: ct(g, "avs"))
    res["weighted_by_window_h14"] = t[t.h == 14].groupby("w").apply(lambda g: ct(g, "avs"))
    return res

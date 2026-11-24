def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    total_days = 0
    for coin, wins in bars.items():
        r = {3: [], 5: []}
        for w, df in wins.items():
            c = df["close"].values
            for h in (3, 5):
                idx = np.arange(0, len(c) - h, h)
                r[h] += list(c[idx + h] / c[idx] - 1)
        dr = {h: np.mean(r[h]) for h in (3, 5)}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            total_days += len(df)
            o, h_, l, c = df["open"], df["high"], df["low"], df["close"]
            rng = (h_ - l).replace(0, np.nan)
            rr = rng.rolling(20).mean() / rng
            flat = 1 - (c - o).abs() / rng
            rise6 = c / c.shift(6) - 1
            ar = rise6.abs().rolling(60, min_periods=20).mean()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)), "rr": rr, "flat": flat,
                              "rise6": rise6, "zr": rise6 / ar, "day": ts.dt.floor("D"), "year": ts.dt.year})
            for hh in (3, 5):
                d[f"u{hh}"] = c.shift(-hh) / c - 1 - dr[hh]
            d["cell"] = d["pos"] // 3
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A["u3"].notna() & A["rr"].notna() & A["rise6"].notna()]

    def first(m):
        return A[m].sort_values(["coin", "win", "pos"]).groupby(["coin", "win", "cell"]).head(1)

    def tstat(s, col):
        dev = s[col] - s[col].mean()
        g = dev.groupby(s["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(s)
        return s[col].mean() / se, D

    out = {}
    up = A["rise6"] > 0
    base = first(up & (A["rr"] <= 0.6667) & (A["flat"] >= 0.7))
    out["broad_by_rise_quartile"] = base.groupby(pd.qcut(base["zr"], 4))["u3"].agg(["count", "mean"])
    out["broad_by_year"] = base.groupby("year")["u3"].agg(["count", "mean"])
    t5, D5 = tstat(base.dropna(subset=["u5"]), "u5")
    out["broad_h5"] = pd.Series({"mean_u5": base["u5"].mean(), "t": t5, "days": D5})
    # condition alone: wide flat days without up-run
    dn = first(~up & (A["rr"] <= 0.6667) & (A["flat"] >= 0.7))
    t, D = tstat(dn, "u3")
    out["wideflat_no_uprun"] = pd.Series({"n": len(dn), "mean": dn["u3"].mean(), "t": t})
    # broad case graded by width, slope
    s = base
    out["slope_u3_on_width"] = np.polyfit(1 / s["rr"], s["u3"], 1)[0]
    out["slope_u3_on_zr"] = np.polyfit(s["zr"].fillna(0), s["u3"], 1)[0]
    out["broad_per_coinday"] = len(base) / total_days
    return out

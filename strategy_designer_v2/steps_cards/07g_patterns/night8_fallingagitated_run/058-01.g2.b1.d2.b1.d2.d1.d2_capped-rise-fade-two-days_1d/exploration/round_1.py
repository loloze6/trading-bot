def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std().shift(0)
            out = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "inprof": (b["regime"] != "chop").astype(int),
                "s1": r1 / sd30,
                "s3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                "s5": (c / c.shift(5) - 1) / (sd30 * np.sqrt(5)),
                "range_s": ((b["high"] - b["low"]) / c.shift(1)) / sd30,
                "closepos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            for h in (1, 2, 5):
                out[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(out)
    D = pd.concat(rows, ignore_index=True)
    res = {}
    drift = {}
    for h in (1, 2, 5):
        g = D[D["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
        sdv = g.groupby("coin")[f"f{h}"].std()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(drift[h])
        D[f"z{h}"] = D[f"u{h}"] / D["coin"].map(sdv)
    res["profile share of bars"] = float(D["inprof"].mean())

    def tab(df, key, h, bins):
        g = df[(df["pos"] % h == 0)].dropna(subset=[key, f"u{h}"]).copy()
        g["bin"] = pd.cut(g[key], bins)
        out = []
        for bn, x in g.groupby("bin", observed=True):
            dd = x.groupby("day")[f"u{h}"].sum()
            m = x[f"u{h}"].mean()
            se = np.sqrt((dd - dd.index.map(x.groupby("day").size()) * m).pow(2).sum()) / len(x) if len(x) > 1 else np.nan
            out.append({"bin": str(bn), "n": len(x), "days": dd.size, "mean_u": m,
                        "t_day": m / se if se else np.nan, "mean_z": x[f"z{h}"].mean()})
        return pd.DataFrame(out)

    bins = [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf]
    P = D[D["inprof"] == 1]
    O = D[D["inprof"] == 0]
    res["in profile s1 -> u2"] = tab(P, "s1", 2, bins)
    res["in profile s3 -> u2"] = tab(P, "s3", 2, bins)
    res["in profile s5 -> u5"] = tab(P, "s5", 5, bins)
    res["in profile s1 -> u1"] = tab(P, "s1", 1, bins)
    res["out profile s1 -> u2"] = tab(O, "s1", 2, bins)
    res["out profile s3 -> u2"] = tab(O, "s3", 2, bins)
    res["in profile closepos -> u2"] = tab(P, "closepos", 2, [0, 0.2, 0.4, 0.6, 0.8, 1.0001])
    res["in profile range_s -> u2"] = tab(P, "range_s", 2, [0, 1, 2, 3, 4, np.inf])
    wdt = []
    for nm, df in (("in", P), ("out", O)):
        for wd, x in df.dropna(subset=["u1"]).groupby("wd"):
            wdt.append({"prof": nm, "wd": wd, "n": len(x), "mean_u1": x["u1"].mean(),
                        "t": stats.ttest_1samp(x["u1"], 0).statistic})
    res["weekday u1"] = pd.DataFrame(wdt)
    return res

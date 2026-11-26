def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        allr = {}
        for h in (5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            allr[h] = np.mean(rs) if rs else np.nan
        coin_means[coin] = allr
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ret28 = pd.Series(c).pct_change(28).values
            rng = ((df["high"] - df["low"]) / df["close"]).values
            rng28 = pd.Series(rng).rolling(28).mean().values
            rng120 = pd.Series(rng).rolling(120, min_periods=60).mean().values
            yr = pd.Timestamp(df["timestamp"].iloc[0]).year
            for i in range(0, len(c) - 10, 10):
                r = {"coin": coin, "win": w, "year": yr, "fc": df["forecast"].iloc[i],
                     "thin": df["regime"].iloc[i] == "trending",
                     "ret28": ret28[i], "rngrel": rng28[i] / rng120[i] if rng120[i] else np.nan,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date())}
                for h in (5, 10, 20):
                    if i + h < len(c):
                        r[f"x{h}"] = c[i + h] / c[i] - 1 - allr[h]
                    else:
                        r[f"x{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    def slope(sub, x, y):
        s = sub[[x, y]].dropna()
        if len(s) < 15: return pd.Series({"n": len(s)})
        lr = stats.linregress(s[x], s[y])
        return pd.Series({"n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr, "mean_y": s[y].mean()})
    cases = d[(d.thin) & (d.fc < 0)].copy()
    cases["neg_fc"] = -cases["fc"]  # deeper fall = larger
    # positive slope on neg_fc of -x means continuation; use short-side return
    for h in (5, 10, 20):
        cases[f"s{h}"] = -cases[f"x{h}"]
    out["cases_by_horizon"] = pd.DataFrame({h: slope(cases, "neg_fc", f"s{h}") for h in (5, 10, 20)}).T
    out["cases_raw28_slope"] = pd.DataFrame({h: slope(cases.assign(f=-cases.ret28), "f", f"s{h}") for h in (5, 10, 20)}).T
    out["by_coin"] = cases.groupby("coin").apply(lambda g: slope(g, "neg_fc", "s10"))
    out["by_year"] = cases.groupby("year").apply(lambda g: slope(g, "neg_fc", "s10"))
    cases["q"] = pd.qcut(cases["neg_fc"], 4, labels=False, duplicates="drop")
    out["by_depth_quartile"] = cases.groupby("q").agg(n=("s10", "size"), fc=("neg_fc", "mean"), ret28=("ret28", "mean"),
                                                       s5=("s5", "mean"), s10=("s10", "mean"), s20=("s20", "mean"))
    cases["calm"] = cases["rngrel"] < 1
    out["by_range_calm"] = cases.groupby("calm").apply(lambda g: slope(g, "neg_fc", "s10"))
    # all falling bars, thin vs not, raw 28d fall
    fall = d[d.ret28 < 0].copy()
    fall["f"] = -fall["ret28"]; fall["s10"] = -fall["x10"]; fall["s20"] = -fall["x20"]
    out["falls_thin_vs_not"] = fall.groupby("thin").apply(lambda g: pd.concat([slope(g, "f", "s10"), slope(g, "f", "s20").add_prefix("h20_")]))
    out["falls_rangecalm"] = fall.groupby(fall["rngrel"] < 1).apply(lambda g: slope(g, "f", "s10"))
    return out

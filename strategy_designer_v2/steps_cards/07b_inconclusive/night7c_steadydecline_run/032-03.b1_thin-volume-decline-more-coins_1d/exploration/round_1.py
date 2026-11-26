def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [3, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            hl = ((df["high"] - df["low"]) / df["close"]).values
            for i in range(0, n, 5):
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "fc": df["forecast"].iloc[i], "reg": df["regime"].iloc[i],
                     "vr": df.get("debug_info.components.vol_thin.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                     "ret28": c[i] / c[i-28] - 1 if i >= 28 else np.nan,
                     "rng": hl[max(0,i-27):i+1].mean() / np.nanmean(hl[:i+1]) if i >= 28 else np.nan}
                for h in H:
                    r[f"f{h}"] = c[i+h] / c[i] - 1 if i + h < n else np.nan
                rows.append(r)
    g = pd.DataFrame(rows)
    for h in H:
        g[f"x{h}"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
    reg = g[g.reg == "trending"].copy()
    out = {}
    def slope(d, y="x5", x="fc"):
        d = d.dropna(subset=[x, y])
        if len(d) < 20 or d[x].std() == 0: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        b, a, rr, p, se = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": b, "t": b / se, "mean_x": d[y].mean()})
    out["horizons"] = pd.DataFrame({h: slope(reg, f"x{h}") for h in H}).T
    out["by_year"] = reg.groupby("year").apply(slope)
    out["by_coin"] = reg.groupby("coin").apply(slope)
    reg["fcb"] = pd.cut(reg.fc, [-21, -10, -5, -2, -0.001, 0.001], labels=["<=-10", "-10..-5", "-5..-2", "-2..0", "0"])
    out["by_fc_bucket"] = reg.groupby("fcb")[["x5", "x10", "f5"]].agg(["mean", "count"])
    reg["depth"] = pd.qcut(reg.ret28, 3, labels=["deep", "mid", "shallow"])
    out["by_depth_mean"] = reg.groupby("depth")[["x5", "x10", "ret28"]].mean()
    out["slope_by_depth"] = reg.groupby("depth").apply(slope)
    out["slope_on_ret28_x5"] = slope(reg, "x5", "ret28")
    out["slope_on_ret28_x10"] = slope(reg, "x10", "ret28")
    reg["calm"] = pd.qcut(reg.rng, 2, labels=["calm", "wild"])
    out["slope_by_range"] = reg.groupby("calm").apply(slope)
    out["ret28_slope_by_range"] = reg.groupby("calm").apply(lambda d: slope(d, "x5", "ret28"))
    out["ret28_slope_by_range_x10"] = reg.groupby("calm").apply(lambda d: slope(d, "x10", "ret28"))
    out["thin_vs_thick_depth"] = reg.assign(thin=reg.fc < -2).groupby(["depth", "thin"])["x5"].agg(["mean", "count"])
    return out

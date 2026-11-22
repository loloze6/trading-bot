def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 84
    hs = [6, 12, 18, 42, 84, 126]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # normal drift and usual move per horizon
        d = {}
        for h in hs:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            rr = np.array(rr)
            d[h] = (np.nanmean(rr), np.nanstd(rr))
        drift[coin] = d
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.bounce.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            act = np.where((f != 0) & ~np.isnan(f))[0]
            seen = set()
            for i in act:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                rec = {"coin": coin, "win": w, "year": yr[i], "f": f[i], "raw": raw[i],
                       "past42": c[i] / c[i - 42] - 1 if i >= 42 else np.nan,
                       "past180": c[i] / c[i - 180] - 1 if i >= 180 else np.nan}
                for h in hs:
                    if i + h < n:
                        rec[f"x{h}"] = c[i + h] / c[i] - 1 - d[h][0]
                        rec[f"z{h}"] = rec[f"x{h}"] / d[h][1]
                    else:
                        rec[f"x{h}"] = np.nan
                        rec[f"z{h}"] = np.nan
                rows.append(rec)
    cs = pd.DataFrame(rows)
    out = {}

    def slope(df, y="x84", x="f"):
        s = df[[x, y]].dropna()
        if len(s) < 8:
            return pd.Series({"n": len(s)})
        r = stats.linregress(s[x], s[y])
        return pd.Series({"n": len(s), "slope": r.slope, "t": r.slope / r.stderr,
                          "mean_x": s[y].mean(), "t_mean": s[y].mean() / (s[y].std() / np.sqrt(len(s))),
                          "spearman": stats.spearmanr(s[x], s[y])[0]})

    out["all_84"] = slope(cs)
    out["by_horizon"] = pd.DataFrame({h: slope(cs, f"x{h}") for h in hs}).T
    out["by_coin"] = cs.groupby("coin").apply(slope)
    out["by_year"] = cs.groupby("year").apply(slope)
    cs["fq"] = pd.qcut(cs["f"], 5, labels=False, duplicates="drop")
    g = cs.groupby("fq")
    out["by_forecast_quintile"] = pd.DataFrame({
        "n": g["x84"].count(), "f_mean": g["f"].mean(),
        "x6": g["x6"].mean(), "x18": g["x18"].mean(), "x42": g["x42"].mean(),
        "x84": g["x84"].mean(),
        "t84": g["x84"].apply(lambda s: s.mean() / (s.std() / np.sqrt(s.count()))),
        "x126": g["x126"].mean()})
    out["by_sign"] = cs.assign(pos=cs["f"] > 0).groupby("pos").apply(slope)
    cs["trend_up"] = cs["past180"] > 0
    out["by_prior_30d_trend"] = cs.dropna(subset=["past180"]).groupby("trend_up").apply(slope)
    out["by_prior_7d_trend"] = cs.dropna(subset=["past42"]).assign(up=lambda d: d["past42"] > 0).groupby("up").apply(slope)
    out["raw_bounce_slope_84"] = slope(cs, "x84", "raw")
    out["strength_z84_slope"] = slope(cs, "z84")
    return out

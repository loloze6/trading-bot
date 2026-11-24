def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    H = [3, 5, 10]
    for coin, wins in bars.items():
        nonov = {h: [] for h in H}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o, hi, lo, c = df["open"], df["high"], df["low"], df["close"]
            rng = (hi - lo)
            rr = rng / rng.rolling(20).mean()
            flat = 1 - (c - o).abs() / rng.replace(0, np.nan)
            ret5 = c / c.shift(5) - 1
            ma50 = c.rolling(50).mean()
            n = len(df)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "year": pd.to_datetime(df["timestamp"]).dt.year,
                              "rr": rr, "flat": flat, "ret5": ret5, "above50": c > ma50,
                              "upper_close": (c - lo) / rng.replace(0, np.nan)})
            for h in H:
                fr = c.shift(-h) / c - 1
                d[f"f{h}"] = fr
                nonov[h] += list(fr.iloc[::h].dropna())
            rows.append(d)
        for h in H:
            drift[(coin, h)] = np.mean(nonov[h])
    D = pd.concat(rows, ignore_index=True)
    for h in H:
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(lambda x: drift[(x, h)])

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 3: return pd.Series({"n": len(s), "days": np.nan, "mean%": np.nan, "t": np.nan})
        v = s[col]; m = v.mean()
        dev = (v - m).groupby(s["day"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(v)
        return pd.Series({"n": len(v), "days": G, "mean%": 100 * m, "t": m / se})

    def dedup(sub):
        sub = sub.copy(); sub["cell"] = sub["pos"] // 5
        return sub.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)

    base = D.dropna(subset=["rr", "flat", "ret5"])
    up = dedup(base[(base.ret5 > 0) & (base.rr >= 1) & (base.flat >= 0.9)]).copy()
    out = {}
    out["up_by_coin_u5"] = up.groupby("coin").apply(lambda s: ct(s, "u5"))
    out["up_by_year_u5"] = up.groupby("year").apply(lambda s: ct(s, "u5"))
    up["rr_q"] = pd.qcut(up.rr, 3, labels=["lo", "mid", "hi"])
    up["rise_q"] = pd.qcut(up.ret5, 3, labels=["small", "mid", "large"])
    up["flat_q"] = pd.qcut(up.flat, 3, labels=["lo", "mid", "hi"], duplicates="drop")
    out["up_by_rr_u5"] = up.groupby("rr_q").apply(lambda s: ct(s, "u5"))
    out["up_by_rise_u5"] = up.groupby("rise_q").apply(lambda s: ct(s, "u5"))
    out["up_by_flat_u5"] = up.groupby("flat_q").apply(lambda s: ct(s, "u5"))
    out["up_by_above50_u5"] = up.groupby("above50").apply(lambda s: ct(s, "u5"))
    out["up_corr"] = pd.Series({"rr": up[["rr","u5"]].corr().iloc[0,1], "ret5": up[["ret5","u5"]].corr().iloc[0,1],
                                "flat": up[["flat","u5"]].corr().iloc[0,1], "rr_u10": up[["rr","u10"]].corr().iloc[0,1]})
    comp = {}
    comp["wide_flat_after_rise"] = ct(up, "u5")
    comp["narrow_flat_after_rise"] = ct(dedup(base[(base.ret5 > 0) & (base.rr < 1) & (base.flat >= 0.9)]), "u5")
    comp["all_after_rise"] = ct(dedup(base[base.ret5 > 0]), "u5")
    comp["wide_any_after_rise"] = ct(dedup(base[(base.ret5 > 0) & (base.rr >= 1)]), "u5")
    comp["wide_flat_no_run_ctx_all"] = ct(dedup(base[(base.rr >= 1) & (base.flat >= 0.9)]), "u5")
    comp["very_wide_flat_after_rise"] = ct(dedup(base[(base.ret5 > 0) & (base.rr >= 1.5) & (base.flat >= 0.9)]), "u5")
    comp["wide_flat_after_rise_u10"] = ct(up, "u10")
    comp["narrow_flat_after_rise_u10"] = ct(dedup(base[(base.ret5 > 0) & (base.rr < 1) & (base.flat >= 0.9)]), "u10")
    comp["all_after_rise_u10"] = ct(dedup(base[base.ret5 > 0]), "u10")
    out["comparisons"] = pd.DataFrame(comp).T
    return out

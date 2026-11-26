def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    H = [1, 3, 5, 10]
    for coin, wins in bars.items():
        nonov = {h: [] for h in H}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o, hi, lo, c = df["open"], df["high"], df["low"], df["close"]
            rng = (hi - lo)
            rr = rng / rng.rolling(20).mean()
            flat = 1 - (c - o).abs() / rng.replace(0, np.nan)
            ret5 = c / c.shift(5) - 1
            ret20 = c / c.shift(20) - 1
            ma50 = c.rolling(50).mean()
            vol20 = c.pct_change().rolling(20).std()
            vol60m = vol20.rolling(60).mean()
            f = {}
            for h in H:
                fr = c.shift(-h) / c - 1
                f[h] = fr
                nonov[h] += list(fr.iloc[::h].dropna())
            n = len(df)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "year": pd.to_datetime(df["timestamp"]).dt.year,
                              "rr": rr, "flat": flat, "ret5": ret5, "ret20": ret20,
                              "above50": c > ma50, "volrel": vol20 / vol60m,
                              "fc": df["forecast"]})
            for h in H:
                d[f"f{h}"] = f[h]
            rows.append(d)
        for h in H:
            drift[(coin, h)] = np.mean(nonov[h]); usual[(coin, h)] = np.std(nonov[h])
    D = pd.concat(rows, ignore_index=True)
    for h in H:
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(lambda x: drift[(x, h)])

    def ct(sub, col, sign=1):
        s = sub.dropna(subset=[col])
        if len(s) < 3: return pd.Series({"n": len(s), "mean%": np.nan, "t": np.nan})
        v = sign * s[col]
        m = v.mean()
        dev = (v - m).groupby(s["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(v)
        return pd.Series({"n": len(v), "days": G, "mean%": 100 * m, "t": m / se})

    def dedup(sub):
        sub = sub.copy(); sub["cell"] = sub["pos"] // 5
        return sub.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)

    base = D.dropna(subset=["rr", "flat", "ret5"])
    ev = dedup(base[(base.ret5 < 0) & (base.rr >= 1) & (base.flat >= 0.9)])
    out = {}
    out["horizons_long_event"] = pd.DataFrame({f"h{h}": ct(ev, f"u{h}") for h in H}).T
    out["by_coin_u5"] = ev.groupby("coin").apply(lambda s: ct(s, "u5"))
    out["by_year_u5"] = ev.groupby("year").apply(lambda s: ct(s, "u5"))
    ev = ev.copy()
    ev["rr_q"] = pd.qcut(ev.rr, 3, labels=["lo", "mid", "hi"])
    ev["fall_q"] = pd.qcut(ev.ret5, 3, labels=["deep", "mid", "shallow"])
    out["by_rr_tercile_u5"] = ev.groupby("rr_q").apply(lambda s: ct(s, "u5"))
    out["by_fall_tercile_u5"] = ev.groupby("fall_q").apply(lambda s: ct(s, "u5"))
    out["by_above50_u5"] = ev.groupby("above50").apply(lambda s: ct(s, "u5"))
    out["by_ret20sign_u5"] = ev.groupby(ev.ret20 > 0).apply(lambda s: ct(s, "u5"))
    out["by_volrel_u5"] = ev.groupby(ev.volrel > 1).apply(lambda s: ct(s, "u5"))
    out["corr_rr_flat_ret5_vs_u5"] = pd.Series({
        "rr": ev[["rr", "u5"]].corr().iloc[0, 1], "flat": ev[["flat", "u5"]].corr().iloc[0, 1],
        "ret5": ev[["ret5", "u5"]].corr().iloc[0, 1]})
    # comparisons
    comp = {}
    comp["wide_flat_after_fall_long"] = ct(ev, "u5")
    comp["narrow_flat_after_fall_long"] = ct(dedup(base[(base.ret5 < 0) & (base.rr < 1) & (base.flat >= 0.9)]), "u5")
    comp["wide_flat_after_rise_short"] = ct(dedup(base[(base.ret5 > 0) & (base.rr >= 1) & (base.flat >= 0.9)]), "u5", -1)
    comp["all_after_fall_long"] = ct(dedup(base[base.ret5 < 0]), "u5")
    comp["wide_any_after_fall_long"] = ct(dedup(base[(base.ret5 < 0) & (base.rr >= 1)]), "u5")
    comp["very_wide_flat_after_fall"] = ct(dedup(base[(base.ret5 < 0) & (base.rr >= 1.5) & (base.flat >= 0.9)]), "u5")
    out["comparisons_u5"] = pd.DataFrame(comp).T
    wr = dedup(base[(base.ret5 > 0) & (base.rr >= 1) & (base.flat >= 0.9)])
    out["rise_short_horizons"] = pd.DataFrame({f"h{h}": ct(wr, f"u{h}", -1) for h in H}).T
    return out

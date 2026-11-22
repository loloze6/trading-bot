def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 84
    bars = data["bars"]
    rows = []
    allp = []
    for coin, wins in bars.items():
        # drift and usual move
        nr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            nr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(nr); usual = np.std(nr, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            fwd = c.shift(-H) / c - 1
            rng = (hi.rolling(6).max() - lo.rolling(6).min()) / (hi - lo).rolling(180).mean()
            r6 = c / c.shift(6) - 1
            r540 = c / c.shift(540) - 1
            ts = pd.to_datetime(df["timestamp"])
            raw = df.get("debug_info.components.panic.last_history_value")
            fc = df["forecast"]
            cell = np.arange(len(df)) // H
            d = pd.DataFrame({"coin": coin, "w": w, "cell": cell, "fc": fc, "raw": raw,
                              "fwd": fwd, "rng": rng, "r6": r6, "r540": r540,
                              "year": ts.dt.year, "drift": drift, "usual": usual})
            d = d[d["fwd"].notna()]
            # tested cases
            cs = d[d["fc"] >= 2].groupby("cell").head(1)
            rows.append(cs)
            # all panic-falls (no uptrend condition)
            p = d[(d["rng"] >= 7.5) & (d["r6"] < 0)].groupby("cell").head(1)
            allp.append(p)
    cs = pd.concat(rows); ap = pd.concat(allp)
    for x in (cs, ap):
        x["um"] = x["fwd"] - x["drift"]; x["st"] = x["um"] / x["usual"]
    def summ(g):
        n = len(g); m = g["um"].mean(); s = g["um"].std(ddof=1)
        return pd.Series({"n": n, "mean_um": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan,
                          "strength": g["st"].mean(), "share_pos": (g["um"] > 0).mean()})
    out = {}
    out["forecast_dist_cases"] = cs["fc"].describe()
    out["fc_eq_20_share"] = float((cs["fc"] >= 19.99).mean())
    out["all_cases"] = summ(cs)
    cs["raw_q"] = pd.qcut(cs["raw"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_raw_tercile"] = cs.groupby("raw_q").apply(summ)
    cs["fall_q"] = pd.qcut(cs["r6"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["by_fall_tercile"] = cs.groupby("fall_q").apply(summ)
    c2 = cs[cs["r540"].notna()].copy()
    c2["rise_q"] = pd.qcut(c2["r540"].rank(method="first"), 3, labels=["small", "mid", "large"])
    out["by_rise_tercile"] = c2.groupby("rise_q").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["by_coin"] = cs.groupby("coin").apply(summ)
    # brief-level: all panic falls by 90d sign
    a2 = ap[ap["r540"].notna()].copy()
    a2["up90"] = np.where(a2["r540"] > 0, "up", "down")
    out["allpanic_by_90d_sign"] = a2.groupby("up90").apply(summ)
    out["allpanic_all"] = summ(ap)
    ap["fall_q"] = pd.qcut(ap["r6"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["allpanic_by_fall"] = ap.groupby("fall_q").apply(summ)
    out["corr_raw_um_spearman"] = float(stats.spearmanr(cs["raw"], cs["um"], nan_policy="omit")[0])
    return out

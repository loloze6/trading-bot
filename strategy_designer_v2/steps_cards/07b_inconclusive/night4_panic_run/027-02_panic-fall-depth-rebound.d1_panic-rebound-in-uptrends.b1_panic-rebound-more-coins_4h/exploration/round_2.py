def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 84
    bars = data["bars"]
    allp = []
    for coin, wins in bars.items():
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
            ma6 = r6.abs().rolling(180).mean()
            r42 = c / c.shift(42) - 1
            ts = pd.to_datetime(df["timestamp"])
            raw = df.get("debug_info.components.panic.last_history_value")
            reg = df["regime"]
            cell = np.arange(len(df)) // H
            d = pd.DataFrame({"coin": coin, "w": w, "cell": cell, "raw": raw, "reg": reg,
                              "fwd": fwd, "rng": rng, "r6": r6, "sfall": -r6 / ma6, "r42": r42,
                              "year": ts.dt.year, "drift": drift, "usual": usual})
            d = d[d["fwd"].notna()]
            p = d[(d["reg"] == "mean_reversion") & (d["r6"] < 0)].groupby("cell").head(1)
            allp.append(p)
    ap = pd.concat(allp)
    ap["um"] = ap["fwd"] - ap["drift"]; ap["st"] = ap["um"] / ap["usual"]
    def summ(g):
        n = len(g); m = g["um"].mean(); s = g["um"].std(ddof=1)
        return pd.Series({"n": n, "mean_um": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan,
                          "strength": g["st"].mean(), "share_pos": (g["um"] > 0).mean()})
    out = {}
    ap["up"] = np.where(ap["raw"] > 0, "up90", "notup90")
    out["regime_panic_all"] = summ(ap)
    out["by_up"] = ap.groupby("up").apply(summ)
    a = ap[ap["sfall"].notna()].copy()
    a["sf_q"] = pd.qcut(a["sfall"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["by_scaled_fall"] = a.groupby("sf_q").apply(summ)
    out["by_scaled_fall_and_up"] = a.groupby(["up", "sf_q"]).apply(summ)
    out["spearman_sfall_um"] = float(stats.spearmanr(a["sfall"], a["um"])[0])
    a["prior7d"] = np.where(a["r42"] > 0, "prior7d_up", "prior7d_down")
    out["by_prior7d"] = a.groupby("prior7d").apply(summ)
    out["deep_by_year"] = a[a["sf_q"] == "deep"].groupby("year").apply(summ)
    out["all_by_year"] = a.groupby("year").apply(summ)
    for h2 in (42,):
        pass
    return out

def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            if len(c) < 30: continue
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(c)), "yr": ts.dt.year,
                "fc": b["forecast"].astype(float).values,
                "r1": r1, "vol20": vol20,
                "r60": c / c.shift(60) - 1,
                "f20": c.shift(-20) / c - 1, "f10": c.shift(-10) / c - 1,
            })
            df["vol_rel"] = vol20 / vol20.rolling(60, min_periods=20).median()
            df["r1z"] = r1 / vol20.shift(1)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (10, 20):
        g = D[D["pos"] % h == 0]
        st = g.groupby("coin")["f%d" % h].agg(["mean", "std"])
        D["m%d" % h] = D["coin"].map(st["mean"]); D["s%d" % h] = D["coin"].map(st["std"])
        D["u%d" % h] = (D["f%d" % h] - D["m%d" % h]) / D["s%d" % h]
        D["x%d" % h] = D["f%d" % h] - D["m%d" % h]
    def tstat(s):
        s = s.dropna(); return s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan
    for off in (0, 7, 13):
        g = D[(D["pos"] - off) % 20 == 0].dropna(subset=["r1z", "u20"]).copy()
        x = -g["r1z"].clip(-4, 4) * g["u20"]
        out["rev_slope_t_offset%d" % off] = pd.Series({"t": tstat(x), "n": len(x)})
    g = D[D["pos"] % 20 == 0].dropna(subset=["r1z", "u20", "x20"]).copy()
    g["q"] = pd.qcut(g["r1z"].rank(method="first"), 5, labels=False)
    out["r1z_quint_raw_pct"] = g.groupby("q").agg(u=("u20", "mean"), raw_unusual_pct=("x20", lambda s: s.mean() * 100),
                                                  med_raw_pct=("x20", lambda s: s.median() * 100), n=("u20", "count"))
    g["xr"] = -g["r1z"].clip(-4, 4) * g["u20"]
    out["rev_by_year"] = g.groupby("yr")["xr"].agg(["mean", "count", tstat])
    out["rev_by_coin"] = g.groupby("coin")["xr"].agg(["mean", "count", tstat])
    out["rev_by_sign"] = g.groupby(np.sign(g["r1z"]))["xr"].agg(["mean", "count", tstat])
    out["rev_by_volhi"] = g.groupby(g["vol_rel"] > 1)["xr"].agg(["mean", "count", tstat])
    # 10 day horizon
    g10 = D[D["pos"] % 10 == 0].dropna(subset=["r1z", "u10"])
    out["rev_h10_t"] = pd.Series({"t": tstat(-g10["r1z"].clip(-4, 4) * g10["u10"]), "n": len(g10)})
    # vol_rel -> 20d raw
    gv = D[D["pos"] % 20 == 0].dropna(subset=["vol_rel", "u20", "x20"]).copy()
    gv["xv"] = (gv["vol_rel"].clip(0, 3) - 1) * gv["u20"]
    out["volrel_by_year"] = gv.groupby("yr")["xv"].agg(["mean", "count", tstat])
    gv["q"] = pd.qcut(gv["vol_rel"].rank(method="first"), 5, labels=False)
    out["volrel_quint_raw_pct"] = gv.groupby("q").agg(u=("u20", "mean"), raw_pct=("x20", lambda s: s.mean() * 100), n=("u20", "count"))
    # 60d trend times vol interaction
    gi = D[D["pos"] % 20 == 0].dropna(subset=["r60", "vol_rel", "u20"]).copy()
    gi["xi"] = np.sign(gi["r60"]) * gi["u20"]
    out["trend_by_volq"] = gi.groupby(pd.qcut(gi["vol_rel"].rank(method="first"), 4, labels=False))["xi"].agg(["mean", "count", tstat])
    out["trend_by_volhi_year"] = gi[gi.vol_rel > 1].groupby("yr")["xi"].agg(["mean", "count", tstat])
    return out

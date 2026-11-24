def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, b in data["bars"][coin].items():
        b = b.sort_values("timestamp").reset_index(drop=True)
        c = b["close"].astype(float)
        r = c.pct_change()
        vol = r.rolling(30, min_periods=20).std().shift(1)
        z = r / vol
        df = pd.DataFrame({
            "w": w, "pos_i": np.arange(len(b)),
            "r": r, "z": z, "vol": vol,
            "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
            "f20": c.shift(-20) / c - 1,
            "r60": c / c.shift(60) - 1,
            "range": (b["high"] - b["low"]) / b["close"],
            "alloc": b["postRebalance_current_allocation"].astype(float),
            "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            "yr": pd.to_datetime(b["timestamp"]).dt.year,
            "zrec": b.get("debug_info.components.fade_move.last_history_value"),
        })
        df["gain"] = df["alloc"] * df["f1"]
        df["vol_rank"] = vol / vol.rolling(180, min_periods=60).median()
        rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu1 = d["f1"].mean()
    out["n_bars_mean_f1"] = pd.Series({"n": d["f1"].notna().sum(), "mean_f1": mu1, "sd_f1": d["f1"].std(), "n_windows": d["w"].nunique()})

    def grp(df, key, col="f1"):
        g = df.dropna(subset=[col]).groupby(key)[col]
        res = g.agg(["count", "mean", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res

    dd = d.dropna(subset=["z", "f1"]).copy()
    dd["zbin"] = pd.qcut(dd["z"], 10, labels=False)
    t1 = grp(dd, "zbin")
    t1["zmean"] = dd.groupby("zbin")["z"].mean()
    out["f1_by_z_decile"] = t1
    # multi-day horizons, non-overlapping grids
    for h, col in [(3, "f3"), (5, "f5")]:
        g = d[(d["pos_i"] % h == 0)].dropna(subset=["z", col]).copy()
        g["zbin"] = pd.qcut(g["z"], 5, labels=False)
        t = grp(g, "zbin", col); t["zmean"] = g.groupby("zbin")["z"].mean()
        out[f"f{h}_by_z_quintile_grid"] = t
    # 60-day move vs 20-day forward (brief's horizon), non-overlap grid 20
    g = d[d["pos_i"] % 20 == 0].dropna(subset=["r60", "f20"]).copy()
    if len(g) > 20:
        g["bin"] = pd.qcut(g["r60"], 4, labels=False)
        t = grp(g, "bin", "f20"); t["r60mean"] = g.groupby("bin")["r60"].mean()
        out["f20_by_r60_quartile"] = t
    # reversal slope by vol regime
    dd["vq"] = pd.qcut(dd["vol"], 3, labels=False)
    res = []
    for k, s in dd.groupby("vq"):
        sl = stats.linregress(s["z"], s["f1"])
        res.append({"vq": k, "n": len(s), "vol": s["vol"].mean(), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["slope_by_vol_tercile"] = pd.DataFrame(res)
    dv = dd.dropna(subset=["vol_rank"]).copy()
    dv["vr"] = pd.qcut(dv["vol_rank"], 3, labels=False)
    res = []
    for k, s in dv.groupby("vr"):
        sl = stats.linregress(s["z"], s["f1"])
        res.append({"vr": k, "n": len(s), "vol_rank": s["vol_rank"].mean(), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["slope_by_relative_vol"] = pd.DataFrame(res)
    # by year
    res = []
    for k, s in dd.groupby("yr"):
        sl = stats.linregress(s["z"], s["f1"])
        gg = s["alloc"] * (s["f1"] - mu1)
        res.append({"yr": k, "n": len(s), "slope": sl.slope, "t": sl.slope / sl.stderr, "gain": gg.mean(), "gain_t": gg.mean() / gg.std() * np.sqrt(len(gg))})
    out["by_year"] = pd.DataFrame(res)
    out["f1_by_weekday"] = grp(d, "wd")
    # range (intraday) z vs next day abs
    dd["rz"] = dd["range"] / dd["vol"]
    dd["rzbin"] = pd.qcut(dd["rz"], 5, labels=False)
    out["f1_by_rangez_quintile"] = grp(dd, "rzbin")
    # book gains: largest gain/loss days
    dd["gq"] = pd.qcut(dd["gain"].rank(method="first"), 20, labels=False)
    gs = dd.groupby("gq").agg(gain=("gain", "mean"), z=("z", "mean"), absz=("z", lambda x: x.abs().mean()), alloc=("alloc", "mean"), vol=("vol", "mean"), n=("gain", "size"))
    out["book_gain_ventiles"] = gs.iloc[[0, 1, 2, 9, 10, 17, 18, 19]]
    # sign of previous two days
    dd["r_prev"] = d.loc[dd.index, "r"].groupby(d.loc[dd.index, "w"]).shift(1)
    dd["two_same"] = np.sign(dd["r"]) * np.sign(dd["r_prev"])
    s = dd.dropna(subset=["two_same"])
    s = s.assign(signed=-np.sign(s["z"]) * s["f1"])
    out["fade_gain_by_two_day_same_sign"] = grp(s, "two_same", "signed")
    return out

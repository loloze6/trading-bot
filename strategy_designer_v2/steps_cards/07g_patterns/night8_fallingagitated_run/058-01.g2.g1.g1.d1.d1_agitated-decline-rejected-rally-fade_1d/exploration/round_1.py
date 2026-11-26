def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            s30 = r.rolling(30, min_periods=15).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fa": (b["regime"] != "chop").astype(int),
                "reg": b["regime"],
                "r": r, "rz": r / s30,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "dhigh": (c - h) / c / s30,
                "dlow": (c - l) / c / s30,
                "rng": (h - l) / c / s30,
                "r3z": (c / c.shift(3) - 1) / s30,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "pos": b["postRebalance_current_allocation"],
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            up = (r > 0).astype(int)
            streak = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            dn = (r < 0).astype(int)
            dstreak = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            df["ups"] = streak; df["dns"] = dstreak
            df["idx"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d["f1"].mean()
    d["u1"] = d["f1"] - drift
    def summ(g, col="u1"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out["drift1d%"] = 100 * drift
    out["fa_share"] = d["fa"].mean()
    out["by_profile_updown"] = d.groupby(["fa", np.sign(d["r"])]).apply(summ)
    fa = d[d["fa"] == 1].copy()
    nf = d[d["fa"] == 0].copy()
    fa["rzq"] = pd.qcut(fa["rz"], 5, labels=False, duplicates="drop")
    out["fa_by_rz_quint"] = fa.groupby("rzq").apply(summ)
    nf["rzq"] = pd.qcut(nf["rz"], 5, labels=False, duplicates="drop")
    out["nonfa_by_rz_quint"] = nf.groupby("rzq").apply(summ)
    fa["clvq"] = pd.qcut(fa["clv"], 5, labels=False, duplicates="drop")
    out["fa_by_clv_quint"] = fa.groupby("clvq").apply(summ)
    nf["clvq"] = pd.qcut(nf["clv"], 5, labels=False, duplicates="drop")
    out["nonfa_by_clv_quint"] = nf.groupby("clvq").apply(summ)
    fa["upsc"] = fa["ups"].clip(0, 4); fa["dnsc"] = fa["dns"].clip(0, 4)
    out["fa_by_upstreak"] = fa.groupby("upsc").apply(summ)
    out["fa_by_dnstreak"] = fa.groupby("dnsc").apply(summ)
    out["fa_by_weekday"] = fa.groupby("wd").apply(summ)
    out["all_by_weekday"] = d.groupby("wd").apply(summ)
    # 3-day, non-overlapping grid
    g3 = d[d["idx"] % 3 == 0].copy()
    g3["u3"] = g3["f3"] - d.loc[d["idx"] % 3 == 0, "f3"].mean()
    fa3 = g3[g3["fa"] == 1].copy()
    fa3["r3q"] = pd.qcut(fa3["r3z"], 5, labels=False, duplicates="drop")
    out["fa_3d_by_r3z_quint"] = fa3.groupby("r3q").apply(lambda g: summ(g, "u3"))
    nf3 = g3[g3["fa"] == 0].copy()
    nf3["r3q"] = pd.qcut(nf3["r3z"], 5, labels=False, duplicates="drop")
    out["nonfa_3d_by_r3z_quint"] = nf3.groupby("r3q").apply(lambda g: summ(g, "u3"))
    # rejected rallies outside profile: up day after down, dhigh quintile
    first_up = d[(d["ups"] == 1)]
    fu_nf = first_up[first_up["fa"] == 0].copy()
    fu_nf["q"] = pd.qcut(fu_nf["dhigh"], 3, labels=False, duplicates="drop")
    out["nonfa_firstup_by_dhigh_terc"] = fu_nf.groupby("q").apply(summ)
    fu_fa = first_up[first_up["fa"] == 1].copy()
    fu_fa["q"] = pd.qcut(fu_fa["dhigh"], 3, labels=False, duplicates="drop")
    out["fa_firstup_by_dhigh_terc"] = fu_fa.groupby("q").apply(summ)
    # down days in FA: close near low vs not
    dd = fa[fa["r"] < 0].copy()
    dd["q"] = pd.qcut(dd["dlow"], 3, labels=False, duplicates="drop")
    out["fa_downday_by_dlow_terc"] = dd.groupby("q").apply(summ)
    # by window, FA cases of the strategy
    cases = d[(d["reg"] == "mean_reversion")]
    out["cases_by_win"] = cases.groupby("win").apply(summ)
    # book daily returns: largest days
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bk.append(x.assign(coin=coin, win=w))
    bk = pd.concat(bk)
    br = bk.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_win"] = br.groupby(level=0).agg(["count", "mean", "std", "sum"])
    return out

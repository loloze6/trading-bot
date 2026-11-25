def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []; drift = {}
    for coin, ws in bars.items():
        allg = []
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd2"] = c.shift(-2) / c - 1
            b["ret1"] = c.pct_change()
            b["sd30"] = b["ret1"].rolling(30, min_periods=20).std()
            b["low30"] = l.shift(1).rolling(30, min_periods=30).min()
            b["high30"] = h.shift(1).rolling(30, min_periods=30).max()
            b["reclaim"] = (l < b["low30"]) & (c >= b["low30"])
            b["fakeout_hi"] = (h > b["high30"]) & (c <= b["high30"])
            b["depth"] = (b["low30"] - l) / b["low30"]
            b["clv"] = (c - l) / (h - l).replace(0, np.nan)
            b["rec_rng"] = (c - b["low30"]) / (h - l).replace(0, np.nan)
            b["ret30"] = c / c.shift(30) - 1
            b["ret10"] = c / c.shift(10) - 1
            b["inprof"] = b["regime"] != "chop"
            b["pos"] = np.arange(len(b)); b["cell"] = b["pos"] // 5
            b["coin"] = coin; b["win"] = w
            ts = pd.to_datetime(b["timestamp"]); b["dkey"] = ts.dt.floor("D"); b["yr"] = ts.dt.year
            allg.append(b.loc[b["pos"] % 5 == 0, "fwd5"].dropna())
            rows.append(b)
        drift[coin] = pd.concat(allg).mean()
    B = pd.concat(rows, ignore_index=True)
    B["ex5"] = B["fwd5"] - B["coin"].map(drift)
    B["volrank"] = B.groupby("coin")["sd30"].rank(pct=True)

    def ev(mask, col="ex5"):
        d = B[mask & B[col].notna()]
        d = d.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)
        if len(d) < 3: return [len(d), np.nan, np.nan, np.nan]
        m = d[col].mean()
        s = d.groupby("dkey")[col].apply(lambda x: (x - m).sum()); D = len(s)
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / len(d)
        return [len(d), D, m, m / se if se > 0 else np.nan]
    def tab(groups, col="ex5"):
        return pd.DataFrame({k: ev(v, col) for k, v in groups.items()}, index=["cases", "days", "mean", "t"]).T.round(4)

    P = B["inprof"]; R = B["reclaim"]
    r = {}
    tr = pd.cut(B["ret30"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    ag = B["volrank"] > 0.5
    g = {}
    for t in ["fall", "chop", "rise"]:
        for a, nm in [(True, "agit"), (False, "calm")]:
            g[f"{t}_{nm}"] = R & (tr == t) & (ag == a)
    r["reclaim_by_trend30_vol"] = tab(g)
    r["reclaim_out_by_year"] = tab({str(y): R & ~P & (B["yr"] == y) for y in sorted(B["yr"].unique())})
    # graded within reclaims outside profile
    Ro = R & ~P
    med_c = B.loc[Ro, "rec_rng"].median(); med_d = B.loc[Ro, "depth"].median()
    r["reclaim_out_split"] = tab({"rec_rng_hi": Ro & (B["rec_rng"] > med_c), "rec_rng_lo": Ro & (B["rec_rng"] <= med_c),
                                 "depth_hi": Ro & (B["depth"] > med_d), "depth_lo": Ro & (B["depth"] <= med_d)})
    r["reclaim_out_fwd2"] = tab({"out": Ro, "in": R & P}, col="fwd2")
    r["reclaim_out_corr"] = pd.Series({
        "spearman_recrng_ex5": B.loc[Ro, ["rec_rng", "ex5"]].corr("spearman").iloc[0, 1],
        "spearman_depth_ex5": B.loc[Ro, ["depth", "ex5"]].corr("spearman").iloc[0, 1],
        "spearman_ret30_ex5": B.loc[Ro, ["ret30", "ex5"]].corr("spearman").iloc[0, 1]}).round(3)
    F = B["fakeout_hi"]
    r["fakeout_high"] = tab({"all": F, "rise": F & (tr == "rise"), "chop": F & (tr == "chop"), "fall": F & (tr == "fall")})
    q10 = pd.qcut(B["ret10"], 5, labels=False)
    r["ret10_by_trend"] = tab({f"{t}_q{i}": (tr == t) & (q10 == i) for t in ["fall", "chop", "rise"] for i in [0, 4]})
    r["ret10_by_year_top_minus"] = pd.DataFrame({str(y): [ev((B["yr"] == y) & (q10 == 4))[2], ev((B["yr"] == y) & (q10 == 0))[2]] for y in sorted(B["yr"].unique())}, index=["q4", "q0"]).T.round(4)
    return r

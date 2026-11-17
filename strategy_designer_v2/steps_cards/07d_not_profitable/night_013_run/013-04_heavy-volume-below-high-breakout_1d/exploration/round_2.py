def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; v = b["volume"].values
            tr = (b["regime"] == "trending").values
            n = len(b)
            last = -10**6
            runmax = pd.Series(hi).cummax().shift(1).values
            vr = (pd.Series(v).rolling(10).mean() / pd.Series(v).rolling(90, min_periods=30).mean()).values
            for i in range(n):
                if tr[i]: last = i
                rec = {"coin": c, "w": w, "pos": i, "tr": tr[i], "since": (i - last) if last > -10**6 else np.nan,
                       "dist": cl[i] / runmax[i] - 1 if i > 0 else np.nan, "vr": vr[i]}
                rec["f30"] = cl[i+30]/cl[i]-1 if i+30 < n else np.nan
                recs.append(rec)
    R = pd.DataFrame(recs)
    G = R[(R.pos % 30 == 0)].dropna(subset=["f30"])
    G["sinceb"] = pd.cut(G["since"], [-1, 0, 10, 30, 60, 120, 10000])
    out["f30_grid_by_days_since_breakout"] = G.groupby("sinceb", observed=True)["f30"].agg(["mean", "count", "std"])
    out["f30_grid_never_broke_in_window"] = G[G.since.isna()]["f30"].agg(["mean", "count", "std"])
    G["distb"] = pd.qcut(G["dist"], 5)
    out["f30_grid_by_dist_from_window_high"] = G.groupby("distb", observed=True)["f30"].agg(["mean", "count", "std"])
    rho = stats.spearmanr(G["dist"], G["f30"], nan_policy="omit")
    out["spearman_dist_f30"] = pd.Series({"rho": rho.correlation, "p": rho.pvalue, "n": G["dist"].notna().sum()})
    # 30-day hold after breakout events (dedup 30 bars), daily path
    ev = []
    for (c, w), g in R.groupby(["coin", "w"]):
        lastev = -1000
        for _, r in g[g.tr].iterrows():
            if r.pos - lastev >= 30 and not np.isnan(r.f30):
                ev.append(r); lastev = r.pos
    E = pd.DataFrame(ev)
    out["events_f30"] = pd.Series({"n": len(E), "mean_f30": E.f30.mean(), "t_vs_0": E.f30.mean()/E.f30.std()*np.sqrt(len(E)),
                                   "share_pos": (E.f30 > 0).mean(), "worst": E.f30.min()})
    E["vrb"] = pd.qcut(E["vr"], 3)
    out["events_f30_by_volratio"] = E.groupby("vrb", observed=True)["f30"].agg(["mean", "count"])
    # book's realized vs exposure by window-year? exposure fraction of trending bars
    out["trend_bar_share"] = pd.Series({"share": R.tr.mean(), "bars_within30_after": ((R.since >= 0) & (R.since < 30)).mean()})
    return out

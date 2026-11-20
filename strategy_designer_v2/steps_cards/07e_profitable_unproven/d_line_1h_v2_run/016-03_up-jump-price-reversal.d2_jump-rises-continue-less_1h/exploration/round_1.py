def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    port = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    port["year"] = pd.to_datetime(port["day"]).dt.year
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book_by_year"] = port.groupby("year")[["book_return", "coin_return"]].agg(["mean", "count"])
    wb = port.groupby("w")["book_return"].agg(["mean", "count"])
    out["book_by_window"] = wb
    # market part vs timing per coin, bar-level
    mk = []
    fw = []
    for c, ws in data["bars"].items():
        allr = []; allpos = []
        for w, b in ws.items():
            r = b["close"].pct_change().shift(-1)
            allr.append(r); allpos.append(b["postRebalance_current_allocation"])
        r = pd.concat(allr); p = pd.concat(allpos)
        mu = r.mean()
        g = (p * r).mean()
        mk.append({"coin": c, "gain_hr": g, "market_part_hr": p.mean() * mu, "timing_hr": g - p.mean() * mu,
                   "mean_pos": p.mean(), "share_bars_in": (p.abs() > 1e-6).mean()})
        # forward-return analysis on grid
        for w, b in ws.items():
            cl = b["close"].values
            n = len(cl)
            hr = np.diff(np.log(cl), prepend=np.nan)
            for i in range(72, n - 72, 72):
                past = cl[i] / cl[i - 72] - 1
                seg = cl[i - 72:i + 1]
                gains = np.diff(seg)
                net = seg[-1] - seg[0]
                top = np.sort(gains)[-3:].sum()
                share = top / net if net > 0 else np.nan
                rec = {"coin": c, "w": w, "past72": past, "share": share,
                       "f24": cl[i + 24] / cl[i] - 1, "f72": cl[i + 72] / cl[i] - 1,
                       "vol72": np.nanstd(hr[i - 71:i + 1]),
                       "pos": b["postRebalance_current_allocation"].iloc[i]}
                fw.append(rec)
    out["market_vs_timing"] = pd.DataFrame(mk).set_index("coin")
    F = pd.DataFrame(fw)
    F["up"] = F["past72"] > 0
    out["fwd_by_up"] = F.groupby("up")[["f24", "f72"]].agg(["mean", "count"])
    a = F[F.up]["f72"]; b_ = F[~F.up]["f72"]
    out["up_minus_down_f72_t"] = stats.ttest_ind(a, b_, equal_var=False).statistic
    F["pq"] = F.groupby("coin")["past72"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["fwd_by_past_quintile"] = F.groupby("pq")[["past72", "f72"]].agg(["mean", "count"])
    U = F[F.up].copy()
    U["sq"] = U.groupby("coin")["share"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    out["up_fwd_by_share_quartile"] = U.groupby("sq")[["share", "past72", "f24", "f72"]].mean()
    out["up_fwd_by_pos_tercile"] = F.assign(pt=pd.qcut(F["pos"].rank(method="first"), 3, labels=False)).groupby("pt")[["pos", "past72", "f72"]].mean()
    return out

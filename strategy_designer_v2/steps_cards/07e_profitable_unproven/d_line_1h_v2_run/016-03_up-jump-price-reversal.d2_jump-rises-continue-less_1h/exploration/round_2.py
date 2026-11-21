def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # workflow market part on daily book
    rows = []
    for c, ws in data["days"].items():
        allc = pd.concat([d["coin_return"] for d in ws.values()])
        mu = allc.mean()
        for w, d in ws.items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.strftime("%Y-%m-%d")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d[["day", "book_return"]].copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.strftime("%Y-%m-%d")
            dd["pos"] = dd["day"].map(pos)
            dd["mkt"] = dd["pos"] * mu
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows).dropna(subset=["book_return", "pos"])
    port = D.groupby(["w", "day"])[["book_return", "mkt"]].mean()
    out["book_mean_vs_market_part"] = pd.Series({"book": port["book_return"].mean(), "market_part": port["mkt"].mean(),
                                                 "timing": port["book_return"].mean() - port["mkt"].mean(), "n_days": len(port)})
    fw = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; n = len(cl)
            lr = np.diff(np.log(cl))
            for i in range(72, n - 144, 72):
                g = lr[i - 72:i]
                past = cl[i] / cl[i - 72] - 1
                pos_g = g[g > 0]
                top3 = np.sort(g)[-3:].sum()
                fw.append({"coin": c, "w": w, "past72": past,
                           "share_net": top3 / g.sum() if g.sum() > 0 else np.nan,
                           "share_gross": top3 / pos_g.sum() if len(pos_g) else np.nan,
                           "vol": g.std(),
                           "f24": cl[i + 24] / cl[i] - 1, "f72": cl[i + 72] / cl[i] - 1,
                           "f144": cl[i + 144] / cl[i] - 1})
    F = pd.DataFrame(fw)
    U = F[F.past72 > 0].copy()
    U["size_t"] = U.groupby("coin")["past72"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    U["gs"] = U.groupby(["coin", "size_t"])["share_gross"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=False))
    out["up_size_x_grossshare_f72"] = U.groupby(["size_t", "gs"])["f72"].agg(["mean", "count"])
    tt = {}
    for s in range(3):
        x = U[U.size_t == s]
        tt[s] = stats.ttest_ind(x[x.gs == 0]["f72"], x[x.gs == 1]["f72"], equal_var=False).statistic
    out["grind_minus_jump_t_within_size"] = pd.Series(tt)
    # regression f72 on z(past72) and z(share_gross) among up
    z = lambda s: (s - s.mean()) / s.std()
    X = np.column_stack([np.ones(len(U)), z(U.past72), z(U.share_gross), z(U.vol)])
    y = U.f72.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=4)
    out["reg_f72_up"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "past72", "share_gross", "vol"])
    # momentum by size of rise, horizons, all bars
    F["pq"] = F.groupby("coin")["past72"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["fwd_by_past_quintile_h"] = F.groupby("pq")[["past72", "f24", "f72", "f144"]].mean()
    # slope t of f72 on past72 among up, per coin
    sl = {}
    for c, x in U.groupby("coin"):
        r = stats.linregress(x.past72, x.f72); sl[c] = (r.slope, r.slope / r.stderr, len(x))
    out["up_slope_f72_on_past72_by_coin"] = pd.DataFrame(sl, index=["slope", "t", "n"]).T
    r = stats.linregress(U.past72, U.f72)
    out["up_slope_pooled"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(U)})
    # top quintile vs middle f72 t
    out["q4_minus_q2_f72_t"] = stats.ttest_ind(F[F.pq == 4].f72, F[F.pq == 2].f72, equal_var=False).statistic
    return out

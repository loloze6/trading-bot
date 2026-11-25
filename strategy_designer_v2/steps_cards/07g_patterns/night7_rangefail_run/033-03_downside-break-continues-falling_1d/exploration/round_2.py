def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            hh = hi.shift(1).rolling(20).max(); ll = lo.shift(1).rolling(20).min()
            pos = (c - ll) / (hh - ll)
            above = (c - hh) / hh * 100
            below = (c - ll) / ll * 100
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            r20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n, H):
                if i + H >= n: continue
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), fwd=fwd[i], pos=pos[i], above=above[i],
                                 below=below[i], vol20=vol20[i], vratio=vol20[i] / vol60[i] if vol60[i] > 0 else np.nan,
                                 r20=r20[i], r20z=r20[i] / (vol20[i] * np.sqrt(20)) if vol20[i] > 0 else np.nan))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["volpct"] = d.groupby("coin")["vol20"].rank(pct=True)
    out = {}
    def dp_t(x, wcol=None):
        v = (x["ex"] if wcol is None else x["ex"] * x[wcol]).groupby(x["day"]).sum()
        return v.mean() / (v.std() / np.sqrt(len(v))), len(v)
    def slope_stats(x, col):
        x = x.dropna(subset=[col, "ex"]).copy()
        x["rk"] = x.groupby("coin")[col].rank(pct=True) - 0.5
        t, nd = dp_t(x, "rk")
        return pd.Series({"spearman": stats.spearmanr(x[col], x["ex"])[0], "n": len(x), "days": nd, "t_dp": t})
    # range position slope by vol half and by window
    res = {}
    for name, x in [("all", d), ("calm", d[d.volpct <= 0.5]), ("agit", d[d.volpct > 0.5]),
                    ("vratio_low", d[d.vratio <= d.vratio.median()]), ("vratio_high", d[d.vratio > d.vratio.median()])]:
        res[name] = slope_stats(x, "pos")
    out["pos_slope_by_vol"] = pd.DataFrame(res).T.round(4)
    out["pos_slope_by_window"] = d.groupby("w").apply(lambda x: slope_stats(x, "pos")).round(3)
    # above-high cases: sign, size, graded
    a = d[d.above > 0].copy()
    t, nd = dp_t(a)
    out["above_high"] = pd.Series({"mean_ex": a.ex.mean(), "n": len(a), "days": nd, "t_dp": t,
                                   "spearman_depth": stats.spearmanr(a.above, a.ex)[0]}).round(4)
    for nm, x in [("calm", a[a.volpct <= 0.5]), ("agit", a[a.volpct > 0.5])]:
        t, nd = dp_t(x)
        out["above_high_" + nm] = pd.Series({"mean_ex": x.ex.mean(), "n": len(x), "days": nd, "t_dp": t}).round(4)
    bl = d[d.below < 0].copy()
    for nm, x in [("all", bl), ("calm", bl[bl.volpct <= 0.5]), ("agit", bl[bl.volpct > 0.5])]:
        t, nd = dp_t(x)
        out["below_low_" + nm] = pd.Series({"mean_ex": x.ex.mean(), "n": len(x), "days": nd, "t_dp": t,
                                            "sp_depth": stats.spearmanr(x.below, x.ex)[0] if len(x) > 5 else np.nan}).round(4)
    # r20 z deciles with day-pooled t
    x = d.dropna(subset=["r20z"]).copy()
    x["b"] = pd.qcut(x["r20z"], 6, labels=False)
    g = x.groupby("b").apply(lambda s: pd.Series({"mean": s.ex.mean(), "n": len(s), "t_dp": dp_t(s)[0], "r20z": s.r20z.mean()}))
    out["r20z_sext"] = g.round(4)
    # pos sext with day pooled t, calm vs agit
    x = d.dropna(subset=["pos"]).copy()
    x["pb"] = pd.qcut(x["pos"], 5, labels=False)
    x["hv"] = x.volpct > 0.5
    out["pos_q_by_vol"] = x.groupby(["hv", "pb"]).apply(lambda s: pd.Series({"mean": s.ex.mean(), "n": len(s), "t_dp": dp_t(s)[0]})).round(4)
    # book's largest days: what preceded
    dd = []
    for coin, wins in data["days"].items():
        for w, t2 in wins.items():
            dd.append(t2.assign(coin=coin, w=w))
    dd = pd.concat(dd)
    br = dd.groupby("day")["book_return"].mean().dropna()
    cr = dd.groupby("day")["coin_return"].mean()
    top = br.nlargest(15).index; bot = br.nsmallest(15).index
    out["book_extremes"] = pd.DataFrame({"top_book": [br[top].mean(), cr.reindex(top).mean()],
                                         "bottom_book": [br[bot].mean(), cr.reindex(bot).mean()]},
                                        index=["book_ret", "coins_ret_same_day"]).round(4)
    return out

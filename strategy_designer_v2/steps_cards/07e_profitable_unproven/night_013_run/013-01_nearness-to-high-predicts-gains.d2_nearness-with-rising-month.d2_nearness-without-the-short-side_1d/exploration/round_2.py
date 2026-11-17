def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rec = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].values; f = b["forecast"].values
            rpr = b.get("debug_info.components.range_pos.last_history_value")
            r3r = b.get("debug_info.components.ret30.last_history_value")
            rpr = rpr.values if rpr is not None else np.full(len(b), np.nan)
            r3r = r3r.values if r3r is not None else np.full(len(b), np.nan)
            vol = b["volume"].values
            vm = pd.Series(vol).rolling(20, min_periods=10).mean().values
            reg = b["regime"].values
            n = len(b)
            for h in [3, 7]:
                for i in range(0, n - h, h):
                    rec.append((c, w, h, f[i], reg[i], cl[i + h] / cl[i] - 1, rpr[i], r3r[i], vol[i] / vm[i] if vm[i] > 0 else np.nan))
    R = pd.DataFrame(rec, columns=["coin", "win", "h", "f", "reg", "r", "rpr", "r3r", "vrel"])
    R["ex"] = R.r - R.groupby(["coin", "h"])["r"].transform("mean")
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["rpr_describe"] = R[R.reg == "trending"].rpr.describe()
    for h in [3, 7]:
        g = R[(R.h == h) & (R.reg == "trending")].copy()
        g["rp_q"] = pd.qcut(g.rpr, 4, labels=False, duplicates="drop")
        g["r3_q"] = pd.qcut(g.r3r, 4, labels=False, duplicates="drop")
        out[f"h{h}_trending_by_rangepos_q"] = g.groupby("rp_q").ex.apply(tt).unstack()
        out[f"h{h}_trending_by_ret30_q"] = g.groupby("r3_q").ex.apply(tt).unstack()
        out[f"h{h}_by_regime"] = R[R.h == h].groupby("reg").ex.apply(tt).unstack()
        g["v_q"] = pd.qcut(g.vrel, 3, labels=False, duplicates="drop")
        out[f"h{h}_trending_by_volrel_q"] = g.groupby("v_q").ex.apply(tt).unstack()
        out[f"h{h}_trending_by_coin_rp_top"] = g[g.rp_q == g.rp_q.max()].groupby("coin").ex.apply(tt).unstack()
    # top days concentration
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return"]].dropna().copy(); dd["coin"] = c; dd["win"] = w
            rows.append(dd)
    D = pd.concat(rows)
    daily = D.groupby(["win", "day"]).book_return.mean()
    tot = daily.sum()
    top = daily.sort_values(ascending=False).head(30)
    out["top30_days_by_window"] = top.groupby(level=0).agg(["count", "sum"]).sort_values("sum", ascending=False).head(10)
    out["share_excl_top30"] = pd.Series({"sum_excl_top30": tot - top.sum(), "sum_excl_bottom30": tot - daily.sort_values().head(30).sum(), "total": tot})
    return out

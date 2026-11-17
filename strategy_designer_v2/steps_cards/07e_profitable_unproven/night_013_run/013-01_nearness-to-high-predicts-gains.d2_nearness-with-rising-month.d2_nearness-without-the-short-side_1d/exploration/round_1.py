def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    allpos = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["pos_prev"] = pos.reindex(dd.index).shift(1)
            dd["coin"] = c; dd["win"] = w
            dd["year"] = dd.index.year
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    mu = D.groupby("coin")["coin_return"].mean()
    D["mu"] = D["coin"].map(mu)
    D["mkt"] = D["pos_prev"] * D["mu"]
    D = D.dropna(subset=["book_return"])
    daily = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    out["book_mean, mkt_part, hold_mean"] = pd.Series({"book": daily.book.mean(), "mkt": daily.mkt.mean(), "timing": daily.book.mean() - daily.mkt.mean(), "hold": daily.hold.mean(), "n_days": len(daily)})
    pc = D.groupby("coin").agg(book=("book_return", "mean"), mkt=("mkt", "mean"), avgpos=("pos_prev", "mean"), hold=("coin_return", "mean"))
    pc["timing"] = pc.book - pc.mkt
    out["by_coin"] = pc
    py = D.groupby("year").agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    out["by_year"] = py
    pw = D.groupby("win").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), avgpos=("pos_prev", "mean"))
    out["by_window"] = pw
    s = daily.book.sort_values(ascending=False)
    out["top_day_share"] = pd.Series({"top10_sum/total": s.head(10).sum() / s.sum(), "top30_sum/total": s.head(30).sum() / s.sum(), "total_sum": s.sum()})
    # horizon analysis on forecast>0 grid
    rec = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].values; f = b["forecast"].values
            rp = b.get("debug_info.components.range_pos.post_pipeline_value")
            r3 = b.get("debug_info.components.ret30.post_pipeline_value")
            n = len(b)
            for h in [1, 3, 7, 14, 30]:
                for i in range(0, n - h, h):
                    rec.append((c, w, h, f[i], cl[i + h] / cl[i] - 1, rp.values[i] if rp is not None else np.nan, r3.values[i] if r3 is not None else np.nan))
    R = pd.DataFrame(rec, columns=["coin", "win", "h", "f", "r", "rp", "r3"])
    R["ex"] = R.r - R.groupby(["coin", "h"])["r"].transform("mean")
    hz = []
    for h, g in R.groupby("h"):
        a = g[g.f > 0].ex; z = g[g.f <= 0].ex
        hz.append({"h": h, "n_on": len(a), "mean_ex_on": a.mean(), "t_on": a.mean() / (a.std() / np.sqrt(len(a))), "mean_ex_off": z.mean(), "t_off": z.mean() / (z.std() / np.sqrt(len(z))), "welch_on_off": stats.ttest_ind(a, z, equal_var=False).statistic})
    out["horizons"] = pd.DataFrame(hz)
    g = R[(R.h == 7) & (R.f > 0)].copy()
    g["rp_on"] = g.rp > 0; g["r3_on"] = g.r3 > 0
    out["h7_by_parts"] = g.groupby(["rp_on", "r3_on"]).ex.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["h7_on_by_coin"] = g.groupby("coin").ex.agg(["count", "mean"])
    return out

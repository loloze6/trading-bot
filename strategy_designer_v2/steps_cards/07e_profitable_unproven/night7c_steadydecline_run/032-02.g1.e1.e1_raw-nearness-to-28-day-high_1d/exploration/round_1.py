def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # coin mean daily return over all windows
    rows = []
    for c in days:
        cr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = cr.mean()
        for w in days[c]:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.set_index("dayk")
            d["alloc_prev"] = alloc.reindex(d.index).values
            d["coin"] = c; d["window"] = w; d["mu"] = mu
            d["year"] = d.index.year
            rows.append(d.reset_index())
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return", "coin_return", "alloc_prev"])
    D["mkt_part"] = D["alloc_prev"] * D["mu"]
    D["timing"] = D["book_return"] - D["mkt_part"]
    D["alloc_x_ret"] = D["alloc_prev"] * D["coin_return"]
    out["decomp_overall"] = pd.Series({
        "book_mean": D["book_return"].mean(), "mkt_part": D["mkt_part"].mean(),
        "timing": D["timing"].mean(), "mean_alloc": D["alloc_prev"].mean(),
        "coin_mean": D["coin_return"].mean(),
        "t_timing": D["timing"].mean() / (D["timing"].std() / np.sqrt(len(D))), "n": len(D)})
    g = D.groupby("coin")
    out["by_coin"] = pd.DataFrame({"book": g["book_return"].mean(), "mkt": g["mkt_part"].mean(),
                                   "timing": g["timing"].mean(), "alloc": g["alloc_prev"].mean(),
                                   "coin": g["coin_return"].mean()})
    g = D.groupby("window")
    out["by_window"] = pd.DataFrame({"book": g["book_return"].mean(), "timing": g["timing"].mean(),
                                     "coin": g["coin_return"].mean(), "alloc": g["alloc_prev"].mean()})
    g = D.groupby("year")
    out["by_year"] = pd.DataFrame({"book": g["book_return"].mean(), "timing": g["timing"].mean(),
                                   "coin": g["coin_return"].mean(), "alloc": g["alloc_prev"].mean(), "n": g.size()})
    # allocation terciles vs next-day coin return (vol-target timing)
    D["aq"] = D.groupby("coin")["alloc_prev"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    g = D.groupby("aq")
    out["alloc_tercile"] = pd.DataFrame({"alloc": g["alloc_prev"].mean(), "coin_ret": g["coin_return"].mean(),
                                         "coin_sd": g["coin_return"].std(), "book": g["book_return"].mean(), "n": g.size()})
    # forecast slope at several horizons, and realised vol
    res = []
    for h in [1, 3, 5, 10, 20]:
        recs = []
        for c in bars:
            allr = []
            for w in bars[c]:
                cl = bars[c][w]["close"].values
                idx = np.arange(0, len(cl) - h, h)
                allr.append(cl[idx + h] / cl[idx] - 1)
            mu = np.concatenate(allr).mean()
            for w in bars[c]:
                b = bars[c][w]; cl = b["close"].values
                f = b["debug_info.components.high_prox.post_pipeline_value"].values
                rv = b["sizing_realised_vol"].values
                idx = np.arange(0, len(cl) - h, h)
                for i in idx:
                    recs.append((f[i], rv[i], cl[i + h] / cl[i] - 1 - mu))
        R = pd.DataFrame(recs, columns=["f", "rv", "x"]).dropna()
        s1 = stats.linregress(R["f"], R["x"])
        s2 = stats.linregress(R["rv"], R["x"])
        q = pd.qcut(R["f"].rank(method="first"), 3, labels=False)
        res.append({"h": h, "n": len(R), "slope_f": s1.slope, "t_f": s1.slope / s1.stderr,
                    "top_minus_bot": R["x"][q == 2].mean() - R["x"][q == 0].mean(),
                    "slope_rv": s2.slope, "t_rv": s2.slope / s2.stderr})
    out["horizon_slopes"] = pd.DataFrame(res)
    return out

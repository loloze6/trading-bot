def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for c, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.copy()
            b["w"] = w; b["coin"] = c
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["r60"] = b["close"] / b["close"].shift(60) - 1
            b["r5"] = b["close"] / b["close"].shift(5) - 1
            dr = b["close"].pct_change()
            b["vol30"] = dr.rolling(30).std()
            b["vol90"] = dr.rolling(90, min_periods=60).std()
            rng = (b["high"] - b["low"])
            b["rngmult"] = rng / rng.shift(1).rolling(14).mean()
            b["clo"] = (b["high"] - b["close"]) / rng.replace(0, np.nan)
            b["raw"] = b["debug_info.components.wide_low_close.last_history_value"]
            b["pp"] = b["debug_info.components.wide_low_close.post_pipeline_value"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"] * b["ret1"]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B.groupby("coin")["ret1"].transform("mean")
    B["ex"] = B["ret1"] - drift
    B = B.dropna(subset=["ret1"])
    out["alloc_stats"] = B["alloc"].describe()
    out["share_alloc_gt0"] = float((B["alloc"] > 0.01).mean())
    out["pp_stats"] = B["pp"].describe()
    B["rawq"] = B.groupby("coin")["raw"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    g = B.groupby("rawq")
    out["by_raw_quintile"] = pd.DataFrame({"n": g.size(), "mean_ex%": g["ex"].mean()*100,
        "t": g["ex"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))),
        "mean_alloc": g["alloc"].mean(), "mean_gain%": g["gain"].mean()*100, "rngmult": g["rngmult"].mean(), "clo": g["clo"].mean()})
    # trend
    B["trend"] = pd.cut(B["r60"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    B["agit"] = np.where(B["vol30"].isna(), "na", np.where(B["vol30"] > B["vol90"], "agit", "calm"))
    B["top"] = B["rawq"] == 4
    g = B.groupby(["trend", "top"], observed=True)
    out["trend_x_top"] = pd.DataFrame({"n": g.size(), "mean_ex%": g["ex"].mean()*100, "mean_ret%": g["ret1"].mean()*100,
        "t": g["ex"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), "mean_gain%": g["gain"].mean()*100})
    g = B.groupby(["agit", "top"])
    out["agit_x_top"] = pd.DataFrame({"n": g.size(), "mean_ex%": g["ex"].mean()*100,
        "t": g["ex"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), "mean_gain%": g["gain"].mean()*100})
    # r5 down vs top
    B["r5neg"] = B["r5"] < 0
    g = B.groupby(["r5neg", "top"])
    out["r5neg_x_top"] = pd.DataFrame({"n": g.size(), "mean_ex%": g["ex"].mean()*100,
        "t": g["ex"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))})
    # book daily
    drows = []
    for c, wd in data["days"].items():
        for w, d in wd.items():
            d = d.copy(); d["w"] = w; d["coin"] = c; drows.append(d)
    D = pd.concat(drows)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["wn"] = bk["w"].str[1:].astype(int)
    bk = bk.sort_values(["wn", "day"])
    v = (1 + bk["book_return"]).cumprod(); h = (1 + bk["coin_return"]).cumprod()
    bk["dd"] = v / v.cummax() - 1; bk["hdd"] = h / h.cummax() - 1
    out["book_vs_hold_by_window"] = bk.groupby("wn").agg(book_tot=("book_return", lambda s: (1+s).prod()-1),
        hold_tot=("coin_return", lambda s: (1+s).prod()-1), min_dd=("dd", "min"), hold_min_dd=("hdd", "min"),
        corr=("book_return", lambda s: np.nan))
    out["corr_book_hold"] = float(bk["book_return"].corr(bk["coin_return"]))
    out["beta_book_hold"] = float(np.polyfit(bk["coin_return"], bk["book_return"], 1)[0])
    out["deepest_dd"] = float(bk["dd"].min()); out["hold_deepest_dd"] = float(bk["hdd"].min())
    # gain split
    out["gain_by_trend"] = B.groupby("trend", observed=True).agg(n=("gain", "size"), gain=("gain", "mean"), ret=("ret1", "mean"), alloc=("alloc", "mean"))
    return out

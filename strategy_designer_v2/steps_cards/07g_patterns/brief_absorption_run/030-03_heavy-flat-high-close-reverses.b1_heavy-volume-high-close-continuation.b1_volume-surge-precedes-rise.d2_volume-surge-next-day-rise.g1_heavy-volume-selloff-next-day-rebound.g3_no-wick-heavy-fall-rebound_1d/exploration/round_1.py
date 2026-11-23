def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            o = b["open"].astype(float); v = b["volume"].astype(float)
            d = pd.DataFrame()
            d["coin"] = coin; d["win"] = w
            d["ret1"] = c / c.shift(1) - 1
            d["ret3p"] = c / c.shift(3) - 1
            d["vr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            rng = (h - l).replace(0, np.nan)
            d["fall_left"] = (h - c) / rng
            d["range_rel"] = rng / c
            r = c.pct_change()
            d["vol20"] = r.rolling(20, min_periods=20).std()
            d["volratio"] = d["vol20"] / d["vol20"].rolling(60, min_periods=30).mean()
            d["n1"] = c.shift(-1) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            d["n5"] = c.shift(-5) / c - 1
            d["fc"] = b["forecast"].astype(float)
            d["pos"] = np.arange(len(b))
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["n1"].transform("mean")
    D["x1"] = D["n1"] - mu
    D["x3"] = D["n3"] - D.groupby("coin")["n1"].transform("mean") * 3
    def summ(g, col="x1"):
        s = g[col].dropna()
        n = len(s)
        return pd.Series({"n": n, "mean%": s.mean() * 100 if n else np.nan,
                          "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    D["heavy"] = D["vr"] >= 1
    D["down"] = D["ret1"] < 0
    D["rq"] = D.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["next1_by_ret_quintile_x_heavy"] = D.dropna(subset=["rq", "vr"]).groupby(["rq", "heavy"]).apply(summ)
    dh = D[D.down & D.heavy].copy()
    dh["flq"] = pd.qcut(dh["fall_left"], 5, labels=False, duplicates="drop")
    out["downheavy_next1_by_fall_left_q"] = dh.groupby("flq").apply(summ)
    dl = D[D.down & (D.vr < 1)].copy()
    dl["flq"] = pd.qcut(dl["fall_left"], 5, labels=False, duplicates="drop")
    out["downlight_next1_by_fall_left_q"] = dl.groupby("flq").apply(summ)
    uh = D[(~D.down) & D.heavy & D.ret1.notna()].copy()
    uh["flq"] = pd.qcut(uh["fall_left"], 5, labels=False, duplicates="drop")
    out["upheavy_next1_by_fall_left_q"] = uh.groupby("flq").apply(summ)
    # volume ratio grading on down days
    dd = D[D.down & D.vr.notna()].copy()
    dd["vq"] = pd.qcut(dd["vr"], 5, labels=False, duplicates="drop")
    out["down_next1_by_vr_q"] = dd.groupby("vq").apply(summ)
    # range relative to vol20 on down days
    dd["rr"] = dd["range_rel"] / dd["vol20"]
    dd["rrq"] = pd.qcut(dd["rr"], 5, labels=False, duplicates="drop")
    out["down_next1_by_range_over_vol_q"] = dd.groupby("rrq").apply(summ)
    # all days by volatility ratio
    a = D.dropna(subset=["volratio"]).copy()
    a["vlq"] = pd.qcut(a["volratio"], 5, labels=False, duplicates="drop")
    out["all_next1_by_volratio_q"] = a.groupby("vlq").apply(summ)
    out["all_next1_by_weekday"] = D.groupby("wd").apply(summ)
    out["signal_next1_by_weekday"] = D[D.fc > 0].groupby("wd").apply(summ)
    out["signal_by_coin"] = D[D.fc > 0].groupby("coin").apply(summ)
    out["signal_by_year"] = D[D.fc > 0].groupby("year").apply(summ)
    out["signal_3day_excess"] = summ(D[D.fc > 0], "x3")
    # 3-day prior return on down heavy days
    dh["p3q"] = pd.qcut(dh["ret3p"], 5, labels=False, duplicates="drop")
    out["downheavy_next1_by_prior3d_q"] = dh.groupby("p3q").apply(summ)
    # book: daily returns, top/bottom days
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; bd.append(t)
    B = pd.concat(bd, ignore_index=True)
    br = B["book_return"].dropna()
    srt = br.sort_values()
    out["book_share_of_sum_top/bottom"] = pd.Series({
        "sum_all%": br.sum() * 100, "top20_sum%": srt.tail(20).sum() * 100,
        "bottom20_sum%": srt.head(20).sum() * 100, "nonzero_days": (br != 0).sum()})
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_by_duration"] = T.groupby(T["dur_d"].clip(upper=5).round()).agg(
        n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"))
    return out

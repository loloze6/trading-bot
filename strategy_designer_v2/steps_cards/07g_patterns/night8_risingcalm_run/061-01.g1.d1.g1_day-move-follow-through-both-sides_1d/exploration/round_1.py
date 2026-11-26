def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            z = r1 / vol30
            vol5 = r1.rolling(5).std()
            ret20 = c / c.shift(20) - 1
            ret5p = c / c.shift(5) - 1
            rng = (b["high"] - b["low"]) / c
            rngz = rng / rng.rolling(30, min_periods=20).mean()
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            volz = b["volume"] / b["volume"].rolling(30, min_periods=20).mean()
            volrank = vol30 / vol30.expanding(min_periods=30).median()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z": z, "fc": b["forecast"], "rngz": rngz, "clv": clv, "volz": volz,
                "ret20": ret20, "ret5p": ret5p, "volrank": volrank,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f2", "f5", "f10"]:
        d[h + "x"] = d[h] - d.groupby("coin")[h].transform("mean")
    out = {}

    def tday(sub, col):
        s = sub.dropna(subset=[col]).groupby("day")[col].sum()
        n = len(sub.dropna(subset=[col]))
        if len(s) < 5: return (np.nan, np.nan, n)
        m = sub[col].mean()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if s.std() > 0 else np.nan
        return (m, t, n)

    g5 = d[d.pos % 5 == 0].dropna(subset=["z", "f5x"]).copy()
    g5["zq"] = pd.qcut(g5["z"], 10, labels=False)
    out["f5x_by_z_decile"] = g5.groupby("zq").agg(zmean=("z", "mean"), f5x=("f5x", "mean"), n=("f5x", "size"))
    g1 = d.dropna(subset=["z", "f1x"]).copy()
    g1["zq"] = pd.qcut(g1["z"], 10, labels=False)
    out["f1x_by_z_decile"] = g1.groupby("zq").agg(zmean=("z", "mean"), f1x=("f1x", "mean"), n=("f1x", "size"))
    g2 = d[d.pos % 2 == 0].dropna(subset=["z", "f2x"]).copy()
    g2["zq"] = pd.qcut(g2["z"], 10, labels=False)
    out["f2x_by_z_decile"] = g2.groupby("zq").agg(zmean=("z", "mean"), f2x=("f2x", "mean"), n=("f2x", "size"))

    # signed follow-through by calm/agitated proxy and trend proxy
    g5["dir"] = np.sign(g5["z"]) * g5["f5x"]
    g5["calm"] = np.where(g5["volrank"] <= 1, "calm", "agit")
    g5["trend"] = pd.cut(g5["ret20"], [-9, -0.07, 0.07, 9], labels=["fall", "chop", "rise"])
    big = g5[g5["z"].abs() > 1.5]
    res = {}
    for k, sub in big.groupby(["calm", "trend"]):
        res[str(k)] = tday(sub, "dir")
    out["big_z_dir_f5_by_profile_proxy"] = pd.DataFrame(res, index=["mean", "t_day", "n"]).T
    res = {}
    for k, sub in g5.groupby(np.sign(g5["z"])):
        for kk, s2 in sub.groupby(pd.cut(sub["z"].abs(), [0, 1, 2, 9])):
            res[f"sign{k}_abs{kk}"] = tday(s2, "f5x")
    out["f5x_by_sign_and_size"] = pd.DataFrame(res, index=["mean", "t_day", "n"]).T

    # close location and range
    g1["clvq"] = pd.cut(g1["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    res = {}
    for k, sub in g1.groupby("clvq"):
        res[str(k)] = tday(sub, "f1x")
    out["f1x_by_close_location"] = pd.DataFrame(res, index=["mean", "t_day", "n"]).T
    g2["clvq"] = pd.cut(g2["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    res = {}
    for k, sub in g2.groupby("clvq"):
        res[str(k)] = tday(sub, "f2x")
    out["f2x_by_close_location"] = pd.DataFrame(res, index=["mean", "t_day", "n"]).T
    # volume shock
    g1["volq"] = pd.qcut(g1["volz"], 5, labels=False)
    g1["sz1"] = np.sign(g1["z"]) * g1["f1x"]
    res = {}
    for k, sub in g1.groupby("volq"):
        res[str(k)] = tday(sub, "sz1") + tday(sub, "f1x")[:2]
    out["f1_dir_and_raw_by_volume_quintile"] = pd.DataFrame(res, index=["dir_mean", "dir_t", "n", "raw_mean", "raw_t"]).T
    # weekday
    res = {}
    for k, sub in g1.groupby("wd"):
        res[k] = tday(sub, "f1x")
    out["f1x_by_weekday_of_signal_bar"] = pd.DataFrame(res, index=["mean", "t_day", "n"]).T
    # 5-day past return reversal
    g5["p5q"] = pd.qcut(g5["ret5p"] / (g5["volrank"]), 5, labels=False)
    res = {}
    for k, sub in g5.dropna(subset=["ret5p"]).groupby(pd.qcut(g5["ret5p"].dropna(), 5, labels=False)):
        res[k] = tday(sub, "f5x")
    out["f5x_by_past5_quintile"] = pd.DataFrame(res, index=["mean", "t_day", "n"]).T
    # book by year/coin
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w
            bk.append(x)
    bk = pd.concat(bk)
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_coin"] = bk.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book_by_window"] = bk.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out

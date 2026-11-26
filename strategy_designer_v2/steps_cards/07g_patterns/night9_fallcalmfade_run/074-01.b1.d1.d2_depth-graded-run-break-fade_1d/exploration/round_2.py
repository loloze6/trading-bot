def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float)
            r = c.pct_change()
            run = np.zeros(len(c)); cnt = 0
            for i in range(len(c)):
                run[i] = cnt
                cnt = cnt + 1 if r.iloc[i] < 0 else 0
            sd = r.rolling(30).std()
            vol_pct = sd.rolling(365, min_periods=200).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            d = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]), "r": r,
                              "nxt": c.shift(-1) / c - 1, "nxt2": c.shift(-2) / c - 1, "nxt3": c.shift(-3) / c - 1,
                              "run": run, "ret60": c / c.shift(60) - 1, "ret20": c / c.shift(20) - 1,
                              "ret5z": (c / c.shift(5) - 1) / sd, "upz": r / sd, "vp": vol_pct,
                              "volz": v / v.rolling(30).mean(), "rngz": ((h - l) / c) / sd,
                              "br": b["book_value"] if "book_value" in b else np.nan})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["nxt", "nxt2", "nxt3"]:
        D["ex_" + k] = D[k] - D.groupby("coin")[k].transform("mean")
    D["trend"] = np.where(D.ret60 > 0.10, "rising", np.where(D.ret60 < -0.10, "falling", np.where(D.ret60.notna(), "choppy", None)))
    D["agit"] = np.where(D.vp > 0.5, "agitated", np.where(D.vp.notna(), "calm", None))
    D["day"] = D.ts.dt.floor("D")
    def tday(x, col="ex_nxt"):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t": m / se})
    out = {}
    brk = D[(D.r > 0) & (D.run >= 1)].copy()
    out["upafterdown_by_profile"] = brk.groupby(["trend", "agit"]).apply(tday)
    ch = brk[brk.trend == "choppy"].copy()
    ch["runb"] = pd.cut(ch.run, [0, 1, 2, 30], labels=["1", "2", "3+"])
    out["choppy_by_run"] = ch.groupby("runb").apply(tday)
    ch["r5q"] = pd.qcut(ch.ret5z, 3, labels=["deep", "mid", "shallow"])
    out["choppy_by_5dfall"] = ch.groupby("r5q").apply(tday)
    f = brk[brk.trend == "falling"].copy()
    f["r5q"] = pd.qcut(f.ret5z, 3, labels=["deep", "mid", "shallow"])
    out["falling_by_5dfall"] = f.groupby("r5q").apply(tday)
    f["volq"] = pd.qcut(f.volz, 3, labels=["lowvol", "mid", "highvol"])
    out["falling_by_volume"] = f.groupby("volq").apply(tday)
    f["r20q"] = pd.qcut(f.ret20, 3, labels=["deep20", "mid", "shallow20"])
    out["falling_by_20d"] = f.groupby("r20q").apply(tday)
    out["falling_horizons"] = pd.DataFrame({k: tday(f, "ex_" + k) for k in ["nxt", "nxt2", "nxt3"]}).T
    # falling: big down days rebound (all down days)
    fd = D[(D.trend == "falling") & (D.r < 0)].copy()
    fd["q"] = pd.qcut(fd.upz, 3, labels=["bigdown", "mid", "smalldown"])
    out["falling_downdays_by_size"] = fd.groupby("q").apply(tday)
    # book largest days
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dl.append(dd.assign(coin=coin, w=w))
    Dy = pd.concat(dl, ignore_index=True)
    bk = Dy.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk = bk[bk.book_return != 0]
    q = bk.book_return.quantile([0.05, 0.95])
    out["book_tail_days"] = pd.DataFrame({
        "n": [len(bk[bk.book_return <= q.iloc[0]]), len(bk[bk.book_return >= q.iloc[1]])],
        "book_mean": [bk[bk.book_return <= q.iloc[0]].book_return.mean(), bk[bk.book_return >= q.iloc[1]].book_return.mean()],
        "coin_mean": [bk[bk.book_return <= q.iloc[0]].coin_return.mean(), bk[bk.book_return >= q.iloc[1]].coin_return.mean()]},
        index=["worst5", "best5"])
    out["book_by_window"] = Dy.groupby("w")["book_return"].agg(["mean", "std", "count"])
    return out

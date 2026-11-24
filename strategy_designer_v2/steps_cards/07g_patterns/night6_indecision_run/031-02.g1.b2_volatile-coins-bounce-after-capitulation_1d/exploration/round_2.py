def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r,
                "vol20": r.rolling(20).std(),
                "loc": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / b["open"],
                "body": (c - b["open"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "r5p": c / c.shift(5) - 1,
                "r10p": c / c.shift(10) - 1,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
            })
            d["z"] = d["r"] / d["vol20"]
            d["rngz"] = d["rng"] / d["rng"].rolling(20).mean()
            d["z5"] = d["r5p"] / (d["vol20"] * np.sqrt(5))
            d["z10"] = d["r10p"] / (d["vol20"] * np.sqrt(10))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    mu3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(mu3)

    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": s.day.nunique(), "mean": np.nan, "t": np.nan})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": s.day.nunique(), "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    # wide flat after run: continuation robustness
    fl = D[(D.z5.abs() > 1) & (D["body"].abs() < 0.2)].copy()
    fl["xs"] = np.sign(fl["r5p"]) * fl["x1"]          # continuation sign
    fl["xs3"] = np.sign(fl["r5p"]) * fl["x3"]
    wide = fl[fl.rngz > 1.074]
    out["wideflat_cont_by_coin"] = wide.groupby("coin").apply(lambda s: ct(s, "xs"))
    out["wideflat_cont_by_runside"] = wide.groupby(np.sign(wide["r5p"])).apply(lambda s: ct(s, "xs"))
    out["wideflat_cont_by_year"] = wide.groupby(wide.day.dt.year).apply(lambda s: ct(s, "xs"))
    out["flat_cont3_grid_by_rngz"] = fl[fl.pos % 3 == 0].groupby(pd.qcut(fl[fl.pos % 3 == 0]["rngz"], 3)).apply(lambda s: ct(s, "xs3"))
    # control: all days after run, continuation by rngz (not flat)
    ar = D[D.z5.abs() > 1].copy()
    ar["xs"] = np.sign(ar["r5p"]) * ar["x1"]
    out["afterrun_all_cont_by_rngz_q5"] = ar.groupby(pd.qcut(ar["rngz"], 5)).apply(lambda s: ct(s, "xs"))
    # down days: graded by prior 10d fall
    dn = D[D.z <= -1].copy()
    out["down_z<=-1_x1_by_z10_q4"] = dn.groupby(pd.qcut(dn["z10"], 4)).apply(lambda s: ct(s, "x1"))
    out["down_z<=-1_x1_by_loc"] = dn.groupby(pd.cut(dn["loc"], [-0.01, 0.25, 0.5, 1.01])).apply(lambda s: ct(s, "x1"))
    out["all_x1_by_z5_q6"] = D.groupby(pd.qcut(D["z5"], 6)).apply(lambda s: ct(s, "x1"))
    cap = D[(D.z <= -2) & (D["loc"] <= 0.25)]
    out["cap_x1_by_z10_q3"] = cap.groupby(pd.qcut(cap["z10"], 3)).apply(lambda s: ct(s, "x1"))
    out["cap_by_halfperiod_prior5d"] = cap.groupby([cap.day.dt.year >= 2022, pd.qcut(cap["r5p"], 3, labels=["deep", "mid", "shallow"])]).apply(lambda s: ct(s, "x1"))
    # book: days in position, distribution
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin))
    DD = pd.concat(dd)
    br = DD["book_return"].dropna()
    out["book_ret_quantiles"] = br[br != 0].describe()
    out["book_top10_share"] = float(br.nlargest(10).sum() / br.sum())
    return out

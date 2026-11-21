def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin usual move & drift over 5 bars, non-overlapping
        f5 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            f5 += list(c[idx + H] / c[idx] - 1)
        f5 = np.array(f5); drift = f5.mean(); sd = f5.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            feat = pd.DataFrame({
                "ret5": c / c.shift(5) - 1,
                "ret20": c / c.shift(20) - 1,
                "ret60": c / c.shift(60) - 1,
                "vol20": r1.rolling(20).std(),
                "dist_hi60": c / hi.rolling(60).max() - 1,
                "dist_lo60": c / lo.rolling(60).min() - 1,
                "range1": (hi - lo) / c,
                "clv": (c - lo) / (hi - lo).replace(0, np.nan),
                "ret1": r1,
                "fc": b["forecast"],
                "vol_ratio": b["volume"] / b["volume"].rolling(20).mean(),
            })
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(c) - H, H)
            d = feat.iloc[idx].copy()
            d["y"] = (fwd.iloc[idx] - drift) / sd
            d["yraw"] = fwd.iloc[idx] - drift
            d["coin"] = coin; d["win"] = w
            rows.append(d)
            # daily: next-day return by weekday
            ts = pd.to_datetime(b["timestamp"])
            dd = pd.DataFrame({"wd": ts.dt.dayofweek, "nxt": c.shift(-1) / c - 1, "coin": coin})
            daily.append(dd)
    D = pd.concat(rows).dropna(subset=["y"])
    out = {}
    out["n_cases"] = len(D)
    res = []
    for f in ["ret5", "ret20", "ret60", "vol20", "dist_hi60", "dist_lo60", "range1", "clv", "ret1", "fc", "vol_ratio"]:
        x = D[[f, "y", "coin"]].dropna()
        x["q"] = x.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        g = x.groupby("q")["y"].agg(["mean", "count"])
        top = x[x.q == 4]["y"]; bot = x[x.q == 0]["y"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        rho = stats.spearmanr(x[f], x["y"]).correlation
        res.append([f, len(x)] + list(g["mean"].round(3)) + [round(t, 2), round(rho, 3)])
    out["quintile_strength"] = pd.DataFrame(res, columns=["feat", "n", "q1", "q2", "q3", "q4", "q5", "t_q5_q1", "spearman"])
    # interaction: ret20 within vol20 halves
    x = D[["ret20", "vol20", "y", "coin"]].dropna()
    x["vh"] = x.groupby("coin")["vol20"].transform(lambda s: s > s.median())
    x["rq"] = x.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["ret20_by_vol"] = x.groupby(["vh", "rq"])["y"].agg(["mean", "count"]).round(3)
    # per coin spearman for top features
    pc = []
    for coin, g in D.groupby("coin"):
        r = {"coin": coin}
        for f in ["ret5", "ret20", "ret60", "dist_hi60", "vol20"]:
            gg = g[[f, "y"]].dropna()
            r[f] = round(stats.spearmanr(gg[f], gg["y"]).correlation, 3)
        pc.append(r)
    out["per_coin_spearman"] = pd.DataFrame(pc)
    DD = pd.concat(daily).dropna()
    DD["nxt_dm"] = DD["nxt"] - DD.groupby("coin")["nxt"].transform("mean")
    out["weekday_next_day"] = DD.groupby("wd")["nxt_dm"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))]).round(5)
    # book: days
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, win=w))
    B = pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_coin"] = B.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    return out

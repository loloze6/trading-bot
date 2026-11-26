def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            nxt = c.shift(-1) / c - 1
            r1 = c / c.shift(1) - 1
            rng = (h - l) / c
            cloc = (c - l) / (h - l).replace(0, np.nan)
            width = (h - l) / (h - l).rolling(20, min_periods=10).mean()
            r5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20, min_periods=10).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "nxt": nxt, "r1": r1, "cloc": cloc,
                "width": width, "r5": r5, "vol20": vol20, "rng": rng,
                "inprof": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "day": ts.dt.floor("D"),
                "body": (c - o) / (h - l).replace(0, np.nan),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["usual"] = d["coin"].map(d.groupby("coin")["nxt"].std())
    d["exs"] = d["ex"] / d["usual"]
    d = d.dropna(subset=["nxt"])

    def summ(g):
        x = g["exs"].dropna()
        # day-clustered t
        dd = g.groupby("day")["ex"].sum()
        n = len(g)
        t = dd.sum() / (np.sqrt((dd**2).sum() - dd.sum()**2/len(dd)) if len(dd) > 1 else np.nan)
        return pd.Series({"n": n, "days": g["day"].nunique(),
                          "mean_ex_pct": 100*g["ex"].mean(),
                          "strength": x.mean(),
                          "t_day": t})
    out = {}
    d["cloc_q"] = pd.cut(d["cloc"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["cloc_by_profile"] = d.groupby(["inprof", "cloc_q"]).apply(summ)
    d["r1_q"] = pd.qcut(d["r1"], 5)
    out["r1q_by_profile"] = d.groupby(["inprof", "r1_q"]).apply(summ)
    d["w_q"] = pd.qcut(d["width"], 5)
    out["width_q_all"] = d.groupby(["w_q"]).apply(summ)
    hi = d[d["cloc"] > 0.5]
    out["highclose_widthq_by_profile"] = hi.groupby(["inprof", pd.qcut(hi["width"], 4)]).apply(summ)
    d["vol_q"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["volq_r1sign"] = d.groupby(["vol_q", np.sign(d["r1"])]).apply(summ)
    out["weekday"] = d.groupby("wd").apply(summ)
    out["r5_q"] = d.groupby(pd.qcut(d["r5"], 5)).apply(summ)
    out["body_q"] = d.groupby(pd.qcut(d["body"], 5)).apply(summ)
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; days.append(x)
    D = pd.concat(days)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "std", "count"])
    out["book_corr_coin"] = float(bk.corr().iloc[0, 1])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 20: continue
            c = b["close"].values
            n = len(b)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            loc = ((b["close"] - b["low"]) / rng).values
            ret5 = pd.Series(c).pct_change(5).values
            ret1 = pd.Series(c).pct_change(1).values
            vol30 = pd.Series(c).pct_change().rolling(30, min_periods=15).std().values
            ts = pd.to_datetime(b["timestamp"])
            inprof = (b["regime"] != "chop").values
            for h in (2, 5):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, day=ts[i].normalize(),
                                     wd=ts[i].dayofweek, year=ts[i].year,
                                     loc=loc[i], ret5=ret5[i], ret1=ret1[i], vol=vol30[i],
                                     inprof=inprof[i], regime=b["regime"].iloc[i],
                                     fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    # drift per coin and horizon over all windows
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["unus"] = d["fwd"] - d["drift"]
    out = {}
    def tstat(s, days):
        g = pd.DataFrame({"v": s.values, "d": days.values}).groupby("d")["v"].sum()
        # per-day summed; t of mean per case approx
        m = s.mean(); se = np.sqrt((g - g.mean()*0).pow(2).sum()) / len(s) if len(s) else np.nan
        return m, (m / se if se else np.nan), g.shape[0]
    def summ(sub, key):
        res = []
        for k, g in sub.groupby(key):
            m, t, nd = tstat(g["unus"], g["day"])
            res.append(dict(group=str(k), n=len(g), days=nd, mean_unus=round(m, 4), t=round(t, 2)))
        return pd.DataFrame(res)
    d["locb"] = pd.cut(d["loc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1", "q2", "q3", "q4"])
    d["r5s"] = np.where(d["ret5"] < 0, "r5neg", "r5pos")
    d["prof"] = np.where(d["inprof"], "chopagi", "other")
    for h in (2, 5):
        x = d[(d.h == h)].dropna(subset=["loc", "ret5"])
        x = x.assign(key=x["prof"] + "_" + x["r5s"] + "_" + x["locb"].astype(str))
        out[f"h{h} prof x ret5 x loc"] = summ(x, "key")
    x = d[(d.h == 5)].dropna(subset=["ret5"])
    x = x.assign(r5q=x.groupby("prof")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop")))
    out["h5 prof x ret5 quintile"] = summ(x.assign(key=x["prof"] + "_" + x["r5q"].astype(str)), "key")
    x = d[(d.h == 2)].dropna(subset=["ret1"])
    x = x.assign(r1q=x.groupby("prof")["ret1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop")))
    out["h2 prof x ret1 quintile"] = summ(x.assign(key=x["prof"] + "_" + x["r1q"].astype(str)), "key")
    x = d[(d.h == 5) & d.inprof]
    out["h5 chopagi weekday"] = summ(x, "wd")
    out["h5 chopagi year"] = summ(x, "year")
    out["share in profile"] = float(d[d.h == 5]["inprof"].mean())
    # book: largest gains/losses days
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            br.append(dd.assign(coin=coin, w=w))
    br = pd.concat(br)
    book = br.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book by window"] = book.groupby(level=0).agg(["count", "mean", "std", "sum"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin, w=w))
    tr = pd.concat(tr)
    tr["absf"] = tr["entry_forecast"].abs()
    tr["fq"] = pd.qcut(tr["absf"], 3, labels=False, duplicates="drop")
    out["trades by entry forecast tercile"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out

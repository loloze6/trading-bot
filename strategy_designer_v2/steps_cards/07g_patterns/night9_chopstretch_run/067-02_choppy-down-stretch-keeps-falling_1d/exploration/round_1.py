def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            stretch = (c / sma - 1) / sd
            r1 = r
            r5p = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            wd = ts.dt.weekday
            chop = (b["regime"] == "unknown")
            sd_rank = sd.rolling(60, min_periods=30).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            for h in (10, 3):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, stretch=stretch[i], chop=chop[i],
                                     fwd=fwd[i], r1=r1[i], r5p=r5p[i], sdr=sd_rank[i],
                                     year=ts[i].year))
            nxt = r.shift(-1)
            for i in range(len(b) - 1):
                daily.append(dict(coin=coin, w=w, wd=wd[i], chop=chop[i], r=r[i], nxt=nxt[i],
                                  stretch=stretch[i], sdr=sd_rank[i]))
    g = pd.DataFrame(rows)
    d = pd.DataFrame(daily).dropna()
    out = {}
    for h in (10, 3):
        gh = g[g.h == h].dropna(subset=["stretch", "fwd"]).copy()
        gh["drift"] = gh.groupby("coin")["fwd"].transform("mean")
        gh["ex"] = gh["fwd"] - gh["drift"]
        gh["q"] = pd.qcut(gh["stretch"], 5, labels=False)
        t = gh.groupby(["chop", "q"])["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
        t.columns = ["mean_ex", "n", "t"]
        out[f"h{h}_stretch_quintile_by_chop(True=choppy)"] = t
        for ch in (True, False):
            s = gh[gh.chop == ch]
            sl = stats.linregress(s["stretch"], s["ex"])
            out[f"h{h}_slope_chop{ch}"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(s)}"
        # past 5-day return quintile
        gh2 = gh.dropna(subset=["r5p"]).copy()
        gh2["q5"] = pd.qcut(gh2["r5p"], 5, labels=False)
        t2 = gh2.groupby(["chop", "q5"])["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
        t2.columns = ["mean_ex", "n", "t"]
        out[f"h{h}_past5d_quintile_by_chop"] = t2
        gh3 = gh.dropna(subset=["sdr"]).copy()
        gh3["qs"] = pd.cut(gh3["sdr"], [-0.01, 0.33, 0.66, 1.0], labels=False)
        gh3["sq"] = np.sign(gh3["stretch"])
        t3 = gh3.groupby(["qs", "sq"])["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
        t3.columns = ["mean_ex", "n", "t"]
        out[f"h{h}_volrank_x_stretchsign"] = t3
    # daily: next-day return after large daily moves
    d["rz"] = d.groupby("coin")["r"].transform(lambda x: (x - x.mean()) / x.std())
    d["rq"] = pd.qcut(d["rz"], 10, labels=False)
    t4 = d.groupby(["chop", "rq"])["nxt"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    t4.columns = ["mean_next", "n", "t"]
    out["next_day_after_day_decile"] = t4
    t5 = d.groupby("wd")["r"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    t5.columns = ["mean", "n", "t"]
    out["weekday_return"] = t5
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, w=w))
    bk = pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_window"] = bk.groupby("w")["book_return"].agg(["mean", "count"])
    out["book_by_coin"] = bk.groupby("coin")["book_return"].agg(["mean", "std"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        tr = pd.concat(tr)
        out["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count", "median"])
    return out

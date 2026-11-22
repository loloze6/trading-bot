def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < 40: continue
            r30 = c / c.shift(30) - 1
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min()
            nmr = (c - c.shift(30)).abs() / (hh - ll)
            mid = (hh + ll) / 2
            pos = (c - mid) / (hh - ll)  # -0.5..0.5
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            r5p = c / c.shift(5) - 1
            fwd = c.shift(-H) / c - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, r30=r30[i], nmr=nmr[i], pos=pos[i], r1=r1[i],
                                 z1=r1[i] / vol20[i] if vol20[i] > 0 else np.nan,
                                 r5p=r5p[i], vol=vol20[i], fwd=fwd[i],
                                 wd=pd.Timestamp(b["timestamp"][i]).weekday(),
                                 year=pd.Timestamp(b["timestamp"][i]).year))
            daily.append(pd.DataFrame(dict(coin=coin, w=w, r=r1.values[1:],
                                           wd=pd.to_datetime(b["timestamp"]).dt.weekday.values[1:],
                                           alloc=b["postRebalance_current_allocation"].shift(1).values[1:])))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    usual = df.groupby("coin")["fwd"].std()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    df["exs"] = df["ex"] / df["coin"].map(usual)
    df = df.dropna(subset=["ex"])
    out = {}
    def tab(g, col="exs"):
        a = df.dropna(subset=[g]) if isinstance(g, str) else df
        return a
    # 1 r30 quintiles by regime
    d = df.dropna(subset=["r30", "nmr"]).copy()
    d["trend"] = np.where(d["nmr"] >= 0.5, "trend", "flat")
    d["q"] = d.groupby("coin")["r30"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["r30 quintile x regime: mean exs, n"] = d.groupby(["trend", "q"])["exs"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # 2 range position in flat
    d["pq"] = pd.cut(d["pos"], [-0.6, -0.3, -0.1, 0.1, 0.3, 0.6])
    out["range pos x regime"] = d.groupby(["trend", "pq"])["exs"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    cor = {}
    for t in ["trend", "flat"]:
        s = d[d.trend == t].dropna(subset=["pos"])
        r, p = stats.pearsonr(s["pos"], s["exs"]); cor[t + "_pos"] = (r, len(s), r*np.sqrt((len(s)-2)/(1-r*r)))
        r, p = stats.pearsonr(s["r30"], s["exs"]); cor[t + "_r30"] = (r, len(s), r*np.sqrt((len(s)-2)/(1-r*r)))
    out["corr (r,n,t)"] = pd.DataFrame(cor, index=["r", "n", "t"]).T
    # 3 last-day shock z
    e = df.dropna(subset=["z1"]).copy()
    e["zq"] = pd.cut(e["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["1d shock z -> next5"] = e.groupby("zq")["exs"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    e = df.dropna(subset=["r5p", "vol"]).copy()
    e["z5"] = e["r5p"] / (e["vol"] * np.sqrt(5))
    e["z5q"] = pd.cut(e["z5"], [-99, -2, -1, 0, 1, 2, 99])
    out["5d past z -> next5"] = e.groupby("z5q")["exs"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    e["vq"] = e.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["vol tercile -> next5 raw fwd"] = e.groupby("vq")["fwd"].agg(["mean", "std", "count"])
    # 4 weekday daily
    dd = pd.concat(daily).dropna(subset=["r"])
    dd["rx"] = dd["r"] - dd["coin"].map(dd.groupby("coin")["r"].mean())
    out["weekday daily ex ret"] = dd.groupby("wd")["rx"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # 5 book by year and window
    bk = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; bk.append(t)
    bk = pd.concat(bk)
    bd = bk.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bd["year"] = pd.to_datetime(bd["day"]).dt.year
    out["book by year"] = bd.groupby("year")[["book_return", "coin_return"]].agg(["mean", "count"])
    wk = bd.groupby("w")["book_return"].agg(["mean", "std", "count"])
    out["book by window"] = wk
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count", "std"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"])
    return out

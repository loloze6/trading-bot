def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # daily reversal after down days, per coin, grid by horizon h (non-overlapping), signal = z of the day's return vs prior 20-day vol
    recs = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].astype(float).values)
            r1 = c.pct_change()
            vol = r1.rolling(20).std().shift(1)
            z = r1 / vol
            ret30 = c / c.shift(30) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(c)
            for h in (1, 3, 5):
                for t in range(0, n - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, z=z.iloc[t], f=c.iloc[t + h] / c.iloc[t] - 1,
                                     yr=yr.iloc[t], r30=ret30.iloc[t], vol=vol.iloc[t]))
    g = pd.DataFrame(recs).dropna(subset=["z", "f"])
    g["ex"] = g["f"] - g.groupby(["coin", "h"])["f"].transform("mean")
    g["ex_v"] = g["ex"] / g["vol"]
    g["zb"] = pd.cut(g["z"], [-99, -2, -1, 0, 1, 2, 99])
    a = g.groupby(["h", "zb"])["ex"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["ex return by prior-day z, by horizon"] = a.round(5)
    res = {}
    for (h, coin), s in g.groupby(["h", "coin"]):
        sl = stats.linregress(s["z"].clip(-4, 4), s["ex"]); res[f"h{h} {coin}"] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["slope ex on z by coin and h"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(5)
    res = {}
    for (h, yr), s in g.groupby(["h", "yr"]):
        if len(s) > 50:
            sl = stats.linregress(s["z"].clip(-4, 4), s["ex"]); res[f"h{h} {yr}"] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["slope ex on z by year and h"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(5)
    # down-day only slope (z<0), h=1, by sign of 30-day return
    d = g[(g.h == 1) & (g.z < 0)].dropna(subset=["r30"]).copy()
    res = {}
    for k, s in d.groupby(d["r30"] > 0):
        sl = stats.linregress(s["z"].clip(-4, 0), s["ex"]); res[f"r30>0={k}"] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["h1 down-day slope by 30d trend sign"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(5)
    # weekday t-stats of coin return
    dd = []
    for coin, ws in days.items():
        for w, df in ws.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin
            x["wd"] = pd.to_datetime(x["day"]).dt.dayofweek; dd.append(x)
    dd = pd.concat(dd).dropna(subset=["coin_return"])
    a = dd.groupby("wd")["coin_return"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["weekday coin return t"] = a.round(5)
    a = dd.groupby(["coin"])["coin_return"].apply(lambda s: 0).to_frame("x")
    sat = dd.assign(sat=dd.wd == 5).groupby(["coin", "sat"])["coin_return"].mean().unstack()
    out["saturday vs other by coin"] = sat.round(5)
    # book drawdown: worst 10% book days, what was coin doing and position
    bb = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            al = df["postRebalance_current_allocation"].shift(1)
            g1 = al * c.pct_change()
            r30 = c / c.shift(30) - 1
            bb.append(pd.DataFrame(dict(g=g1, al=al, cr=c.pct_change(), r30=r30.shift(1))))
    bb = pd.concat(bb).dropna()
    bb["q"] = pd.qcut(bb["g"].rank(method="first"), 10, labels=False)
    out["bar gain decile: alloc, coin ret, |alloc|"] = bb.groupby("q").agg(g=("g", "mean"), al=("al", "mean"),
        absal=("al", lambda s: s.abs().mean()), cr=("cr", "mean"), r30=("r30", "mean"), n=("g", "count")).round(4)
    bb["side"] = np.sign(bb["al"])
    out["bar gain by side"] = bb.groupby("side")["g"].agg(["mean", "count", "std"]).round(5)
    return out

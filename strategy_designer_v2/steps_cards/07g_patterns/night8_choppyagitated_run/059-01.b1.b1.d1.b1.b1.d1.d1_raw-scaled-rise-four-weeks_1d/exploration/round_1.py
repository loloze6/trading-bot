def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30, min_periods=20).mean()
            mult = r7 / mabs
            vol30 = r1.rolling(30, min_periods=20).std()
            tr60 = c / c.shift(60) - 1
            dayret = r1
            rng = (b["high"] - b["low"]) / c
            n = len(b)
            for h in [3, 7, 14, 28]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if np.isnan(fwd.iloc[i]) if i < n else True:
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     inprof=b["regime"].iloc[i] == "unknown",
                                     mult=mult.iloc[i], r1=dayret.iloc[i],
                                     sc1=dayret.iloc[i] / vol30.iloc[i] if vol30.iloc[i] else np.nan,
                                     vol30=vol30.iloc[i], tr60=tr60.iloc[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                     fc=b["forecast"].iloc[i], fwd=fwd.iloc[i]))
    df = pd.DataFrame(rows)
    # demean per coin, per horizon
    df["fwd_d"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["fwd_z"] = df["fwd_d"] / df.groupby(["coin", "h"])["fwd"].transform("std")

    def reg(sub, x):
        s = sub[[x, "fwd_z"]].dropna()
        if len(s) < 20:
            return (len(s), np.nan, np.nan)
        res = stats.linregress(s[x], s["fwd_z"])
        return (len(s), res.slope, res.slope / res.stderr)

    tab = []
    for h in [3, 7, 14, 28]:
        for prof in [True, False]:
            sub = df[(df.h == h) & (df.inprof == prof)]
            for x in ["mult", "sc1", "tr60", "vol30"]:
                n, sl, t = reg(sub, x)
                tab.append(dict(h=h, inprof=prof, x=x, n=n, slope=sl, t=t))
    out["slopes_fwd_z"] = pd.DataFrame(tab)

    # bins of weekly multiple, in/out profile, h=7 and 28
    q = []
    for h in [7, 28]:
        sub = df[df.h == h].dropna(subset=["mult"]).copy()
        sub["bin"] = pd.cut(sub["mult"], [-10, -1.5, -0.5, 0.5, 1.5, 10])
        g = sub.groupby(["inprof", "bin"], observed=True)["fwd_d"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["h"] = h
        q.append(g.reset_index())
    out["mult_bins"] = pd.concat(q).drop(columns="std")

    # daily scaled move bins, all bars, next 3 and 7 days
    q = []
    for h in [3, 7]:
        sub = df[df.h == h].dropna(subset=["sc1"]).copy()
        sub["bin"] = pd.cut(sub["sc1"], [-20, -2, -1, 1, 2, 20])
        g = sub.groupby(["inprof", "bin"], observed=True)["fwd_d"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["h"] = h
        q.append(g.reset_index())
    out["day_move_bins"] = pd.concat(q).drop(columns="std")

    # weekday on daily bars, next-day coin return
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    g = D.groupby("wd")["coin_return"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_coin_ret"] = g.drop(columns="std")
    g = D.groupby("w")["book_return"].agg(["count", "mean"])
    out["book_by_window"] = g
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    g = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_side"] = g
    return out

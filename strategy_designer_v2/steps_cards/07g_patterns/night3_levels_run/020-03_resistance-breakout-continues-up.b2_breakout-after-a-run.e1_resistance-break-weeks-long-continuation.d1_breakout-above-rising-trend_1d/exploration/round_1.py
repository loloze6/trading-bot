def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 20
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            sma = c.rolling(50, min_periods=50).mean()
            ma = c / sma - 1
            vol = r1.rolling(20, min_periods=15).std()
            hi90 = c.rolling(90, min_periods=60).max()
            dhi = c / hi90 - 1
            f = b["forecast"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n, H):
                if i + H >= n:
                    break
                rows.append(dict(coin=coin, win=w, fwd=fwd[i], r1=r1[i], r5=r5[i], r20=r20[i],
                                 ma=ma[i], vol=vol[i], dhi=dhi[i], f=f[i],
                                 wd=ts[i].dayofweek, yr=ts[i].year))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].transform("mean")
    df["u"] = df["fwd"] - drift
    df["vn"] = df.groupby("coin")["vol"].rank(pct=True)
    out = {}
    def grp(col, q=5):
        d = df.dropna(subset=[col, "u"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        g = d.groupby("q")["u"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.round(4)
    for col in ["r1", "r5", "r20", "ma", "vol", "dhi"]:
        out["u by quintile of " + col] = grp(col)
    act = df[df.f > 0]
    out["forecast>0 vs 0"] = pd.DataFrame({
        "on": [act.u.mean(), len(act)],
        "off": [df[df.f == 0].u.mean(), (df.f == 0).sum()]}).round(4)
    out["u by forecast tercile when on"] = act.assign(q=pd.qcut(act.f.rank(method="first"), 3, labels=False)).groupby("q")["u"].agg(["mean", "count"]).round(4)
    out["u by year"] = df.groupby("yr")["u"].agg(["mean", "count"]).round(4)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades by entry forecast tercile"] = T.assign(q=pd.qcut(T.entry_forecast.rank(method="first"), 3, labels=False)).groupby("q")[["net_profit_loss_percent", "entry_forecast", "dur_d"]].agg(["mean", "count"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    # book by window
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    D = pd.concat(dd)
    bw = D.groupby("win")[["book_return", "coin_return"]].mean()
    out["book by window (mean daily)"] = (bw * 1e4).round(1)
    return out

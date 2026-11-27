def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; out = {}
    rows = []
    for c in bars:
        allsd = pd.concat([b["close"].pct_change().rolling(30).std() for b in bars[c].values()])
        med = allsd.median()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            hi20 = b["high"].rolling(20).max()
            sd20 = r1.rolling(20).std()
            depth = (hi20 - cl) / hi20 / sd20
            sd30 = r1.rolling(30).std()
            n = len(b)
            for h in (3, 5, 10):
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame({"coin": c, "w": w, "h": h,
                    "depth": depth.iloc[idx].values, "up": (r1.iloc[idx] > 0).values,
                    "chop": (b["regime"].iloc[idx] != "chop").values,
                    "agit": (sd30.iloc[idx] > med).values,
                    "day": pd.to_datetime(b["timestamp"].iloc[idx]).dt.floor("D").values,
                    "yr": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values,
                    "fwd": fwd.iloc[idx].values}))
    D = pd.concat(rows).dropna(subset=["fwd", "depth"])
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["un"] = D["fwd"] - D["drift"]
    D["dz"] = D.groupby(["coin", "h"])["depth"].transform(lambda s: (s - s.mean()) / s.std())
    def ct(g):
        # day-clustered t of mean un
        s = g.groupby("day")["un"].sum(); n = len(g); m = g["un"].mean()
        dev = g.assign(d=g["un"] - m).groupby("day")["d"].sum()
        se = np.sqrt((dev**2).sum()) / n * np.sqrt(len(dev) / max(len(dev) - 1, 1))
        # slope of un on dz
        x = g["dz"]; y = g["un"]
        b1 = np.cov(x, y)[0, 1] / x.var() if len(g) > 3 else np.nan
        res = y - y.mean() - b1 * (x - x.mean())
        sb = np.sqrt((res**2).sum() / (len(g) - 2) / ((x - x.mean())**2).sum()) if len(g) > 3 else np.nan
        return pd.Series({"n": n, "days": len(dev), "mean_un": m, "t": m / se if se > 0 else np.nan,
                          "slope_per_sd": b1, "t_slope": b1 / sb if sb else np.nan})
    D["prof"] = np.where(D["chop"], "choppy", "trend") + np.where(D["agit"], "_agit", "_calm")
    out["slope of unusual move on depth, by h x profile"] = D.groupby(["h", "prof"]).apply(ct).round(4)
    Dc = D[D.chop]
    out["choppy: slope by h x up"] = Dc.groupby(["h", "up"]).apply(ct).round(4)
    out["choppy agit h5: by year"] = Dc[(Dc.agit) & (Dc.h == 5)].groupby("yr").apply(ct).round(4)
    out["choppy h5: by coin"] = Dc[Dc.h == 5].groupby("coin").apply(ct).round(4)
    # book: losses vs coin move during trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    T["coin_ret"] = T["exit_price"] / T["entry_price"] - 1
    T["dur_d"] = T["duration_minutes"] / 1440
    T["q"] = pd.qcut(T["entry_forecast"].abs().rank(method="first"), 4, labels=False)
    out["trades by |entry forecast| quartile"] = T.groupby("q").agg(n=("coin_ret", "size"), coin_ret=("coin_ret", "mean"),
        net=("net_profit_loss_percent", "mean"), med_net=("net_profit_loss_percent", "median"), dur=("dur_d", "mean")).round(3)
    out["trades: share coin up, mean coin ret"] = pd.Series({"share_up": (T.coin_ret > 0).mean(),
        "mean_coin_ret": T.coin_ret.mean(), "median_coin_ret": T.coin_ret.median(), "n": len(T)}).round(4)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            hi = c.rolling(31).max(); lo = c.rolling(31).min()
            rng = (hi - lo)
            pos = (c - lo) / rng
            net = (c - c.shift(30)) / rng
            flat = 1 - net.abs()
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            mom30 = c / c.shift(30) - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fc=b["forecast"].iloc[i], pos=pos.iloc[i], flat=flat.iloc[i],
                                 net=net.iloc[i], r1=r1.iloc[i], r5p=r5p.iloc[i], vol=vol20.iloc[i],
                                 vrel=vol20.iloc[i] / r1.std() if r1.std() > 0 else np.nan,
                                 mom30=mom30.iloc[i], fwd=fwd.iloc[i], year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - drift
    usual = g.groupby("coin")["fwd"].transform("std")
    g["z"] = g["ex"] / usual
    out = {}
    def tab(col, q=5, d=None):
        d = g if d is None else d
        d = d.dropna(subset=[col, "z"])
        b = pd.qcut(d[col].rank(method="first"), q, labels=False)
        t = d.groupby(b).agg(mean_x=(col, "mean"), n=("z", "size"), ex_pct=("ex", lambda x: x.mean() * 100),
                             z=("z", "mean"), t=("z", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
        return t.round(4)
    out["by_forecast_q"] = tab("fc")
    out["by_pos_q"] = tab("pos")
    out["by_flat_q"] = tab("flat")
    out["by_net30_q"] = tab("net")
    out["by_prev1d_q"] = tab("r1")
    out["by_prev5d_q"] = tab("r5p")
    out["by_vol_rel_q"] = tab("vrel")
    # pos signal strength by vol level and flatness
    d = g.dropna(subset=["pos", "flat", "vrel"]).copy()
    d["s"] = 2 * d["pos"] - 1
    res = []
    for name, col in [("vrel", "vrel"), ("flat", "flat")]:
        bb = pd.qcut(d[col].rank(method="first"), 3, labels=False)
        for k, sub in d.groupby(bb):
            sl = stats.linregress(sub["s"], sub["z"])
            res.append(dict(by=name, tercile=k, n=len(sub), slope=sl.slope, t=sl.slope / sl.stderr))
    out["pos_slope_by_tercile"] = pd.DataFrame(res).round(4)
    # momentum signs: net30 slope by vol
    res = []
    for k, sub in d.groupby(pd.qcut(d["vrel"].rank(method="first"), 3, labels=False)):
        sl = stats.linregress(sub["net"], sub["z"])
        res.append(dict(vol_tercile=k, n=len(sub), slope=sl.slope, t=sl.slope / sl.stderr))
    out["net30_slope_by_vol"] = pd.DataFrame(res).round(4)
    out["forecast_slope_by_coin"] = pd.DataFrame(
        [dict(coin=c, n=len(s), slope=stats.linregress(s["fc"], s["z"]).slope,
              t=stats.linregress(s["fc"], s["z"]).slope / stats.linregress(s["fc"], s["z"]).stderr)
         for c, s in g.dropna(subset=["fc", "z"]).groupby("coin")]).round(4)
    out["forecast_slope_by_year"] = pd.DataFrame(
        [dict(year=y, n=len(s), slope=stats.linregress(s["fc"], s["z"]).slope,
              t=stats.linregress(s["fc"], s["z"]).slope / stats.linregress(s["fc"], s["z"]).stderr)
         for y, s in g.dropna(subset=["fc", "z"]).groupby("year")]).round(4)
    # book daily
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; dl.append(x)
    D = pd.concat(dl)
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.dayofweek
    D["year"] = D["day"].dt.year
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count")).round(5)
    out["coin_ret_by_weekday"] = D.groupby("wd")["coin_return"].agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(x.count()))]).round(5)
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tl.append(t)
    T = pd.concat(tl)
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"),
                                               gross=("profit_loss_percent", "mean"), dur_days=("duration_minutes", lambda x: x.mean() / 1440)).round(3)
    return out

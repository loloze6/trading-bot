def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [1, 3, 5, 10, 20]
    coinmean = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            coinmean[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            rp = 2 * (c - lo) / (hi - lo) - 1
            ts = pd.to_datetime(b["timestamp"])
            for h in H:
                idx = np.arange(0, len(b) - h, h)
                for i in idx:
                    if b.loc[i, "regime"] != "unknown" or b.loc[i, "forecast"] == 0 or np.isnan(rp[i]):
                        continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, year=ts[i].year, h=h, rp=rp[i],
                                     f=b.loc[i, "forecast"], ex=r - coinmean[(coin, h)],
                                     day=ts[i].normalize()))
    d = pd.DataFrame(rows)

    def slope(g, x="f"):
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x] - g[x].mean(); y = g["ex"]
        bta = (X * y).sum() / (X ** 2).sum()
        res = y - y.mean() - bta * X
        s = (X * res).groupby(g["day"]).sum()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series(dict(n=len(g), slope=bta, t=bta / se))
    out = {}
    out["by_h_forecast"] = d.groupby("h").apply(slope)
    out["by_h_rangepos"] = d.groupby("h").apply(lambda g: slope(g, "rp"))
    d5 = d[d.h == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(slope)
    out["h5_by_year"] = d5.groupby("year").apply(slope)
    out["h5_by_window"] = d5.groupby("w").apply(slope)
    d5["q"] = pd.qcut(d5["rp"], 5, labels=False)
    out["h5_by_rp_quintile"] = d5.groupby("q").agg(n=("ex", "size"), rp=("rp", "mean"),
                                                    ex_mean=("ex", "mean"), ex_t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    d10 = d[d.h == 10].copy(); d10["q"] = pd.qcut(d10["rp"], 5, labels=False)
    out["h10_by_rp_quintile"] = d10.groupby("q").agg(n=("ex", "size"), rp=("rp", "mean"), ex_mean=("ex", "mean"))
    d5["side"] = np.sign(d5["f"])
    out["h5_signed_by_side"] = d5.groupby("side").apply(lambda g: pd.Series(dict(n=len(g), signed_ex=(g.ex * g.side).mean(), t=(g.ex*g.side).mean()/(g.ex*g.side).std()*np.sqrt(len(g)))))
    out["h5_by_side_slope"] = d5.groupby("side").apply(slope)
    return out

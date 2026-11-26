def explore(data):
    import pandas as pd, numpy as np
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 30:
                continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            s = pd.Series(c)
            vol20 = pd.Series(r1).rolling(20).std().values
            rng = ((b["high"] - b["low"]) / b["close"]).values
            rngrel = rng / pd.Series(rng).rolling(20).mean().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, day=ts.iloc[i].normalize(), wd=ts.iloc[i].weekday(),
                                 fwd=c[i+H]/c[i]-1, fwd1=c[i+1]/c[i]-1, r1=r1[i], absz=abs(r1[i])/vol20[i] if vol20[i] > 0 else np.nan,
                                 rngrel=rngrel[i], rng=rng[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    g["rng_pct"] = g.groupby("coin")["rng"].rank(pct=True)
    g["absz_pct"] = g.groupby("coin")["absz"].rank(pct=True)
    g["rngrel_pct"] = g.groupby("coin")["rngrel"].rank(pct=True)

    def slope(d, x, y="z"):
        d = d.dropna(subset=[x, y])
        X = d[x] - d[x].mean(); Y = d[y] - d[y].mean()
        b = (X*Y).sum() / (X*X).sum()
        e = Y - b*X
        se = np.sqrt(((X*e).groupby(d["day"]).sum()**2).sum()) / (X*X).sum()
        return pd.Series(dict(slope=b, t=b/se, n=len(d), days=d["day"].nunique()))

    def ct(d, col="ex"):
        d = d.dropna(subset=[col]); N = len(d); m = d[col].mean()
        dd = (d[col]-m).groupby(d["day"]).sum(); se = np.sqrt((dd**2).sum())/N
        return pd.Series(dict(n=N, mean=m, zmean=d["z"].mean(), t=m/se, days=d["day"].nunique()))

    out = {}
    out["slopes on z"] = pd.DataFrame({k: slope(g, k) for k in ["rng_pct", "absz_pct", "rngrel_pct"]}).T
    # signed: up days vs down days, by size of move
    g["sgn"] = np.sign(g["r1"])
    q = pd.cut(g["absz_pct"], [0, .5, .8, .9, 1.0], include_lowest=True)
    out["by |move| x sign"] = g.groupby([g["sgn"], q]).apply(ct)
    q2 = pd.cut(g["rngrel_pct"], [0, .2, .5, .8, .9, 1.0], include_lowest=True)
    out["by range vs own 20d"] = g.groupby(q2).apply(ct)
    out["slope by coin rng_pct"] = g.groupby("coin").apply(lambda d: slope(d, "rng_pct"))
    # book's largest days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; dl.append(d)
    D = pd.concat(dl)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index).weekday
    lo, hi = bk.book_return.quantile([.05, .95])
    out["book extremes"] = pd.DataFrame({
        "worst5%": bk[bk.book_return <= lo].mean(), "best5%": bk[bk.book_return >= hi].mean(),
        "all": bk.mean()})
    out["book share of return from worst/best 5%"] = pd.Series(dict(
        sum_all=bk.book_return.sum(), sum_worst=bk.book_return[bk.book_return <= lo].sum(),
        sum_best=bk.book_return[bk.book_return >= hi].sum(),
        hold_on_worst=bk.coin_return[bk.book_return <= lo].mean(),
        hold_on_best=bk.coin_return[bk.book_return >= hi].mean()))
    return out

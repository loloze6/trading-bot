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
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                up[i] = up[i-1] + 1 if r1[i] > 0 else 0
                dn[i] = dn[i-1] + 1 if r1[i] < 0 else 0
            s = pd.Series(c)
            ret5p = s / s.shift(5) - 1
            ret20p = s / s.shift(20) - 1
            vol20 = pd.Series(r1).rolling(20).std()
            rng = (b["high"] - b["low"]) / b["close"]
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(),
                                 year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 fwd=c[i+H] / c[i] - 1, up=up[i], dn=dn[i],
                                 r1=r1[i], ret5p=ret5p.iloc[i], ret20p=ret20p.iloc[i],
                                 vol20=vol20.iloc[i], rng=rng.iloc[i],
                                 fc=b["forecast"].iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    # scale-free: divide by coin's 5d std
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    for col in ["vol20", "rng", "ret5p", "ret20p", "r1"]:
        g[col + "_pct"] = g.groupby("coin")[col].rank(pct=True)

    def ct(d, col="ex"):
        d = d.dropna(subset=[col])
        N = len(d)
        if N < 10:
            return pd.Series(dict(n=N, mean=np.nan, t=np.nan))
        m = d[col].mean()
        dd = (d[col] - m).groupby(d["day"]).sum()
        se = np.sqrt((dd**2).sum()) / N
        return pd.Series(dict(n=N, mean=m, zmean=d["z"].mean(), t=m / se if se > 0 else np.nan, days=d["day"].nunique()))

    out = {}
    g["upb"] = g["up"].clip(upper=6)
    g["dnb"] = g["dn"].clip(upper=6)
    out["by up streak"] = g.groupby("upb").apply(ct)
    out["by down streak"] = g.groupby("dnb").apply(ct)
    for col in ["ret5p_pct", "ret20p_pct", "r1_pct", "vol20_pct", "rng_pct"]:
        q = pd.cut(g[col], [0, .1, .3, .5, .7, .9, 1.0], include_lowest=True)
        out["by " + col] = g.groupby(q).apply(ct)
    out["by weekday"] = g.groupby("wd").apply(ct)
    out["by year"] = g.groupby("year").apply(ct)
    # interaction: past 20d return within high/low vol
    g["hv"] = g["vol20_pct"] > 0.5
    q = pd.cut(g["ret20p_pct"], [0, .2, .8, 1.0], include_lowest=True)
    out["ret20 x highvol"] = g.groupby([g["hv"], q]).apply(ct)
    # book: daily returns, top/bottom days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    D = pd.concat(dl)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book vs hold daily"] = pd.Series(dict(book_mean=bk.book_return.mean(), hold_mean=bk.coin_return.mean(),
        book_sd=bk.book_return.std(), hold_sd=bk.coin_return.std(), corr=bk.corr().iloc[0, 1],
        beta=np.cov(bk.book_return, bk.coin_return)[0, 1] / bk.coin_return.var(), days=len(bk)))
    out["alloc by forecast>0"] = g.groupby(g["fc"] > 0)["alloc"].describe()
    return out

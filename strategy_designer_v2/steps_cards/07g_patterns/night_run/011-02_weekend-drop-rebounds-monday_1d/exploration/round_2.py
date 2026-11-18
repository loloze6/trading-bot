def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats

    def tstat(x):
        x = pd.Series(x).dropna()
        x = x[np.isfinite(x)]
        n = len(x)
        if n < 3 or x.std() == 0:
            return (n, np.nan, np.nan)
        return (n, x.mean(), x.mean() / (x.std() / np.sqrt(n)))

    def summ(df, by, col):
        out = []
        for k, g in df.groupby(by):
            n, m, t = tstat(g[col])
            out.append(dict(group=str(k), n=n, mean=m, t=t))
        return pd.DataFrame(out)

    def to_ts(s):
        if pd.api.types.is_datetime64_any_dtype(s):
            ts = pd.to_datetime(s)
            if ts.dt.tz is None:
                ts = ts.dt.tz_localize("UTC")
            return ts
        if pd.api.types.is_numeric_dtype(s):
            return pd.to_datetime(s, unit="ms", utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = to_ts(b["timestamp"])
            c = b["close"].astype(float)
            r1 = c.pct_change()
            lr = np.log(c).diff()
            vol = lr.rolling(20, min_periods=10).std()
            v = b["volume"].astype(float)
            rv = v / v.rolling(20, min_periods=10).mean()
            rng = (b["high"].astype(float) - b["low"].astype(float)) / c
            df = pd.DataFrame(dict(
                coin=coin, w=w, wd=ts.dt.dayofweek.values, year=ts.dt.year.values,
                r1=r1.values, z=(r1 / vol).values, vol=vol.values, rv=rv.values,
                r2=(c / c.shift(2) - 1).values,
                f1=(c.shift(-1) / c - 1).values, f2=(c.shift(-2) / c - 1).values,
                f7=(c.shift(-7) / c - 1).values,
                r30=(c / c.shift(30) - 1).values, r7=(c / c.shift(7) - 1).values,
                rng=(rng / rng.rolling(20, min_periods=10).mean()).values,
                pos=np.arange(len(b)),
                alloc=b["postRebalance_current_allocation"].astype(float).values))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    m1 = D.groupby("coin")["f1"].mean()
    m2 = D[D.pos % 2 == 0].groupby("coin")["f2"].mean()
    m7 = D[D.pos % 7 == 0].groupby("coin")["f7"].mean()
    D["e1"] = D["f1"] - D["coin"].map(m1)
    D["e2"] = D["f2"] - D["coin"].map(m2)
    D["e7"] = D["f7"] - D["coin"].map(m7)
    D["e2s"] = D["e2"] / D["vol"]
    D["e1s"] = D["e1"] / D["vol"]

    res = {}
    def safe(name, fn):
        try:
            res[name] = fn()
        except Exception as ex:
            res[name] = "err: " + str(ex)[:100]

    safe("A day return by weekday (0=Mon)", lambda: summ(D, "wd", "r1"))

    def fB():
        out = []
        for k, g in D.groupby("wd"):
            g = g[np.isfinite(g.z) & np.isfinite(g.e2s)]
            r, p = stats.pearsonr(g.z, g.e2s)
            n = len(g)
            dn = g[g.z < -1]["e2"]; up = g[g.z > 1]["e2"]
            out.append(dict(wd=k, n=n, corr_z_next2=r, t=r * np.sqrt((n - 2) / (1 - r * r)),
                            n_dn=len(dn), e2_dn=dn.mean(), t_dn=tstat(dn)[2],
                            n_up=len(up), e2_up=up.mean(), t_up=tstat(up)[2]))
        return pd.DataFrame(out)
    safe("B next-2d excess vs day z, by weekday", fB)

    def fB2():
        # 2-day move (z of 2-day ret) ending each weekday vs next 2d, per weekday
        out = []
        for k, g in D.groupby("wd"):
            zz = g.r2 / (g.vol * np.sqrt(2))
            m = np.isfinite(zz) & np.isfinite(g.e2s)
            r, _ = stats.pearsonr(zz[m], g.e2s[m]); n = m.sum()
            out.append(dict(wd_end=k, n=n, corr=r, t=r * np.sqrt((n - 2) / (1 - r * r))))
        return pd.DataFrame(out)
    safe("B2 2-day move ending weekday vs next 2d", fB2)

    def fC():
        G = D[np.isfinite(D.z) & np.isfinite(D.e1)].copy()
        G["zq"] = pd.qcut(G["z"], 5, labels=False)
        return summ(G, "zq", "e1")
    safe("C next-day excess by z quintile", fC)

    def fC2():
        G = D[np.isfinite(D.z) & np.isfinite(D.e1)].copy()
        G["zq"] = pd.qcut(G["z"], 5, labels=False)
        G["wkend"] = G.wd.isin([5, 6]).astype(int)
        return summ(G, ["wkend", "zq"], "e1")
    safe("C2 next-day excess by weekend-day x z quintile", fC2)

    def fD():
        G = D[np.isfinite(D.vol) & np.isfinite(D.e1)].copy()
        G["vq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
        return summ(G, "vq", "e1")
    safe("D next-day excess by vol tercile", fD)

    def fE():
        G = D[np.isfinite(D.rv) & np.isfinite(D.e1) & np.isfinite(D.r1)].copy()
        G["rq"] = G.groupby("coin")["rv"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
        G["sg"] = np.sign(G["r1"])
        return summ(G, ["rq", "sg"], "e1")
    safe("E next-day excess by relvol tercile x day sign", fE)

    def fE2():
        G = D[np.isfinite(D.rng) & np.isfinite(D.e1)].copy()
        G["q"] = G.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        return summ(G, "q", "e1")
    safe("E2 next-day excess by relative range quintile", fE2)

    def fF():
        G = D[(D.pos % 7 == 0)]
        G = G[np.isfinite(G.r30) & np.isfinite(G.e7)].copy()
        G["q"] = G.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        return summ(G, "q", "e7")
    safe("F next-7d excess by 30d return quintile (7-grid)", fF)

    def fF2():
        G = D[(D.pos % 7 == 0)]
        G = G[np.isfinite(G.r7) & np.isfinite(G.e7)].copy()
        G["q"] = G.groupby("coin")["r7"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        return summ(G, "q", "e7")
    safe("F2 next-7d excess by 7d return quintile (7-grid)", fF2)

    def fF3():
        G = D[(D.pos % 7 == 0)]
        G = G[np.isfinite(G.r30) & np.isfinite(G.e7)].copy()
        out = []
        for k, g in G.groupby("coin"):
            r, _ = stats.pearsonr(g.r30, g.e7); n = len(g)
            out.append(dict(coin=k, n=n, corr=r, t=r * np.sqrt((n - 2) / (1 - r * r))))
        return pd.DataFrame(out)
    safe("F3 corr 30d ret vs next 7d, per coin", fF3)

    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy()
            dd = pd.to_datetime(d["day"])
            d["wd"] = dd.dt.dayofweek.values
            d["year"] = dd.dt.year.values
            d["coin"] = coin
            bk.append(d)
    B = pd.concat(bk, ignore_index=True)
    safe("H book return by weekday", lambda: summ(B, "wd", "book_return"))
    safe("H2 coin return by weekday (days)", lambda: summ(B, "wd", "coin_return"))
    safe("H3 book return by year", lambda: summ(B, "year", "book_return"))
    safe("H4 coin return by year", lambda: summ(B, "year", "coin_return"))

    def fI():
        A = D[(D.alloc.abs() > 0) & np.isfinite(D.e1)].copy()
        A["aq"] = A.groupby("wd")["alloc"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
        return summ(A, ["wd", "aq"], "e1")
    safe("I next-day excess by alloc tercile x weekday held", fI)

    def fJ():
        # Sunday drop z vs next 2d excess per coin
        S = D[(D.wd == 6) & (D.z < 0)]
        S = S[np.isfinite(S.z) & np.isfinite(S.e2s)]
        out = []
        for k, g in S.groupby("coin"):
            r, _ = stats.pearsonr(-g.z, g.e2s); n = len(g)
            out.append(dict(coin=k, n=n, corr=r, t=r * np.sqrt((n - 2) / (1 - r * r))))
        return pd.DataFrame(out)
    safe("J Sunday-drop size vs next2d, per coin", fJ)
    return res

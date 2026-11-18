def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats

    def tstat(x):
        x = pd.Series(x).dropna()
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

    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            tsr = b["timestamp"]
            if np.issubdtype(tsr.dtype, np.number):
                ts = pd.to_datetime(tsr, unit="ms", utc=True)
            else:
                ts = pd.to_datetime(tsr, utc=True, errors="coerce")
            c = b["close"].astype(float)
            r1 = c.pct_change()
            lr = np.log(c).diff()
            vol = lr.rolling(20, min_periods=10).std()
            v = b["volume"].astype(float)
            rv = v / v.rolling(20, min_periods=10).mean()
            df = pd.DataFrame(dict(
                coin=coin, w=w, wd=ts.dt.dayofweek.values, year=ts.dt.year.values,
                r1=r1, z=r1 / vol, vol=vol, rv=rv,
                f1=c.shift(-1) / c - 1, f2=c.shift(-2) / c - 1, f7=c.shift(-7) / c - 1,
                r30=c / c.shift(30) - 1, r7=c / c.shift(7) - 1,
                pos=np.arange(len(b)),
                alloc=b["postRebalance_current_allocation"].astype(float)))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    # coin means over all windows
    m1 = D.groupby("coin")["f1"].mean()
    m2 = D[D.pos % 2 == 0].groupby("coin")["f2"].mean()
    m7 = D[D.pos % 7 == 0].groupby("coin")["f7"].mean()
    D["e1"] = D["f1"] - D["coin"].map(m1)
    D["e2"] = D["f2"] - D["coin"].map(m2)
    D["e7"] = D["f7"] - D["coin"].map(m7)
    D["e2s"] = D["e2"] / D["vol"]

    res = {}
    # A: own return by weekday
    res["A day return by weekday (0=Mon)"] = summ(D, "wd", "r1")

    # B: reversal slope by weekday of the signal day (same weekday cases are 7 bars apart)
    out = []
    for k, g in D.dropna(subset=["z", "e2s"]).groupby("wd"):
        g = g[np.isfinite(g.z) & np.isfinite(g.e2s)]
        r, p = stats.pearsonr(g.z, g.e2s)
        n = len(g)
        dn = g[g.z < -1]["e2"]; up = g[g.z > 1]["e2"]
        out.append(dict(wd=k, n=n, corr_z_next2=r, t=r * np.sqrt((n - 2) / (1 - r * r)),
                        n_dn=len(dn), e2_after_dn=dn.mean(), n_up=len(up), e2_after_up=up.mean()))
    res["B next-2d excess vs day z, by weekday"] = pd.DataFrame(out)

    # C: z quintile -> next day excess
    G = D.dropna(subset=["z", "e1"]).copy()
    G["zq"] = pd.qcut(G["z"], 5, labels=False)
    res["C next-day excess by z quintile"] = summ(G, "zq", "e1")

    # D: vol tercile within coin -> next day excess
    G = D.dropna(subset=["vol", "e1"]).copy()
    G["vq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res["D next-day excess by vol tercile"] = summ(G, "vq", "e1")

    # E: relative volume tercile x sign of day -> next-day excess
    G = D.dropna(subset=["rv", "e1", "r1"]).copy()
    G["rq"] = G.groupby("coin")["rv"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    G["sg"] = np.sign(G["r1"])
    res["E next-day excess by relvol tercile x day sign"] = summ(G, ["rq", "sg"], "e1")

    # F: 30d return quintile -> next 7d excess on 7-grid
    G = D[(D.pos % 7 == 0)].dropna(subset=["r30", "e7"]).copy()
    G["q"] = G.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["F next-7d excess by 30d return quintile (7-grid)"] = summ(G, "q", "e7")
    G = D[(D.pos % 7 == 0)].dropna(subset=["r7", "e7"]).copy()
    G["q"] = G.groupby("coin")["r7"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["F2 next-7d excess by 7d return quintile (7-grid)"] = summ(G, "q", "e7")

    # G: weekend (Sat+Sun) 2-day move vs weekday 2-day move, next 2d excess
    out = []
    for wdend, lab in [(6, "Sat+Sun ending Sun"), (2, "Tue+Wed ending Wed"), (3, "Wed+Thu ending Thu")]:
        g = D[D.wd == wdend].copy()
        # 2-day prior return approx from r1 and previous r1 not stored; use r7 skip; compute via z only
        g = g.dropna(subset=["z", "e2"])
        hi = g[g.z.abs() > g.z.abs().median()]
        r, _ = stats.pearsonr(hi.z, hi.e2 / hi.vol)
        out.append(dict(case=lab, n_bigmoves=len(hi), corr=r, t=r * np.sqrt((len(hi) - 2) / (1 - r * r))))
    res["G big-move reversal by day"] = pd.DataFrame(out)

    # H: book
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
    res["H book return by weekday"] = summ(B, "wd", "book_return")
    res["H2 coin return by year"] = summ(B, "year", "coin_return")
    res["H3 book return by year"] = summ(B, "year", "book_return")

    # I: forecast-active days: next-day excess by forecast tercile, Mon vs Tue
    A = D[D.alloc.abs() > 0].dropna(subset=["e1"]).copy()
    A["aq"] = pd.qcut(A["alloc"], 3, labels=False, duplicates="drop")
    res["I next-day excess by alloc tercile x weekday"] = summ(A, ["wd", "aq"], "e1")
    return res

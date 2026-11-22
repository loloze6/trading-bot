def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; drows = []
    for coin, wins in data["bars"].items():
        g5 = []; g1 = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 5, 5):
                g5.append(c[i+5]/c[i]-1)
            g1 += list(pd.Series(c).pct_change().dropna().values)
        mu5 = np.mean(g5); sd5 = np.std(g5); mu1 = np.mean(g1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            r30 = c / c.shift(30) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=20).std()
            hi60 = c.rolling(60, min_periods=20).max(); dist = c/hi60 - 1
            fwd = c.shift(-5)/c - 1
            nxt = c.shift(-1)/c - 1
            for i in range(0, len(b) - 5, 5):
                rows.append(dict(coin=coin, win=w, yr=ts.iloc[i].year, r30=r30.iloc[i],
                                 r30v=r30.iloc[i]/(vol20.iloc[i]*np.sqrt(30)) if vol20.iloc[i] else np.nan,
                                 vol20=vol20.iloc[i], vr=vol20.iloc[i]/vol60.iloc[i], dist=dist.iloc[i],
                                 z=(fwd.iloc[i]-mu5)/sd5, f=b["forecast"].iloc[i]))
            dd = pd.DataFrame(dict(coin=coin, win=w, day=ts.dt.floor("D"), wd=ts.dt.dayofweek, yr=ts.dt.year,
                                   r=nxt - mu1, a=b["postRebalance_current_allocation"]))
            drows.append(dd)
    d = pd.DataFrame(rows).dropna()
    D = pd.concat(drows).dropna()
    # weekday of next-day return (return of day wd+1), clustered by date: average coins per date first
    D["nwd"] = (D["wd"] + 1) % 7
    perdate = D.groupby(["day", "nwd", "yr"])["r"].mean().reset_index()
    t = perdate.groupby("nwd")["r"].agg(n="size", mean="mean", sd="std")
    t["t"] = t["mean"]/(t["sd"]/np.sqrt(t["n"]))
    out["next-day excess return by its weekday (date-clustered)"] = t
    out["weekday excess by year (mean x1e3)"] = (perdate.pivot_table(index="yr", columns="nwd", values="r", aggfunc="mean")*1e3).round(2)
    # momentum slope by vol tercile, date-robust: by year and by coin halves
    d["vb"] = d.groupby("yr")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = {}
    for (yr, vb), s in d.groupby(["yr", "vb"]):
        if len(s) > 30:
            lr = stats.linregress(s["r30"].clip(-1, 2), s["z"]); res[(yr, vb)] = lr.slope/lr.stderr
    out["t of z on r30, by year (rows) x vol tercile within year"] = pd.Series(res).unstack()
    # per-coin vol tercile (coin's own vol)
    d["vbc"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = {}
    for vb, s in d.groupby("vbc"):
        lr = stats.linregress(s["r30"].clip(-1, 2), s["z"]); res[vb] = dict(n=len(s), slope=lr.slope, t=lr.slope/lr.stderr)
        lr2 = stats.linregress(s["r30v"], s["z"]); res[vb]["t_volscaled_r30"] = lr2.slope/lr2.stderr
    out["z on r30 by coin's own vol tercile"] = pd.DataFrame(res).T
    # r30 quintile x own-vol tercile mean z
    d["rq"] = pd.qcut(d["r30"].rank(method="first"), 5, labels=False)
    out["mean z: r30 quintile x own-vol tercile"] = d.pivot_table(index="rq", columns="vbc", values="z", aggfunc="mean").round(3)
    # vol-scaled r30 vs raw r30 whole sample
    for col in ["r30", "r30v"]:
        lr = stats.linregress(d[col].clip(-1, 2) if col == "r30" else d[col], d["z"])
        out[f"z on {col} all t"] = lr.slope/lr.stderr
    # book: largest gain/loss days, what preceded
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bk.append(x.assign(coin=coin, win=w))
    bk = pd.concat(bk).dropna(subset=["book_return"])
    bd = bk.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean"))
    bd["q"] = pd.qcut(bd["br"].rank(method="first"), 10, labels=False)
    bd["prev_cr"] = bd["cr"].shift(1)
    out["book days by decile: book ret, coins ret"] = bd.groupby("q")[["br", "cr"]].mean()
    # short side by forecast strength
    D2 = D.copy(); D2["side"] = np.sign(D2["a"])
    out["excess next-day by side and year"] = (D2.pivot_table(index="yr", columns="side", values="r", aggfunc="mean")*1e3).round(2)
    return out

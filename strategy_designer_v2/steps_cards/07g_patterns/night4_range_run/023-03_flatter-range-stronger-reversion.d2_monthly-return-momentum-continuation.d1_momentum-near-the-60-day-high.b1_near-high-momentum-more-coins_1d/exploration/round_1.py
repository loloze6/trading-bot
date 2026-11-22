def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean 5-day return over all windows (grid)
        g5 = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 5, 5):
                g5.append(c[i+5]/c[i]-1)
        mu5 = np.mean(g5) if g5 else np.nan
        sd5 = np.std(g5) if g5 else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r5p = c / c.shift(5) - 1
            hi60 = c.rolling(60, min_periods=20).max()
            lo60 = c.rolling(60, min_periods=20).min()
            dist = c / hi60 - 1
            pos = (c - lo60) / (hi60 - lo60)
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=20).std()
            fwd = c.shift(-5) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b) - 5, 5):
                rows.append(dict(coin=coin, win=w, f=b["forecast"].iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 r30=r30.iloc[i], r5p=r5p.iloc[i], dist=dist.iloc[i], pos=pos.iloc[i],
                                 vr=vol20.iloc[i]/vol60.iloc[i] if vol60.iloc[i] else np.nan,
                                 vol20=vol20.iloc[i], fwd=fwd.iloc[i], ex=fwd.iloc[i]-mu5,
                                 z=(fwd.iloc[i]-mu5)/sd5, wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year))
    d = pd.DataFrame(rows)
    out = {}
    def tab(col, q=5):
        x = d.dropna(subset=[col, "ex"]).copy()
        x["b"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        t = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                               ex=("ex", "mean"), z=("z", "mean"))
        t["t"] = x.groupby("b")["ex"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        return t
    out["forecast quintiles"] = tab("f")
    out["r30 quintiles"] = tab("r30")
    out["dist from 60d high quintiles"] = tab("dist")
    out["range position quintiles"] = tab("pos")
    out["prior 5d return quintiles"] = tab("r5p")
    out["vol20 quintiles"] = tab("vol20")
    out["vol ratio 20/60 quintiles"] = tab("vr")
    # interaction r30 x dist (terciles)
    x = d.dropna(subset=["r30", "dist", "ex"]).copy()
    x["rb"] = pd.qcut(x["r30"], 3, labels=["r30lo", "r30mid", "r30hi"])
    x["db"] = pd.qcut(x["dist"], 3, labels=["far", "mid", "near"])
    out["r30 x dist mean ex (z)"] = x.pivot_table(index="rb", columns="db", values="z", aggfunc="mean")
    out["r30 x dist n"] = x.pivot_table(index="rb", columns="db", values="z", aggfunc="size")
    # by vol tercile: slope of ex on r30
    x = d.dropna(subset=["r30", "vol20", "ex"]).copy()
    x["vb"] = pd.qcut(x["vol20"], 3, labels=False)
    res = {}
    for k, s in x.groupby("vb"):
        lr = stats.linregress(s["r30"], s["z"]); res[k] = dict(n=len(s), slope=lr.slope, t=lr.slope/lr.stderr)
    out["z on r30 by vol tercile"] = pd.DataFrame(res).T
    # weekday
    wd = d.groupby("wd")["z"].agg(["size", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["weekday z"] = wd
    # book: long vs short days
    br = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            g = b["postRebalance_current_allocation"] * (b["close"].shift(-1)/b["close"]-1)
            br.append(pd.DataFrame(dict(a=b["postRebalance_current_allocation"], g=g, yr=pd.to_datetime(b["timestamp"]).dt.year)))
    br = pd.concat(br).dropna()
    br["side"] = np.sign(br["a"])
    out["bar gain by side"] = br.groupby("side")["g"].agg(["size", "mean", "sum"])
    out["bar gain by side and year"] = br.pivot_table(index="yr", columns="side", values="g", aggfunc="mean")
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    tr["dur_d"] = tr["duration_minutes"]/1440
    tr["db"] = pd.qcut(tr["dur_d"].rank(method="first"), 4, labels=False)
    out["trades by duration quartile"] = tr.groupby("db").agg(dmin=("dur_d", "min"), dmax=("dur_d", "max"),
                                                            n=("net_profit_loss_percent", "size"),
                                                            pnl=("net_profit_loss_percent", "mean"))
    return out

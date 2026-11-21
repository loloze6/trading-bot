def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def ols_t(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        m = ~(np.isnan(x) | np.isnan(y))
        x, y = x[m], y[m]
        if len(x) < 30 or np.std(x) == 0: return (np.nan, np.nan, len(x))
        r = stats.linregress(x, y)
        return (r.slope, r.slope / r.stderr, len(x))
    def build(h):
        recs = []
        for coin, wins in bars.items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values.astype(float)
                f = b["forecast"].values.astype(float)
                ts = pd.to_datetime(b["timestamp"])
                r20 = pd.Series(c).pct_change(20).values
                r60 = pd.Series(c).pct_change(60).values
                for i in range(0, len(b) - h, h):
                    recs.append(dict(coin=coin, year=ts.iloc[i].year, f=f[i],
                                     fwd=c[i + h] / c[i] - 1, r20=r20[i], r60=r60[i]))
        d = pd.DataFrame(recs)
        d["fwd_dm"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        d["dirmove"] = np.sign(d["f"]) * d["fwd_dm"]
        d["agree20"] = np.sign(d["f"]) == np.sign(d["r20"])
        d["agree60"] = np.sign(d["f"]) == np.sign(d["r60"])
        return d
    out = {}
    hz = []
    for h in [1, 2, 3, 5, 10, 20]:
        d = build(h)
        for k, g in d.groupby("agree20"):
            s, t, n = ols_t(g["f"], g["fwd_dm"])
            hz.append(dict(h=h, agree20=k, slope=s, t=t, n=n, dirmove=g["dirmove"].mean()))
    out["agree20_by_horizon"] = pd.DataFrame(hz)
    d = build(5)
    a = d[d["agree20"]]
    res = []
    for k, g in a.groupby("year"):
        s, t, n = ols_t(g["f"], g["fwd_dm"]); res.append(dict(year=k, slope=s, t=t, n=n))
    out["agree20_h5_by_year"] = pd.DataFrame(res)
    res = []
    for k, g in a.groupby("coin"):
        s, t, n = ols_t(g["f"], g["fwd_dm"]); res.append(dict(coin=k, slope=s, t=t, n=n))
    out["agree20_h5_by_coin"] = pd.DataFrame(res)
    res = []
    for k, g in d.groupby("agree60"):
        s, t, n = ols_t(g["f"], g["fwd_dm"]); res.append(dict(agree60=k, slope=s, t=t, n=n, dirmove=g["dirmove"].mean()))
    out["agree60_h5"] = pd.DataFrame(res)
    a["absq"] = pd.qcut(a["f"].abs(), 4, labels=False, duplicates="drop")
    out["agree20_h5_dirmove_by_absq"] = a.groupby("absq").agg(absf=("f", lambda x: x.abs().mean()),
        mean=("dirmove", "mean"), t=("dirmove", lambda x: x.mean()/x.std()*np.sqrt(len(x))), n=("dirmove","size"))
    d1 = build(1)
    d1["absq"] = pd.qcut(d1["f"].abs(), 4, labels=False, duplicates="drop")
    out["h1_dirmove_by_absq"] = d1.groupby("absq").agg(absf=("f", lambda x: x.abs().mean()),
        mean=("dirmove", "mean"), t=("dirmove", lambda x: x.mean()/x.std()*np.sqrt(len(x))), n=("dirmove","size"))
    d5 = d.copy(); d5["side"] = np.sign(d5["f"])
    d5["absq"] = pd.qcut(d5["f"].abs(), 4, labels=False, duplicates="drop")
    out["h5_fwd_dm_by_side_absq"] = d5.groupby(["side","absq"]).agg(fwd_dm=("fwd_dm","mean"), n=("f","size"))
    return out

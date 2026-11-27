def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float)
            r = c.pct_change()
            hh = h.rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            depth = (c - hh) / hh / sd
            tr60 = c / c.shift(60) - 1
            inprof = (df["regime"] == "unknown")
            for H in (1, 3, 5, 10):
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(df), H)
                for i in idx:
                    if np.isnan(fwd.iloc[i]) or np.isnan(depth.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, H=H, i=i, depth=depth.iloc[i], fwd=fwd.iloc[i],
                                     prof=bool(inprof.iloc[i]), tr60=tr60.iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    mu = d.groupby(["coin", "H"])["fwd"].mean().rename("mu")
    d = d.join(mu, on=["coin", "H"]); d["ex"] = d["fwd"] - d["mu"]
    out = {}
    res = []
    for (H, prof), g in d.groupby(["H", "prof"]):
        sl = stats.linregress(g["depth"], g["ex"])
        q = pd.qcut(g["depth"], 3, labels=["deep", "mid", "shallow"])
        m = g.groupby(q)["ex"].mean()
        res.append(dict(H=H, prof=prof, n=len(g), slope=sl.slope, t=sl.slope / sl.stderr,
                        deep=m["deep"], mid=m["mid"], shallow=m["shallow"], meanfwd=g["fwd"].mean(),
                        t_mean=g["ex"].mean() / g["ex"].std() * np.sqrt(len(g))))
    out["slope_by_H_prof"] = pd.DataFrame(res)
    p = d[d.prof]
    r2 = []
    for (H, coin), g in p.groupby(["H", "coin"]):
        if len(g) < 10: continue
        sl = stats.linregress(g["depth"], g["ex"])
        r2.append(dict(H=H, coin=coin, n=len(g), slope=sl.slope, t=sl.slope / sl.stderr, meanex=g["ex"].mean()))
    out["prof_by_coin"] = pd.DataFrame(r2)
    r3 = []
    for (H, y), g in p[p.H.isin([3, 5])].groupby(["H", "year"]):
        if len(g) < 8: continue
        sl = stats.linregress(g["depth"], g["ex"])
        r3.append(dict(H=H, year=y, n=len(g), slope=sl.slope, t=sl.slope / sl.stderr, meanex=g["ex"].mean()))
    out["prof_by_year"] = pd.DataFrame(r3)
    # deep quintiles in profile
    r4 = []
    for H, g in p.groupby("H"):
        q = pd.qcut(g["depth"], 5, labels=False)
        for k, gg in g.groupby(q):
            r4.append(dict(H=H, q=k, n=len(gg), depth=gg["depth"].mean(), ex=gg["ex"].mean(),
                           t=gg["ex"].mean() / gg["ex"].std() * np.sqrt(len(gg)), up=(gg["fwd"] > 0).mean()))
    out["prof_quintiles"] = pd.DataFrame(r4)
    return out

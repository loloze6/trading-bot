def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c - 1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            sig = 2*(c-(h+l)/2)/c/sd
            pos = (c-l)/(h-l)
            width = (h-l)/c/sd
            df = pd.DataFrame({"coin": coin, "win": w, "sig": sig, "pos": pos, "width": width,
                               "inprof": b["regime"].eq("unknown"),
                               "fc": b["forecast"].astype(float),
                               "r1": c.shift(-1)/c-1-mu, "r2": c.shift(-2)/c-1-2*mu, "r3": c.shift(-3)/c-1-3*mu,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["sig", "r1"])
    out = {}
    def summ(g, col="r1"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g)})
        dd = g.groupby("day")[col].sum(); n = g.groupby("day")[col].count()
        m = g[col].mean()
        t = m/(g[col].std()/np.sqrt(len(g)))
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean%": 100*m, "t": t})
    p = d[d.inprof]
    out["in profile, low side vs high side, h1"] = pd.DataFrame({
        "low(sig<0)": summ(p[p.sig < 0]), "high(sig>0)": summ(p[p.sig > 0]),
        "fc>0": summ(p[p.fc > 0]), "all in profile": summ(p)})
    lo = p[p.sig < 0].copy()
    lo["q"] = pd.qcut(-lo.sig, 5, labels=False)
    out["low side by quintile of |sig| (4 strongest), h1/h2/h3"] = pd.concat(
        {h: lo.groupby("q").apply(lambda g: summ(g, h)) for h in ["r1", "r2", "r3"]}, axis=1)
    hi = p[p.sig > 0].copy()
    hi["q"] = pd.qcut(hi.sig, 5, labels=False)
    out["high side by quintile, h1 (reversal = negative)"] = hi.groupby("q").apply(summ)
    out["low side by coin h1"] = lo.groupby("coin").apply(summ)
    out["low side by year h1"] = lo.groupby("year").apply(summ)
    out["low side by window h1"] = lo.groupby("win").apply(summ)
    # outside profile for comparison
    o = d[~d.inprof & (d.sig < 0)].copy()
    o["q"] = pd.qcut(-o.sig, 5, labels=False)
    out["outside profile low side by quintile h1"] = o.groupby("q").apply(summ)
    # width vs position separately on low side
    lo["wq"] = pd.qcut(lo.width, 3, labels=False); lo["pq"] = pd.qcut(lo.pos, 3, labels=False)
    out["low side mean% h1 by width tercile x pos tercile"] = lo.groupby(["wq", "pq"])["r1"].mean().unstack()*100
    out["low side slope r1 on -sig"] = pd.Series(stats.linregress(-lo.sig, lo.r1)._asdict())
    return out

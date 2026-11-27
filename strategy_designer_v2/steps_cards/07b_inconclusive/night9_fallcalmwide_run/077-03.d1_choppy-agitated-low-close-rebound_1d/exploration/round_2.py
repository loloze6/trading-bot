def explore(data):
    import numpy as np, pandas as pd
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
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "sig": sig,
                               "inprof": b["regime"].eq("unknown"),
                               "r1": c.shift(-1)/c-1-mu, "r2": c.shift(-2)/c-1-2*mu,
                               "day": ts.dt.floor("D"), "year": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["sig", "r1"])
    def summ(g, col="r1"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g)})
        m = g[col].mean()
        dev = (g[col]-m).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum()*G/(G-1))/len(g)
        return pd.Series({"n": len(g), "days": G, "mean%": 100*m, "t_day": m/se})
    p = d[d.inprof].copy()
    lo = p[p.sig < 0].copy(); hi = p[p.sig > 0].copy()
    lo["strong"] = -lo.sig >= (-lo.sig).quantile(0.6)
    hi["strong"] = hi.sig >= hi.sig.quantile(0.6)
    out = {}
    out["low side strong 40% vs weak 60%, h1 and h2"] = pd.DataFrame({
        "strong h1": summ(lo[lo.strong]), "weak h1": summ(lo[~lo.strong]),
        "strong h2": summ(lo[lo.strong], "r2"), "weak h2": summ(lo[~lo.strong], "r2")})
    out["low side strong by year h1"] = lo[lo.strong].groupby("year").apply(summ)
    out["low side strong by coin h1"] = lo[lo.strong].groupby("coin").apply(summ)
    out["low |sig| cutoff for strong"] = float((-lo.sig).quantile(0.6))
    out["high side strong 40% vs weak h1 (fade=negative)"] = pd.DataFrame({
        "strong": summ(hi[hi.strong]), "weak": summ(hi[~hi.strong])})
    out["high side by year h1"] = hi.groupby("year").apply(summ)
    p["fade"] = -np.sign(p.sig) * p.r1
    p["w"] = p.sig.abs()
    out["both sides fade, weighted mean% and plain"] = pd.Series({
        "weighted%": 100*(p.fade*p.w).sum()/p.w.sum(), "plain": summ(p.assign(r1=p.fade))["mean%"],
        "t_day": summ(p.assign(r1=p.fade))["t_day"], "n": len(p)})
    return out

def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o=b["open"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "ts": b["timestamp"], "pos": np.arange(len(b)),
                               "z": r/sd, "rngz": ((h-l)/c.shift(1))/sd, "r5z": (c/c.shift(5)-1)/(sd*np.sqrt(5)),
                               "r10z": (c/c.shift(10)-1)/(sd*np.sqrt(10)),
                               "sd": sd, "sdrel": sd/sd.rolling(120, min_periods=60).median(),
                               "cl": (h-c)/(h-l).replace(0,np.nan),
                               "f1": c.shift(-1)/c-1, "f3": c.shift(-3)/c-1})
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for hh in (1,3):
        dr = D[D.pos % hh == 0].groupby("coin")[f"f{hh}"].mean()
        D[f"e{hh}"] = D[f"f{hh}"] - D["coin"].map(dr)
    def stat(sub, col):
        sub = sub.dropna(subset=[col]); n=len(sub)
        if n < 5: return pd.Series({"n": n, "mean%": np.nan, "t_day": np.nan, "days": 0})
        m = sub[col].mean(); g=(sub[col]-m).groupby(sub["ts"]).sum(); se=np.sqrt((g**2).sum())/n
        return pd.Series({"n": n, "mean%": 100*m, "t_day": m/se, "days": sub["ts"].nunique()})
    def slope(sub, x, y):
        sub = sub.dropna(subset=[x,y]); X=sub[x]-sub[x].mean(); Y=sub[y]
        b = (X*Y).sum()/(X**2).sum(); res = Y - Y.mean() - b*X
        g=(X*res).groupby(sub["ts"]).sum(); se=np.sqrt((g**2).sum())/(X**2).sum()
        return pd.Series({"n": len(sub), "slope": b, "t_day": b/se, "days": sub["ts"].nunique()})
    out = {}
    # continuation after flat days in a run: signed by run direction
    D["dir"] = np.sign(D["r5z"])
    D["cont1"] = D["dir"]*D["e1"]; D["cont3"] = D["dir"]*D["e3"]
    fl = D[(D.z.abs()<0.5) & (D.r5z.abs()>1)]
    out["flat in run: slope cont1 on rngz"] = slope(fl, "rngz", "cont1")
    out["flat in run: slope cont3 on rngz (grid3)"] = slope(fl[fl.pos%3==0], "rngz", "cont3")
    flr = fl.copy(); flr["rb"] = pd.qcut(flr.rngz, 4)
    out["flat in run: cont1 by range quartile x run dir"] = flr.groupby(["dir","rb"], observed=True).apply(lambda s: stat(s,"cont1"))
    out["flat in run top-range: cont1 by year"] = flr[flr.rngz>1.368].groupby("year").apply(lambda s: stat(s,"cont1"))
    # control: flat days NOT in run
    nr = D[(D.z.abs()<0.5) & (D.r5z.abs()<0.5)].copy(); nr["rb"]=pd.qcut(nr.rngz,4)
    out["flat no run: |e1|-type cont by r5 sign, range q"] = nr.groupby("rb", observed=True).apply(lambda s: stat(s,"cont1"))
    # all days in run: slope of cont1 on rngz
    allr = D[D.r5z.abs()>1]
    out["all run days: slope cont1 on rngz"] = slope(allr, "rngz", "cont1")
    out["all run days: slope cont1 on r5z abs"] = slope(allr.assign(a=allr.r5z.abs()), "a", "cont1")
    # sharp down by volatility regime (sd relative to its own 120d median)
    dn = D[D.z<=-2].copy()
    out["sharp down: slope e1 on sdrel"] = slope(dn, "sdrel", "e1")
    dn["vq"] = pd.qcut(dn.sdrel, 4)
    out["sharp down e1 by sdrel quartile"] = dn.groupby("vq", observed=True).apply(lambda s: stat(s,"e1"))
    out["sharp down e1 by year"] = dn.groupby("year").apply(lambda s: stat(s,"e1"))
    # all down days: next-day by sd relative
    d2 = D[D.z<=-1].copy(); d2["vq"]=pd.qcut(d2.sdrel,4)
    out["down days z<=-1: e1 by sdrel quartile"] = d2.groupby("vq", observed=True).apply(lambda s: stat(s,"e1"))
    out["down days z<=-1: slope e1 on -z"] = slope(d2.assign(a=-d2.z), "a", "e1")
    # book's best/worst days: what kind of day preceded
    Ds = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            Ds.append(d.assign(coin=coin, w=w))
    B = pd.concat(Ds, ignore_index=True)
    bk = B.groupby("day")["book_return"].mean().dropna()
    q = bk[bk!=0]
    out["book active days: count, mean%, share of gain top10"] = pd.Series({"n": len(q), "mean%": 100*q.mean(),
        "top10 share of total": q.nlargest(10).sum()/q.sum(), "bottom10 sum%": 100*q.nsmallest(10).sum(), "top10 sum%": 100*q.nlargest(10).sum()})
    return out

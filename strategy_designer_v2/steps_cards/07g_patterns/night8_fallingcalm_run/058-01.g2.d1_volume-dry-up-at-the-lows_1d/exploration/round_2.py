def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            n = len(b)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fc": b["forecast"].astype(float),
                "regime": b["regime"].astype(str),
                "r1": r1, "f1": c.shift(-1)/c-1, "f5": c.shift(-5)/c-1,
                "past60": (c/c.shift(60)-1)*100,
                "vol30": r1.rolling(30).std(),
                "clv": (c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
            })
            df["volrank"] = df["vol30"].rank(pct=True)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    mu1 = A.groupby("coin")["f1"].mean()
    mu5 = A.groupby("coin").apply(lambda d: d.loc[d.pos%5==0,"f5"].mean())
    A["x1"] = A["f1"]-A["coin"].map(mu1)
    A["x5"] = A["f5"]-A["coin"].map(mu5)
    A["trend"] = np.where(A.past60>10,"rising",np.where(A.past60<-10,"falling",np.where(A.past60.notna(),"choppy","na")))
    A["agit"] = np.where(A.volrank>0.5,"agit","calm")
    def ct(d, val):
        d = d.dropna(subset=[val])
        s = d.groupby("day")[val].apply(lambda x:(x-d[val].mean()).sum())
        G = len(s)
        if G<5: return np.nan
        se = np.sqrt((s**2).sum()*G/(G-1))/len(d)
        return d[val].mean()/se
    def tab(d, col, val, q=5):
        d = d.dropna(subset=[col,val]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        r = d.groupby("b").apply(lambda g: pd.Series({"n":len(g),"mean%":g[val].mean()*100,"t_day":ct(g,val)}))
        return r.round(3)
    D = A.dropna(subset=["clv","x1"])
    out["clv quintile, day-clustered t"] = tab(D,"clv","x1")
    for tr in ["rising","choppy","falling"]:
        out[f"clv quintile, trend {tr}"] = tab(D[D.trend==tr],"clv","x1")
    out["clv quintile, regime falling-calm"] = tab(D[D.regime=="unknown"],"clv","x1")
    # by window: top-clv quintile minus bottom
    q = D["clv"].quantile([0.2,0.8]).values
    W = D.assign(hi=D.clv>=q[1], lo=D.clv<=q[0])
    byw = W.groupby("win").apply(lambda g: pd.Series({"hi%":g.loc[g.hi,"x1"].mean()*100,"lo%":g.loc[g.lo,"x1"].mean()*100}))
    byw["hi_minus_lo"] = byw["hi%"]-byw["lo%"]
    out["clv hi/lo next-day by window"] = byw.round(3)
    byy = W.groupby(W.day.dt.year).apply(lambda g: pd.Series({"hi%":g.loc[g.hi,"x1"].mean()*100,"lo%":g.loc[g.lo,"x1"].mean()*100,"n_hi":g.hi.sum()}))
    out["clv hi/lo next-day by year"] = byy.round(3)
    # in-profile forecast strength by window
    U = A[(A.regime=="unknown")&(A.pos%5==0)&(A.fc<0)].dropna(subset=["x5"])
    med = U.fc.median()
    out["in-profile strong vs weak forecast by window"] = U.groupby("win").apply(lambda g: pd.Series({"n":len(g),"strong%":g.loc[g.fc<=med,"x5"].mean()*100,"weak%":g.loc[g.fc>med,"x5"].mean()*100})).round(3)
    out["in-profile strong-half t_day"] = float(ct(U[U.fc<=med],"x5"))
    out["in-profile weak-half t_day"] = float(ct(U[U.fc>med],"x5"))
    # short side: high-close next day by trend x agitation
    H = D[D.clv>=q[1]]
    out["top-clv next-day by trend x agit"] = H.groupby(["trend","agit"]).apply(lambda g: pd.Series({"n":len(g),"mean%":g.x1.mean()*100,"t_day":ct(g,"x1")})).round(3)
    return out

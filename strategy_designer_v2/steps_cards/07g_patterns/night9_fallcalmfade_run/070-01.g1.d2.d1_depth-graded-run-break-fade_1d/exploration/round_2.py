def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values; v = b["volume"].astype(float).values
            h = b["high"].astype(float).values; l = b["low"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:]/c[:-1]-1
            s = pd.Series(r)
            vol30 = s.rolling(30, min_periods=20).std().values
            vm20 = pd.Series(v).rolling(20, min_periods=10).mean().shift(1).values
            tr60 = np.full(n, np.nan); tr60[60:] = c[60:]/c[:-60]-1
            ts = pd.to_datetime(b["timestamp"])
            for t in range(1, n-1):
                if not (r[t] > 0): continue
                k = 0; j = t-1
                while j >= 1 and r[j] < 0:
                    k += 1; j -= 1
                if k < 2: continue
                runloss = -(c[t-1]/c[t-1-k]-1)
                f = {}
                for hz in (1, 2, 3):
                    f[hz] = c[t+hz]/c[t]-1 if t+hz < n else np.nan
                rows.append(dict(coin=coin, w=w, day=ts[t].normalize(), year=ts[t].year, k=k,
                                 runloss=runloss, r=r[t], vol=vol30[t], tr60=tr60[t],
                                 retr=r[t]/runloss if runloss > 0 else np.nan,
                                 vrel=v[t]/vm20[t] if vm20[t] > 0 else np.nan,
                                 rng=(h[t]-l[t])/c[t-1],
                                 ex1=-(f[1]-mu), ex2=-(f[2]-2*mu), ex3=-(f[3]-3*mu),
                                 pos=b["postRebalance_current_allocation"].iloc[t]))
    d = pd.DataFrame(rows).dropna(subset=["ex1"])
    def summ(g, col="ex1"):
        g = g.dropna(subset=[col])
        ds = g.groupby("day")[col].sum()
        t = ds.mean()/(ds.std()/np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(ds), mean=g[col].mean(), t_day=t))
    out = {}
    d["loss_z"] = d["runloss"]/(d["vol"]*np.sqrt(d["k"]))
    d["up_z"] = d["r"]/d["vol"]
    for col in ["runloss", "loss_z", "retr", "up_z", "vol", "vrel", "rng"]:
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col].rank(method="first"), 4, labels=["q1low", "q2", "q3", "q4high"])
        out["by "+col+" quartile"] = dd.groupby("q").apply(summ)
    out["horizons all events"] = pd.DataFrame({h: summ(d, h) for h in ["ex1", "ex2", "ex3"]}).T
    d["vq"] = pd.qcut(d["vol"].rank(method="first"), 2, labels=["lowvol", "highvol"])
    d["dq"] = d.groupby("vq")["runloss"].transform(lambda x: pd.qcut(x.rank(method="first"), 2, labels=False))
    out["vol half x runloss half within"] = d.groupby(["vq", "dq"]).apply(summ)
    d["rq"] = pd.qcut(d["retr"].rank(method="first"), 2, labels=False)
    out["retr half by year"] = d.dropna(subset=["retr"]).groupby(["year", "rq"]).apply(summ)
    out["corr ex1 with features (spearman)"] = d[["ex1", "runloss", "loss_z", "retr", "up_z", "vol", "vrel", "k"]].corr(method="spearman")["ex1"]
    return out

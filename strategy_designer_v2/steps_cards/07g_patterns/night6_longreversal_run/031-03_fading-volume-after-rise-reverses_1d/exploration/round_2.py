def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]

    def cases(h, lbv=30, lbp=14):
        rows = []
        for c in bars:
            drift_f = []
            for w, df in bars[c].items():
                cl = df["close"].values.astype(float)
                drift_f += [cl[t+h]/cl[t]-1 for t in range(0, len(cl)-h, h)]
            drift = np.mean(drift_f)
            for w, df in bars[c].items():
                cl = df["close"].values.astype(float)
                vol = df["volume"].values.astype(float)
                ts = pd.to_datetime(df["timestamp"]).values
                r1 = np.diff(np.log(cl))
                for t in range(0, len(cl)-h, h):
                    if t < max(lbv, lbp): continue
                    vr = np.log(vol[t-13:t+1].mean()/vol[t-lbv+1:t+1].mean())
                    past = cl[t]/cl[t-lbp]-1
                    sd = np.std(r1[t-lbv:t])
                    rows.append((c, w, ts[t], vr, past, sd, cl[t+h]/cl[t]-1-drift))
        d = pd.DataFrame(rows, columns=["coin","w","ts","lvr","past","sd","ex"])
        d["yr"] = pd.to_datetime(d["ts"]).dt.year
        d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
        d["pz"] = d["past"]/(d["sd"]*np.sqrt(14))
        return d

    def day_t(d, x):
        # slope of ex on standardized x, t with cases of one day summed
        xz = (d[x]-d[x].mean())/d[x].std()
        prod = xz*(d["ex"]-d["ex"].mean())
        s = prod.groupby(d["day"]).sum()
        n = len(s)
        return prod.sum()/len(d), s.mean()/(s.std()/np.sqrt(n)), n

    res = []
    for h in [7, 14]:
        d = cases(h)
        for x in ["lvr", "pz"]:
            b, t, n = day_t(d, x)
            res.append(dict(h=h, x=x, cov=b, t_day=t, days=n, cases=len(d)))
    out["clustered slopes"] = pd.DataFrame(res)

    d = cases(14)
    rows = []
    for c, g in d.groupby("coin"):
        s = stats.linregress(g["lvr"], g["ex"]); rows.append(dict(grp=c, n=len(g), t=s.slope/s.stderr))
    for y, g in d.groupby("yr"):
        s = stats.linregress(g["lvr"], g["ex"]); rows.append(dict(grp=str(y), n=len(g), t=s.slope/s.stderr))
    out["lvr 14d by coin and year"] = pd.DataFrame(rows)
    q = pd.qcut(d["lvr"], 5, labels=False)
    out["lvr quintile 14d"] = d.groupby(q).agg(lvr=("lvr","mean"), ex=("ex","mean"), n=("ex","size"))
    # lvr partial on past
    X = np.column_stack([np.ones(len(d)), d["lvr"], d["pz"]])
    beta, *_ = np.linalg.lstsq(X, d["ex"].values, rcond=None)
    resid = d["ex"].values - X@beta
    cov = np.linalg.inv(X.T@X)*resid.var(ddof=3)
    out["14d joint lvr,pz t"] = pd.Series({"t_lvr": beta[1]/np.sqrt(cov[1,1]), "t_pz": beta[2]/np.sqrt(cov[2,2])})
    d7 = cases(7)
    rows = []
    for c, g in d7.groupby("coin"):
        s = stats.linregress(g["pz"], g["ex"]); rows.append(dict(grp=c, n=len(g), t=s.slope/s.stderr))
    for y, g in d7.groupby("yr"):
        s = stats.linregress(g["pz"], g["ex"]); rows.append(dict(grp=str(y), n=len(g), t=s.slope/s.stderr))
    out["7d momentum by coin and year"] = pd.DataFrame(rows)

    # weekday: day-clustered (mean across coins per day)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({"day": ts.dt.floor("D"), "r": df["close"].astype(float).pct_change(), "yr": ts.dt.year}))
    a = pd.concat(rows).dropna()
    dm = a.groupby("day").agg(r=("r","mean"), yr=("yr","first")).reset_index()
    dm["wd"] = dm["day"].dt.weekday
    g = dm.groupby("wd")["r"].agg(["mean","std","size"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["weekday, day-mean"] = g
    sat = dm[dm.wd==5].groupby("yr")["r"].agg(["mean","size"])
    out["saturday by year"] = sat
    return out

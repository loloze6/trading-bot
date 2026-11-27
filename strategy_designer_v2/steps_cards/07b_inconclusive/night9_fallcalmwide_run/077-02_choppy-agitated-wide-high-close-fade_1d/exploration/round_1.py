def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].values
            allr.append(c[1:]/c[:-1]-1)
        drift[coin] = np.nanmean(np.concatenate(allr))
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            rng = (h-l)/c
            rr = (h-l)/(h-l).rolling(30, min_periods=30).mean()
            loc = (c-l)/(h-l).replace(0,np.nan)
            r1 = c.shift(-1)/c-1
            r2 = c.shift(-2)/c-1
            r3 = c.shift(-3)/c-1
            sd30 = (c/c.shift(1)-1).rolling(30).std()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year,"wd":ts.dt.weekday,
                "fc":df["forecast"],"regime":df["regime"],"rr":rr,"loc":loc,
                "rsd":(h-l)/c/sd30,"r1":r1,"r2":r2,"r3":r3,"dr":drift[coin],
                "day":ts.dt.floor("D")})
            rows.append(d)
    A = pd.DataFrame(pd.concat(rows, ignore_index=True))
    A["inprof"] = A["regime"]!="chop"
    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g)<3: return pd.Series({"n":len(g),"mean":np.nan,"t":np.nan,"days":0})
        dev = g.groupby("day")[col].sum()
        D=len(dev); m=g[col].mean()
        # clustered t
        resid = g[col]-m
        s = resid.groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum()*D/(D-1))/len(g)
        return pd.Series({"n":len(g),"mean":m,"t":m/se if se>0 else np.nan,"days":D})
    # short cases
    S = A[A["fc"]<=-2].copy()
    for k in [1,2,3]:
        S[f"u{k}"] = -(S[f"r{k}"]-k*S["dr"])
    out = {}
    out["short cases by horizon"] = pd.DataFrame({k:summ(S,f"u{k}") for k in ["u1","u2","u3"]}).T
    out["by coin"] = S.groupby("coin").apply(summ)
    out["by year"] = S.groupby("year").apply(summ)
    out["by window"] = S.groupby("w").apply(summ)
    S["fq"] = pd.qcut(S["fc"].abs().rank(method="first"),3,labels=["lo","mid","hi"])
    out["by |fc| tercile"] = S.groupby("fq").apply(summ)
    S["rq"] = pd.qcut(S["rsd"].rank(method="first"),3,labels=["lo","mid","hi"])
    out["by width-in-std tercile"] = S.groupby("rq").apply(summ)
    S["lq"] = pd.qcut(S["loc"].rank(method="first"),3,labels=["lo","mid","hi"])
    out["by close loc tercile"] = S.groupby("lq").apply(summ)
    out["corr u1 with rsd, loc, |fc|"] = pd.Series({
        "rsd": S[["u1","rsd"]].corr().iloc[0,1],"loc":S[["u1","loc"]].corr().iloc[0,1],
        "absfc":S[["u1","fc"]].assign(fc=S["fc"].abs()).corr().iloc[0,1]})
    # low-close mirror in profile (long)
    L = A[A["inprof"] & (A["rr"]>=1) & (A["loc"]<=0.25)].copy()
    for k in [1,2,3]:
        L[f"u{k}"] = (L[f"r{k}"]-k*L["dr"])
    out["low-close mirror, long, by horizon"] = pd.DataFrame({k:summ(L,f"u{k}") for k in ["u1","u2","u3"]}).T
    # high close in profile, all (regime mean_reversion) vs cases
    H = A[A["inprof"] & (A["rr"]>=1) & (A["loc"]>=0.75)].copy()
    H["u1"] = -(H["r1"]-H["dr"])
    out["high-close in profile, all"] = summ(H)
    # same situation outside profile
    O = A[(~A["inprof"]) & (A["rr"]>=1) & (A["loc"]>=0.75)].copy()
    O["u1"] = -(O["r1"]-O["dr"])
    out["high-close outside profile"] = summ(O)
    return out

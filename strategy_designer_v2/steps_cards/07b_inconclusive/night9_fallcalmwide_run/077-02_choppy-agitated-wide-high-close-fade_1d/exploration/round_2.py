def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            allr.append(c[1:]/c[:-1]-1)
        drift[coin] = np.nanmean(np.concatenate(allr))
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            hl = (h-l)
            rr = hl/hl.rolling(30, min_periods=30).mean()
            loc = (c-l)/hl.replace(0,np.nan)
            sd30 = (c/c.shift(1)-1).rolling(30).std()
            tr60 = (c/c.shift(60)-1)*100
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values,"wd":ts.dt.weekday.values,
                "fc":df["forecast"].values,"regime":df["regime"].astype(str).values,"rr":rr.values,"loc":loc.values,
                "rsd":(hl/c/sd30).values,"tr60":tr60.values,
                "r1":(c.shift(-1)/c-1).values,"r2":(c.shift(-2)/c-1).values,"r3":(c.shift(-3)/c-1).values,
                "dr":drift[coin],"day":ts.dt.floor("D").values})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A["regime"]!="chop"
    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g)<3: return pd.Series({"n":len(g),"mean":np.nan,"t":np.nan,"days":len(g)})
        m=g[col].mean()
        s = (g[col]-m).groupby(g["day"]).sum()
        D=len(s)
        se = np.sqrt((s**2).sum()*D/max(D-1,1))/len(g)
        return pd.Series({"n":len(g),"mean":m,"t":m/se if se>0 else np.nan,"days":D})
    def grp(df, key, col="u1"):
        return pd.DataFrame({k: summ(g, col) for k, g in df.groupby(key)}).T
    S = A[A["fc"]<=-2].copy()
    for k in [1,2,3]:
        S[f"u{k}"] = -(S[f"r{k}"]-k*S["dr"])
    out = {}
    out["short cases by horizon"] = pd.DataFrame({f"u{k}":summ(S,f"u{k}") for k in [1,2,3]}).T
    out["by coin"] = grp(S,"coin")
    out["by year"] = grp(S,"year")
    out["by window"] = grp(S,"w")
    S["fq"] = pd.qcut(S["fc"].abs().rank(method="first"),3,labels=["lo","mid","hi"]).astype(str)
    out["by |fc| tercile"] = grp(S,"fq")
    S["rq"] = pd.qcut(S["rsd"].rank(method="first"),3,labels=["lo","mid","hi"]).astype(str)
    out["by width-in-std tercile"] = grp(S,"rq")
    S["lq"] = pd.qcut(S["loc"].rank(method="first"),3,labels=["lo","mid","hi"]).astype(str)
    out["by close loc tercile"] = grp(S,"lq")
    S["tq"] = pd.qcut(S["tr60"].rank(method="first"),3,labels=["lo","mid","hi"]).astype(str)
    out["by 60d trend tercile"] = grp(S,"tq")
    out["corr u1 with rsd, loc, |fc|, rr"] = pd.Series({
        "rsd": S["u1"].corr(S["rsd"]),"loc":S["u1"].corr(S["loc"]),
        "absfc":S["u1"].corr(S["fc"].abs()),"rr":S["u1"].corr(S["rr"])})
    out["median u1, share positive"] = pd.Series({"median":S["u1"].median(),"share_pos":(S["u1"]>0).mean()})
    L = A[A["inprof"] & (A["rr"]>=1) & (A["loc"]<=0.25)].copy()
    for k in [1,2,3]:
        L[f"u{k}"] = (L[f"r{k}"]-k*L["dr"])
    out["low-close mirror in profile, long"] = pd.DataFrame({f"u{k}":summ(L,f"u{k}") for k in [1,2,3]}).T
    O = A[(~A["inprof"]) & (A["rr"]>=1) & (A["loc"]>=0.75)].copy()
    O["u1"] = -(O["r1"]-O["dr"])
    out["high-close outside profile, short u1"] = summ(O)
    return out

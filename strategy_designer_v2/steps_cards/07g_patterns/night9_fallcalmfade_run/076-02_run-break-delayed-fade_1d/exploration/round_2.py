def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            run = np.zeros(n); dn = 0
            for i in range(1, n):
                if r1[i] < 0: dn += 1
                elif r1[i] > 0: run[i] = dn; dn = 0
                else: dn = 0
            def back(k):
                x = np.full(n, np.nan); x[k:] = c[k:]/c[:-k]-1; return x
            def fwd(a, z):
                x = np.full(n, np.nan); x[:n-z] = c[z:]/c[a:n-z+a]-1; return x
            sd20 = pd.Series(r1).rolling(20, min_periods=10).std().values
            sd60 = pd.Series(r1).rolling(60, min_periods=40).std().values
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame(dict(coin=coin, w=w, pos=np.arange(n), run=run, r1=r1,
                r20=back(20), r40=back(40), f1=fwd(0,1), f3=fwd(0,3), f23=fwd(1,3), f5=fwd(0,5),
                ag=sd20/sd60, day=ts.dt.floor("D").values)))
    D = pd.concat(rows, ignore_index=True)
    G3 = D[D.pos % 3 == 0]
    dr = {k: G3.groupby("coin")[k].mean() for k in ["f1","f3","f23"]}
    dr["f5"] = D[D.pos % 5 == 0].groupby("coin")["f5"].mean()
    for k in dr: D["x"+k] = D[k] - D["coin"].map(dr[k])
    def summ(g, col):
        g = g[g[col].notna()]; x = g[col]; m = x.mean()
        se = np.sqrt(((x-m).groupby(g["day"]).sum()**2).sum())/len(x)
        return pd.Series(dict(n=len(x), days=g.day.nunique(), mean=m, t=m/se if se>0 else np.nan))
    def slope(g, col):
        g = g[g[col].notna()]; X = g["run"].values; y = g[col].values
        b = np.polyfit(X, y, 1)[0]; res = y - np.polyval(np.polyfit(X,y,1), X)
        se = np.sqrt((res**2).sum()/(len(y)-2)/((X-X.mean())**2).sum())
        return pd.Series(dict(n=len(y), slope=b, t=b/se))
    out = {}
    B = D[(D.pos % 3 == 0) & (D.run >= 1)].copy()
    B["runc"] = B.run.clip(upper=4)
    B["tr"] = np.select([B.r40 < -0.10, B.r40 > 0.10], ["falling", "rising"], "choppy")
    B.loc[B.r40.isna(), "tr"] = "na"
    for col in ["xf1", "xf23", "xf3"]:
        out[f"breaks {col} by 40d trend x run"] = B.groupby(["tr","runc"]).apply(lambda g: summ(g,col)).round(4)
    out["slope xf3 on run, by trend"] = B.groupby("tr").apply(lambda g: slope(g,"xf3")).round(4)
    B["agh"] = np.where(B.ag > 1, "agit", "calm")
    F = B[B.r20 < 0]
    out["20d-falling breaks xf3 by agitation x run"] = F.groupby(["agh","runc"]).apply(lambda g: summ(g,"xf3")).round(4)
    out["20d-falling breaks slope xf3 by window half"] = F.assign(h=F.w.str[1:].astype(int) <= 12).groupby("h").apply(lambda g: slope(g,"xf3")).round(4)
    out["20d-falling run>=2 xf3 by window"] = F[F.run>=2].groupby("w").apply(lambda g: summ(g,"xf3")).round(4)
    B5 = D[(D.pos % 5 == 0) & (D.run >= 1) & (D.r20 < 0)].copy(); B5["runc"] = B5.run.clip(upper=4)
    out["20d-falling breaks xf5 by run"] = B5.groupby("runc").apply(lambda g: summ(g,"xf5")).round(4)
    return out

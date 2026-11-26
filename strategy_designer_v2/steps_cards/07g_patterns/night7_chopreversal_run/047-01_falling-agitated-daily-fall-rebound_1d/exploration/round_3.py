def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); pc = c.shift(1)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "rn": c.shift(-1)/c - 1, "rn2": c.shift(-2)/c.shift(-1) - 1,
                "inp": (b["regime"] != "chop").astype(int),
            })
            ma = r.abs().rolling(60, min_periods=20).mean()
            rg = (b["high"]-b["low"])/pc
            d["z"] = r/ma
            d["zr"] = rg/rg.rolling(60, min_periods=20).mean()
            d["wick_up"] = (b["high"]-np.maximum(c, b["open"]))/pc/ma
            d["wick_dn"] = (np.minimum(c, b["open"])-b["low"])/pc/ma
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["rn"].mean()
    D["xn"] = D["rn"] - D["coin"].map(drift)
    D["xn2"] = D["rn2"] - D["coin"].map(drift)
    D = D.dropna(subset=["z", "xn", "zr"])

    def ct(g, col="xn"):
        g = g.dropna(subset=[col]); m = g[col].mean()
        s = (g[col]-m).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum())/len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean%": 100*m, "t": m/se})

    def reg(g, xs):
        g = g.dropna(subset=xs+["xn"]).reset_index(drop=True)
        X = np.column_stack([np.ones(len(g))]+[g[x].values for x in xs]); y = g["xn"].values
        XtXi = np.linalg.inv(X.T@X); bt = XtXi@X.T@y; e = y-X@bt
        S = np.zeros((X.shape[1],)*2)
        for _, idx in g.groupby("day").indices.items():
            s = (X[idx]*e[idx,None]).sum(0); S += np.outer(s,s)
        G = g["day"].nunique(); N = len(g); K = X.shape[1]
        V = XtXi@S@XtXi*G/(G-1)*(N-1)/(N-K)
        return pd.DataFrame({"coef%":100*bt,"t":bt/np.sqrt(np.diag(V))}, index=["const"]+xs).assign(n=N, days=G)

    out = {}
    for name, sub in [("in_up", D[(D.inp==1)&(D.z>0)]), ("out_up", D[(D.inp==0)&(D.z>0)]),
                      ("in_dn", D[(D.inp==1)&(D.z<0)]), ("in_all", D[D.inp==1])]:
        sub = sub.copy()
        sub["rq"] = sub.groupby("coin")["zr"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
        out[name+"_by_range_tercile"] = sub.groupby("rq").apply(ct)
    U = D[(D.inp==1)&(D.z>0)].copy()
    out["in_up_wickup"] = reg(U, ["z", "wick_up"])
    out["in_up_wickup_day2"] = U.assign(xn=U["xn2"]).pipe(lambda g: reg(g, ["z", "wick_up"]))
    out["in_all_range"] = reg(D[D.inp==1], ["z", "zr"])
    Dn = D[(D.inp==1)&(D.z<0)].copy()
    out["in_dn_wickdn"] = reg(Dn, ["z", "wick_dn"])
    return out

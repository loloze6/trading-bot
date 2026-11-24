def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                if c[i] > c[i-1]:
                    up[i] = up[i-1] + 1
                elif c[i] < c[i-1]:
                    dn[i] = dn[i-1] + 1
            reg = b["regime"].astype(str).values
            for i in range(n):
                rec = {"coin": coin, "wn": int(w[1:]), "i": i, "ts": b["timestamp"].iloc[i],
                       "fc": b["forecast"].iloc[i], "trend": reg[i] == "trending",
                       "up": up[i], "dn": dn[i]}
                for h in (5, 10, 20):
                    rec[f"f{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                    rec[f"g{h}"] = (i % h == 0)
                rows.append(rec)
    df = pd.DataFrame(rows)
    df["fold"] = pd.cut(df["wn"], [0,6,12,18,24], labels=["A","B","C","D"])
    for h in (5,10,20):
        m = df[df[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        df[f"u{h}"] = df[f"f{h}"] - df["coin"].map(m)
    def cl_slope(d, y, x):
        d = d.dropna(subset=[y, x])
        if len(d) < 20 or d[x].std() == 0: return (np.nan, np.nan, len(d))
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        XtXi = np.linalg.inv(X.T @ X); beta = XtXi @ X.T @ Y; e = Y - X @ beta
        meat = np.zeros((2,2)); G = 0
        for _, idx in d.groupby("ts").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s); G += 1
        n = len(d); k = 2
        V = XtXi @ meat @ XtXi * (G/(G-1)) * ((n-1)/(n-k))
        return (beta[1], beta[1]/np.sqrt(V[1,1]), n)
    out = {}
    # A: down streak inside uptrend (dip continuation in uptrend -> rebound)
    T = df[df["trend"]]
    rs = []
    for h in (5,10,20):
        g = T[T[f"g{h}"]]
        s,t,n = cl_slope(g, f"u{h}", "dn"); rs.append(("trend_dn_all", h, s, t, n))
        s,t,n = cl_slope(g.assign(dc=g["dn"].clip(upper=5)), f"u{h}", "dc"); rs.append(("trend_dn_cap5", h, s, t, n))
        gg = g[g["dn"]>0]
        s,t,n = cl_slope(gg, f"u{h}", "dn"); rs.append(("trend_dn_pos_only", h, s, t, n))
    N = df[~df["trend"]]
    for h in (5,10,20):
        g = N[N[f"g{h}"]]
        s,t,n = cl_slope(g.assign(uc=g["up"].clip(upper=5)), f"u{h}", "uc"); rs.append(("nontrend_up_cap5", h, s, t, n))
        s,t,n = cl_slope(g.assign(dc=g["dn"].clip(upper=5)), f"u{h}", "dc"); rs.append(("nontrend_dn_cap5", h, s, t, n))
    out["slopes"] = pd.DataFrame(rs, columns=["x","h","slope","t","n"])
    g = T[T["g20"]].assign(dc=lambda d: d["dn"].clip(upper=5))
    rr = []
    for f, gg in g.groupby("fold"):
        s,t,n = cl_slope(gg, "u20", "dc"); rr.append((f, s, t, n))
    out["trend_dn_by_fold_h20"] = pd.DataFrame(rr, columns=["fold","slope","t","n"])
    rr = []
    for f, gg in g.groupby("coin"):
        if len(gg) < 15: continue
        s,t,n = cl_slope(gg, "u20", "dc"); rr.append((f, s, t, n))
    cc = pd.DataFrame(rr, columns=["coin","slope","t","n"])
    out["trend_dn_coins_pos_share"] = float((cc["slope"]>0).mean())
    out["trend_dn_coins_n"] = len(cc)
    # 10-day continuation of positive forecast by fold
    g10 = T[T["g10"] & (T["fc"]>0)]
    rr = []
    for f, gg in g10.groupby("fold"):
        s,t,n = cl_slope(gg, "u10", "fc"); rr.append((f, s, t, n, gg["u10"].mean()))
    out["fcpos_h10_by_fold"] = pd.DataFrame(rr, columns=["fold","slope","t","n","mean_u10"])
    # down-close bar in trend vs up-close bar in trend, 20d unusual move, cluster t of mean
    g20 = T[T["g20"]].dropna(subset=["u20"])
    def mt(s):
        d = s.groupby(level=0).sum() if False else s
        return s.mean()/(s.std()/np.sqrt(len(s)))
    res = []
    for lab, m in [("dn>=1", g20["dn"]>=1), ("up>=1", g20["up"]>=1), ("dn>=2", g20["dn"]>=2)]:
        x = g20[m]
        dsum = x.groupby("ts")["u20"].sum()
        res.append((lab, x["u20"].mean(), len(x), dsum.mean()/(dsum.std()/np.sqrt(len(dsum))), len(dsum)))
    out["trend_means"] = pd.DataFrame(res, columns=["sit","mean_u20","n","t_day","days"])
    return out

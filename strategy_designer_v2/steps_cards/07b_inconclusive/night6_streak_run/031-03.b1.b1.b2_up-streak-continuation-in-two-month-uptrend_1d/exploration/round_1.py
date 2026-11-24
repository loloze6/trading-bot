def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            # up streak length from closes (within window)
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                if c[i] > c[i-1]:
                    up[i] = up[i-1] + 1
                elif c[i] < c[i-1]:
                    dn[i] = dn[i-1] + 1
            r30 = pd.Series(c).pct_change(30).values
            r60 = pd.Series(c).pct_change(60).values
            reg = b["regime"].astype(str).values
            for i in range(n):
                rec = {"coin": coin, "w": w, "wn": int(w[1:]), "i": i, "ts": b["timestamp"].iloc[i],
                       "fc": b["forecast"].iloc[i], "trend": reg[i] == "trending",
                       "up": up[i], "dn": dn[i], "r30": r30[i], "r60": r60[i]}
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
        if len(d) < 20: return (np.nan, np.nan, len(d))
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        XtXi = np.linalg.inv(X.T @ X); beta = XtXi @ X.T @ Y; e = Y - X @ beta
        meat = np.zeros((2,2)); G = 0
        for _, idx in d.groupby("ts").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s); G += 1
        n = len(d); k = 2
        V = XtXi @ meat @ XtXi * (G/(G-1)) * ((n-1)/(n-k))
        return (beta[1], beta[1]/np.sqrt(V[1,1]), n)
    out = {}
    T = df[df["trend"]]
    rs = []
    for h in (5,10,20):
        g = T[T[f"g{h}"]]
        s, t, n = cl_slope(g, f"u{h}", "fc"); rs.append(("fc", h, s, t, n))
        s, t, n = cl_slope(g, f"u{h}", "up"); rs.append(("raw_up", h, s, t, n))
        gp = g[g["fc"] > 0]
        s, t, n = cl_slope(gp, f"u{h}", "fc"); rs.append(("fc_pos_only", h, s, t, n))
    out["slopes_by_horizon"] = pd.DataFrame(rs, columns=["x","h","slope","t","n"])
    g = T[T["g20"]].copy()
    g["fbin"] = pd.cut(g["fc"], [-0.1, 0.01, 8, 12, 16, 20.1])
    out["trend_u20_by_fc_bin"] = g.groupby("fbin")["u20"].agg(["mean","count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    g["ubin"] = pd.cut(g["up"], [-0.1, 0.5, 1.5, 2.5, 3.5, 30])
    out["trend_u20_by_rawup"] = g.groupby("ubin")["u20"].agg(["mean","count"])
    rr = []
    for f, gg in g.groupby("fold"):
        s, t, n = cl_slope(gg, "u20", "fc"); rr.append((f, s, t, n, gg["u20"].mean()))
    out["trend_slope_by_fold"] = pd.DataFrame(rr, columns=["fold","slope","t","n","mean_u20"])
    rr = []
    for f, gg in g.groupby("coin"):
        s, t, n = cl_slope(gg, "u20", "fc"); rr.append((f, s, t, n, gg["u20"].mean()))
    out["trend_slope_by_coin"] = pd.DataFrame(rr, columns=["coin","slope","t","n","mean_u20"])
    # all bars, raw streaks, both sides, outside and inside trend
    a = df[df["g20"]].copy()
    a["ub"] = pd.cut(a["up"], [-0.1,0.5,1.5,2.5,3.5,30]); a["db"] = pd.cut(a["dn"], [-0.1,0.5,1.5,2.5,3.5,30])
    out["all_u20_by_up"] = a.groupby(["trend","ub"])["u20"].agg(["mean","count"])
    out["all_u20_by_dn"] = a.groupby(["trend","db"])["u20"].agg(["mean","count"])
    # trend strength grading
    g["r60b"] = pd.qcut(g["r60"], 4)
    out["trend_u20_by_r60q"] = g.groupby("r60b")["u20"].agg(["mean","count"])
    return out

def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    H = [1, 3, 5, 10]
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                up[i] = up[i-1] + 1 if ret1[i] > 0 else 0
                dn[i] = dn[i-1] + 1 if ret1[i] < 0 else 0
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n):
                r = {"coin": coin, "win": w, "i": i, "year": ts[i].year, "day": ts[i].normalize(),
                     "up": up[i], "dn": dn[i], "fc": df["forecast"].iloc[i]}
                # prior 5d return
                r["past5"] = c[i] / c[i-5] - 1 if i >= 5 else np.nan
                for h in H:
                    if i + h < n:
                        r[f"f{h}"] = c[i+h] / c[i] - 1 - drift[(coin, h)]
                        r[f"tot{h}"] = c[i+h] / c[i] - 1
                    else:
                        r[f"f{h}"] = np.nan
                rows.append(r)
    D = pd.DataFrame(rows)

    def clt(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return (len(s), np.nan, np.nan)
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g**2).sum() * G / (G - 1)) / len(s)
        return (len(s), m, m / se)

    # grid per horizon: positions multiple of h
    res = []
    for h in H:
        G = D[D["i"] % h == 0]
        for name, sub in [("up>=1", G[G.up >= 1]), ("up1", G[G.up == 1]), ("up2", G[G.up == 2]),
                          ("up3", G[G.up == 3]), ("up4+", G[G.up >= 4]),
                          ("dn1", G[G.dn == 1]), ("dn2", G[G.dn == 2]), ("dn3", G[G.dn == 3]), ("dn4+", G[G.dn >= 4]),
                          ("all", G)]:
            n, m, t = clt(sub, f"f{h}")
            res.append({"h": h, "grp": name, "n": n, "mean_unusual_fwd(long dir)": m, "t": t})
    out["by streak & horizon (fwd unusual, long sign)"] = pd.DataFrame(res)

    G5 = D[(D["i"] % 5 == 0) & (D.up >= 1)]
    rc = []
    for coin, s in G5.groupby("coin"):
        n, m, t = clt(s, "f5"); rc.append({"coin": coin, "n": n, "mean": m, "t": t})
    out["up>=1 h5 by coin"] = pd.DataFrame(rc)
    ry = []
    for y, s in G5.groupby("year"):
        n, m, t = clt(s, "f5"); ry.append({"year": y, "n": n, "mean": m, "t": t})
    out["up>=1 h5 by year"] = pd.DataFrame(ry)
    # by past5 return tercile among up days
    G5 = G5.dropna(subset=["past5"])
    G5["q"] = G5.groupby("coin")["past5"].transform(lambda x: pd.qcut(x, 3, labels=False))
    rq = []
    for q, s in G5.groupby("q"):
        n, m, t = clt(s, "f5"); rq.append({"past5_tercile": q, "n": n, "mean": m, "t": t, "mean_streak": s.up.mean()})
    out["up>=1 h5 by past5 tercile"] = pd.DataFrame(rq)
    out["corr streak vs fc on up days"] = float(D[D.up >= 1][["up", "fc"]].corr().iloc[0, 1])
    return out

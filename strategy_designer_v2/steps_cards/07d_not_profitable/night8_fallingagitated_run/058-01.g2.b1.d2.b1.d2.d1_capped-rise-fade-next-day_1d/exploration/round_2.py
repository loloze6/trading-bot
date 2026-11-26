def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}
    for c, ws in data["bars"].items():
        drift[c] = pd.concat([b["close"].pct_change().dropna() for b in ws.values()]).mean()
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change(); sd = r.rolling(30).std(); z = r / sd
            reg = b["regime"].astype(str)
            df = pd.DataFrame({"coin": c, "win": w, "z": z, "day": b["timestamp"].astype(str).str[:10],
                               "inprof": reg.isin(["mean_reversion", "unknown"]),
                               "alloc": b["postRebalance_current_allocation"], "idx": b.index,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for h in (1, 2, 3, 4, 5):
                df[f"f{h}"] = -(cl.shift(-h) / cl - 1 - h * drift[c])
                df[f"tot{h}"] = -(cl.shift(-h) / cl - 1)
                df[f"usual{h}"] = np.nan
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # usual move per coin per horizon on non-overlapping grid
    for h in (1, 2, 3, 4, 5):
        u = d[d.idx % h == 0].groupby("coin")[f"tot{h}"].std()
        d[f"usual{h}"] = d["coin"].map(u)

    def clus(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 3: return (np.nan, len(s), np.nan, 0)
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / max(G - 1, 1)) / len(s)
        return (m, len(s), m / se, G)

    res = []
    for h in (1, 2, 3, 4, 5):
        p = d[d.inprof]  # case bars: every up day (signal bar), not gridded since each case is own signal
        for name, cond in [("z 0-0.5", (p.z > 0) & (p.z <= 0.5)), ("z 0.5-1", (p.z > 0.5) & (p.z <= 1)),
                           ("z 0-1", (p.z > 0) & (p.z <= 1)), ("z >0.5", p.z > 0.5), ("z >1", p.z > 1),
                           ("z >0", p.z > 0)]:
            s = p[cond]
            m, n, t, G = clus(s, f"f{h}")
            tot = s[f"tot{h}"].mean()
            strength = (s[f"f{h}"] / s[f"usual{h}"]).mean()
            res.append({"h": h, "case": name, "unusual": m, "total": tot, "strength": strength, "n": n, "t_day": t, "days": G})
    out["in profile, short side, every signal bar, clustered t"] = pd.DataFrame(res)
    # outside profile same for z>0.5, h=3 (condition check)
    q = d[~d.inprof]
    res2 = []
    for h in (1, 3):
        for name, cond in [("z 0-1", (q.z > 0) & (q.z <= 1)), ("z >0.5", q.z > 0.5)]:
            m, n, t, G = clus(q[cond], f"f{h}")
            res2.append({"h": h, "case": name, "unusual": m, "n": n, "t_day": t})
    out["outside profile"] = pd.DataFrame(res2)
    # stability by year: z>0.5 h=3 in profile
    p = d[d.inprof & (d.z > 0.5)]
    out["in prof z>0.5 h=3 by year"] = p.groupby("year")["f3"].agg(["mean", "count"])
    out["in prof z>0.5 h=3 by window"] = p.groupby("win")["f3"].agg(["mean", "count"])
    p1 = d[d.inprof & (d.z > 0) & (d.z <= 1)]
    out["in prof z0-1 h=1 by year"] = p1.groupby("year")["f1"].agg(["mean", "count"])
    # allocation size by z bin on active bars
    a = d[d.inprof & (d.z > 0)]
    a = a.assign(zb=pd.cut(a.z, [0, 0.25, 0.5, 0.75, 1, 10]))
    out["abs alloc by z bin (in profile up days)"] = a.groupby("zb", observed=True)["alloc"].apply(lambda x: x.abs().mean())
    out["share of in-profile up days with |alloc|<0.05"] = float((a[(a.z <= 1)]["alloc"].abs() < 0.05).mean())
    return out

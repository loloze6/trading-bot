def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=15).std()
            fwd = c.shift(-H) / c - 1
            dn = (r1 < 0).astype(int)
            grp = (dn != dn.shift()).cumsum()
            drun = dn.groupby(grp).cumsum() * dn
            # cumulative log return of current down run, in sd units
            lr = np.log(c / c.shift(1)).where(dn == 1, 0.0)
            druncum = lr.groupby(grp).cumsum() * dn
            drz = druncum / sd30
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            lowclose_run = (clpos < 0.5).astype(int)
            g2 = (lowclose_run != lowclose_run.shift()).cumsum()
            lcrun = lowclose_run.groupby(g2).cumsum() * lowclose_run
            df = pd.DataFrame({
                "coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "inprof": b["regime"].astype(str) != "chop",
                "fwd": fwd, "drun": drun, "drz": drz, "clpos": clpos, "lcrun": lcrun,
                "book": b["postRebalance_total_value"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    allgrid = d[d["pos"] % H == 0].dropna(subset=["fwd"])
    drift = allgrid.groupby("coin")["fwd"].mean()
    d["su"] = -(d["fwd"] - d["coin"].map(drift))
    out = {}
    def tt(v):
        v = v.dropna(); n = len(v)
        return pd.Series({"n": n, "mean": v.mean(), "t": v.mean()/(v.std()/np.sqrt(n)) if n > 2 else np.nan})
    # by grid offset, down-run bucket and clpos bucket, in profile
    res_dr = {}; res_cl = {}; res_sp = {}
    for off in range(H):
        g = d[(d["pos"] % H == off) & d["inprof"]].dropna(subset=["fwd"])
        res_dr[off] = g.groupby(g["drun"].clip(upper=2))["su"].apply(lambda s: s.mean())
        res_cl[off] = g.groupby(pd.cut(g["clpos"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=False))["su"].mean()
        s = g[["drz", "su"]].dropna()
        s = s[s["drz"] < 0]
        res_sp[off] = pd.Series({"spearman drz(neg) vs su": stats.spearmanr(-s["drz"], s["su"])[0], "n": len(s)})
    out["drun bucket mean su by offset"] = pd.DataFrame(res_dr)
    out["clpos bucket mean su by offset"] = pd.DataFrame(res_cl)
    out["down-run depth spearman by offset"] = pd.DataFrame(res_sp)
    g = d[(d["pos"] % H == 0) & d["inprof"]].dropna(subset=["fwd"])
    out["drun>=2 by coin"] = g[g["drun"] >= 2].groupby("coin")["su"].apply(tt).unstack()
    out["drun>=2 early vs late windows"] = g[g["drun"] >= 2].groupby(g["wn"] >= 15)["su"].apply(tt).unstack()
    out["drun 0 vs >=1 out of profile"] = d[(d["pos"] % H == 0) & ~d["inprof"]].dropna(subset=["fwd"]).groupby(lambda i: min(d.loc[i, "drun"], 2))["su"].apply(tt).unstack()
    q = g[g["drz"] < 0].copy()
    q["b"] = pd.qcut(-q["drz"], 3, labels=False, duplicates="drop")
    out["in prof, down days: depth tercile of run (sd units)"] = q.groupby("b")["su"].apply(tt).unstack()
    out["lcrun bucket"] = g.groupby(g["lcrun"].clip(upper=3))["su"].apply(tt).unstack()
    return out

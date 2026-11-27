def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values.astype(float); allr.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); h = b["high"].values.astype(float); l = b["low"].values.astype(float)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            n1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            n2 = np.r_[c[2:]/c[:-2]-1, [np.nan]*2]
            dr = np.zeros(len(c))
            for i in range(1, len(c)):
                dr[i] = dr[i-1]+1 if r[i] < 0 else 0
            pdr = np.r_[0, dr[:-1]]
            tr60 = np.r_[[np.nan]*60, c[60:]/c[:-60]-1]
            vol = pd.Series(r).rolling(20, min_periods=10).std().shift(1).values
            runret = np.full(len(c), np.nan)
            for i in range(len(c)):
                k = int(pdr[i])
                if k >= 1 and i-1-k >= 0: runret[i] = c[i-1]/c[i-1-k]-1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D").values,
                "fc": b["regime"].eq("unknown").values, "r": r, "n1x": n1-mu, "n2x": n2-2*mu,
                "pdr": pdr, "tr": tr60, "rz": r/vol, "runz": runret/(vol*np.sqrt(np.maximum(pdr,1))),
                "rundepth": runret/vol,
                "clpos": (c-l)/np.where(h-l > 0, h-l, np.nan)}))
    D = pd.concat(rows, ignore_index=True)
    def cl(g, col="n1x"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = g[col].mean(); dv = (g[col]-m).groupby(g["day"]).sum()
        G = len(dv); se = np.sqrt((dv**2).sum()*G/(G-1))/len(g)
        return pd.Series({"n": len(g), "days": G, "mean": m, "t": m/se})
    out = {}
    brk = D[(D.r > 0) & (D.pdr >= 1)].copy()
    brk["trend"] = np.where(brk.tr > .10, "rising", np.where(brk.tr < -.10, "falling", np.where(brk.tr.notna(), "choppy", "na")))
    brk["runcls"] = np.clip(brk.pdr, 1, 4)
    out["nonfc_break_by_trend_run"] = brk[~brk.fc].groupby(["trend", "runcls"]).apply(cl).round(4)
    out["fc_break_by_run_clustered"] = brk[brk.fc].groupby("runcls").apply(cl).round(4)
    out["fc_break_by_run_n2"] = brk[brk.fc].groupby("runcls").apply(lambda g: cl(g, "n2x")).round(4)
    f = brk[brk.fc].copy()
    f["dq"] = pd.qcut(f.rundepth.rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["fc_break_by_run_depth"] = f.groupby("dq").apply(cl).round(4)
    f["clq"] = pd.qcut(f.clpos.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["fc_break_by_closepos_clustered"] = f.groupby("clq").apply(cl).round(4)
    out["fc_break_run2p_by_closepos"] = f[f.pdr >= 2].groupby("clq").apply(cl).round(4)
    # all up days in fc by close position (not only breaks)
    u = D[D.fc & (D.r > 0)].copy()
    u["clq"] = pd.qcut(u.clpos.rank(method="first"), 3, labels=["low", "mid", "high"])
    u["isbrk"] = u.pdr >= 1
    out["fc_upday_by_closepos_isbreak"] = u.groupby(["isbrk", "clq"]).apply(cl).round(4)
    # nonfc break run2+ in rising, by year
    nf = brk[(~brk.fc) & (brk.pdr >= 2)].copy(); nf["yr"] = pd.to_datetime(nf.day).dt.year
    out["nonfc_break2p_by_year"] = nf.groupby("yr").apply(cl).round(4)
    # nonfc big down days by trend
    dd = D[(~D.fc) & (D.rz <= -2)].copy()
    dd["trend"] = np.where(dd.tr > .10, "rising", np.where(dd.tr < -.10, "falling", np.where(dd.tr.notna(), "choppy", "na")))
    out["nonfc_bigdown_by_trend"] = dd.groupby("trend").apply(cl).round(4)
    return out

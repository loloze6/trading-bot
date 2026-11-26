def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]

    def ctt(df, col="ex"):
        # day-clustered t of mean: sum deviations per day
        x = df[col]; m = x.mean()
        g = (x - m).groupby(df["day"]).sum()
        G = len(g)
        if G < 3: return np.nan, G
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return m / se, G

    allC = {}
    for H in [7, 14, 21, 28]:
        cases = []
        for c in bars:
            allg = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl) - H, H):
                    allg.append(cl[i + H] / cl[i] - 1)
            mu = np.mean(allg)
            for w, b in bars[c].items():
                cl = b["close"].values; v = b["volume"].values
                ts = pd.to_datetime(b["timestamp"]).values
                for i in range(0, len(cl) - H, H):
                    if i < 30: continue
                    r14 = cl[i] / cl[i - 14] - 1
                    r30 = cl[i] / cl[i - 30] - 1
                    vs = v[i-13:i+1].mean() / v[i-29:i+1].mean() - 1
                    vs7 = v[i-6:i+1].mean() / v[i-29:i+1].mean() - 1
                    cases.append((c, w, pd.Timestamp(ts[i]).floor("D"), cl[i + H] / cl[i] - 1 - mu, r14, r30, vs, vs7))
        C = pd.DataFrame(cases, columns=["coin", "w", "day", "ex", "r14", "r30", "vs", "vs7"])
        C["year"] = C.day.dt.year
        allC[H] = C
    res = []
    for H, C in allC.items():
        up = C[C.r14 > 0]; dn = C[C.r14 <= 0]
        for name, sub in [("up", up), ("down", dn)]:
            sub = sub.copy()
            sub["q"] = pd.qcut(sub.vs, 3, labels=False)
            for q, s in sub.groupby("q"):
                t, G = ctt(s)
                res.append({"H": H, "set": f"{name} vs tercile {q}", "n": len(s), "days": G,
                            "mean_ex": s.ex.mean(), "t_cl": t, "vs_mean": s.vs.mean()})
        # signed product: vs * sign(r14)
        t, G = ctt(C[(C.vs > 0)])
        res.append({"H": H, "set": "vs>0 all", "n": int((C.vs > 0).sum()), "days": G,
                    "mean_ex": C[C.vs > 0].ex.mean(), "t_cl": t})
    out["vs terciles by trend side (clustered t)"] = pd.DataFrame(res)
    C = allC[14]
    up = C[C.r14 > 0].copy()
    up["hi"] = up.vs > 0
    yr = up.groupby(["year", "hi"])["ex"].agg(["mean", "size"]).unstack()
    out["H14 up: by year, swell vs no swell"] = yr
    cn = up.groupby(["coin", "hi"])["ex"].mean().unstack()
    cn["diff"] = cn[True] - cn[False]
    out["H14 up: by coin swell minus no-swell"] = cn.sort_values("diff")
    out["H14 up: share coins diff>0"] = float((cn["diff"] > 0).mean())
    # short-term 7-day swell instead of 14
    s = []
    for H in [7, 14]:
        u = allC[H][allC[H].r14 > 0]
        s.append({"H": H, "corr vs14": u[["vs", "ex"]].corr(method="spearman").iloc[0, 1],
                  "corr vs7": u[["vs7", "ex"]].corr(method="spearman").iloc[0, 1],
                  "corr vs14 down": allC[H][allC[H].r14 <= 0][["vs", "ex"]].corr(method="spearman").iloc[0, 1]})
    out["spearman"] = pd.DataFrame(s)
    return out

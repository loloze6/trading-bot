def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            if len(b) < 220: continue
            r1 = c.pct_change(); vol = r1.rolling(180).std()
            h12 = hi.shift(1).rolling(12).max(); l12 = lo.shift(1).rolling(12).min()
            dn = (c - l12).clip(upper=0) / c
            up = (c - h12).clip(lower=0) / c
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"dnz": dn / vol, "upz": up / vol, "r6z": (c / c.shift(6) - 1) / (vol * np.sqrt(6)),
                               "r180": c / c.shift(180) - 1, "year": ts.dt.year, "ts": ts, "win": w})
            for H in [6, 12, 18]:
                df["f%d" % H] = c.shift(-H) / c - 1
            df = df.iloc[::18]
            df = df[df["f18"].notna() & df["dnz"].notna()]
            recs.append(df)
        if not recs: continue
        d = pd.concat(recs)
        for H in [6, 12, 18]:
            d["u%d" % H] = d["f%d" % H] - d["f%d" % H].mean()
        d["z18"] = d["u18"] / d["f18"].std()
        d["coin"] = coin
        rows.append(d)
    D = pd.concat(rows)
    def summ(g):
        x = g["u18"]
        return pd.Series({"n": len(x), "mean_u%": x.mean() * 100, "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "u6%": g["u6"].mean() * 100, "u12%": g["u12"].mean() * 100, "share_pos": (x > 0).mean()})
    out = {}
    B = D[D["dnz"] < 0].copy()
    B["q"] = pd.qcut(B["dnz"].rank(method="first"), 4, labels=False)  # 0 = deepest break
    out["down-break by depth quartile (0 deepest)"] = B.groupby("q").apply(summ)
    out["down-break by year"] = B.groupby("year").apply(summ)
    pc = B.groupby("coin")["u18"].mean()
    out["down-break per coin"] = pd.Series({"coins": len(pc), "coins_pos": (pc > 0).sum(), "median_u%": pc.median() * 100})
    pw = B.groupby("win")["u18"].mean()
    out["down-break per window"] = pd.Series({"windows": len(pw), "windows_pos": (pw > 0).sum(), "median_u%": pw.median() * 100})
    # date clustering: average over coins on the same bar time
    bt = B.groupby("ts")["u18"].mean()
    out["down-break clustered by bar time"] = pd.Series({"n_times": len(bt), "mean_u%": bt.mean() * 100, "t": bt.mean() / (bt.std() / np.sqrt(len(bt)))})
    # graded r6 reversal: z of 1-day return
    D["q6"] = pd.qcut(D["r6z"].rank(method="first"), 10, labels=False)
    out["fwd by decile of 1-day return z"] = D.groupby("q6").apply(summ)
    out["down-break by trend (r180>0)"] = B.groupby(B["r180"] > 0).apply(summ)
    # weekday clustered by time
    D["wd"] = D["ts"].dt.weekday
    g = D.groupby(["wd", "ts"])["u18"].mean().reset_index()
    out["weekday clustered by bar time"] = g.groupby("wd")["u18"].agg(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    # up-break graded
    U = D[D["upz"] > 0].copy()
    U["q"] = pd.qcut(U["upz"].rank(method="first"), 4, labels=False)
    out["up-break by size quartile"] = U.groupby("q").apply(summ)
    return out

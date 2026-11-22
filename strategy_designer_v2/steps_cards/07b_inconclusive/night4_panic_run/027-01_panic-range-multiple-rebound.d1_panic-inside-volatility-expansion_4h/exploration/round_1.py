def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 84
    hs = {"1d": 6, "3d": 18, "7d": 42, "14d": 84}
    # drift per coin per horizon on non-overlapping grid
    drift, usual = {}, {}
    for c in bars:
        for k, h in hs.items():
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, k)] = np.mean(rs); usual[(c, k)] = np.std(rs)
    rows = []
    raw = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            # recomputed raw situation
            rh = pd.Series(hi).rolling(6).max(); rl = pd.Series(lo).rolling(6).min()
            rng = (rh - rl) / pd.Series(cl)
            mult = (rng / rng.rolling(180).mean()).values
            fall = (pd.Series(cl) / pd.Series(cl).shift(6) - 1).values
            lr = np.log(pd.Series(cl)).diff()
            v7 = lr.rolling(42).std(); vr = (v7 / v7.rolling(360).mean()).values
            ret30 = (pd.Series(cl) / pd.Series(cl).shift(180) - 1).values
            # cases
            lowest = 0.0
            for s in range(0, n, H):
                e = min(s + H, n)
                done = False
                for t in range(s, e):
                    if f[t] <= 0: lowest = 0.0
                    if not done and f[t] - lowest >= 2:
                        done = True
                        lowest = f[t]
                        rec = dict(coin=c, win=w, year=yr[t], fc=f[t], mult=mult[t], fall=fall[t], vr=vr[t], r30=ret30[t])
                        for k, h in hs.items():
                            rec[k] = (cl[t + h] / cl[t] - 1 - drift[(c, k)]) if t + h < n else np.nan
                        rows.append(rec)
                    lowest = min(lowest, f[t]) if f[t] > 0 else 0.0
            # raw panic grid: per 84 cell, bar with largest mult among falls
            for s in range(0, n - H, H):
                seg = np.arange(s, s + H)
                ok = seg[(fall[seg] < 0) & np.isfinite(mult[seg])]
                if len(ok) == 0: continue
                t = ok[np.argmax(mult[ok])]
                if t + H >= n: continue
                rec = dict(coin=c, year=yr[t], mult=mult[t], vr=vr[t], r30=ret30[t], fall=fall[t])
                for k, h in hs.items():
                    rec[k] = (cl[t + h] / cl[t] - 1 - drift[(c, k)]) if t + h < n else np.nan
                raw.append(rec)
    C = pd.DataFrame(rows); R = pd.DataFrame(raw)
    def summ(g):
        out = {}
        for k in hs:
            x = g[k].dropna()
            out[k + "_mean"] = x.mean(); out[k + "_t"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    res = {}
    res["cases_all"] = summ(C)
    res["cases_by_coin"] = C.groupby("coin").apply(summ)
    res["cases_by_year"] = C.groupby("year").apply(summ)
    C["fq"] = pd.qcut(C["fc"].rank(method="first"), 4, labels=False)
    res["cases_by_fc_quartile"] = C.groupby("fq").apply(summ)
    C["vq"] = pd.qcut(C["vr"].rank(method="first"), 4, labels=False)
    res["cases_by_volratio_q"] = C.groupby("vq").apply(summ)
    C["tq"] = pd.qcut(C["r30"].rank(method="first"), 4, labels=False)
    res["cases_by_prior30d_q"] = C.groupby("tq").apply(summ)
    C["mq"] = pd.qcut(C["mult"].rank(method="first"), 4, labels=False)
    res["cases_by_mult_q"] = C.groupby("mq").apply(summ)
    R = R.dropna(subset=["mult"])
    R["mq"] = pd.qcut(R["mult"].rank(method="first"), 5, labels=False)
    res["raw_bestfall_per_cell_by_mult_quint"] = R.groupby("mq").apply(summ)
    R["vq"] = pd.qcut(R["vr"].rank(method="first"), 4, labels=False)
    top = R[R["mq"] == 4]
    res["raw_top_mult_by_volratio_q"] = top.groupby("vq").apply(summ)
    res["raw_top_mult_by_prior30d_q"] = top.groupby(pd.qcut(top["r30"].rank(method="first"), 4, labels=False)).apply(summ)
    return res

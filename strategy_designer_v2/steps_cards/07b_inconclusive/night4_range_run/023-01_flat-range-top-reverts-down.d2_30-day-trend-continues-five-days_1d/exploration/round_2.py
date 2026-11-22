def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    hs = [1, 3, 5, 10, 20]
    drift = {}
    for coin, ws in bars.items():
        for h in hs:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rr), np.std(rr))
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            hi = df["high"].rolling(30).max().values
            lo = df["low"].rolling(30).min().values
            r30 = df["close"].pct_change(30).values
            nmr = np.abs(df["close"].diff(30).values) / (hi - lo)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            f = df["forecast"].values
            wn = int(str(w).lstrip("w"))
            for h in hs:
                for i in range(0, len(c) - h, h):
                    fr = c[i + h] / c[i] - 1 - drift[(coin, h)][0]
                    rows.append(dict(coin=coin, w=wn, year=yr[i], h=h, f=f[i], nmr=nmr[i], r30=r30[i],
                                     fr=fr, z=fr / drift[(coin, h)][1]))
    R = pd.DataFrame(rows)
    out = {}
    def corr(g, x="f"):
        g = g.dropna(subset=[x, "fr"])
        n = len(g)
        if n < 10:
            return pd.Series({"n": n, "r": np.nan, "t": np.nan})
        r = np.corrcoef(g[x], g["fr"])[0, 1]
        return pd.Series({"n": n, "r": r, "t": r * np.sqrt((n - 2) / (1 - r * r))})
    def dmv(g):
        s = g["sgn_move"].dropna(); n = len(s)
        return pd.Series({"n": n, "mean_dir_move": s.mean(), "mean_strength": g["sgn_z"].mean(),
                          "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    T = R[R.f != 0].copy()
    T["sgn_move"] = np.sign(T.f) * T.fr
    T["sgn_z"] = np.sign(T.f) * T.z
    out["corr_by_horizon"] = T.groupby("h").apply(corr)
    out["dirmove_by_horizon"] = T.groupby("h").apply(dmv)
    T5 = T[T.h == 5].copy()
    out["by_coin_h5"] = pd.concat([T5.groupby("coin").apply(corr), T5.groupby("coin").apply(dmv)[["mean_dir_move", "t"]].rename(columns={"t": "t_dir"})], axis=1)
    out["by_year_h5"] = pd.concat([T5.groupby("year").apply(corr), T5.groupby("year").apply(dmv)[["mean_dir_move"]]], axis=1)
    T5["wg"] = pd.cut(T5.w, [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["by_windowgroup_h5"] = T5.groupby("wg").apply(corr)
    out["by_side_h5"] = T5.groupby(np.sign(T5.f)).apply(dmv)
    T5["fq"] = pd.qcut(T5.f.abs().rank(method="first"), 4, labels=False)
    out["by_absf_quartile_h5"] = T5.groupby("fq").apply(lambda g: pd.concat([pd.Series({"absf": g.f.abs().mean()}), dmv(g)]))
    T5["nb"] = pd.cut(T5.nmr, [0, 0.5, 0.65, 0.8, 1.01])
    out["by_nmr_within_trending_h5"] = T5.groupby("nb").apply(dmv)
    A = R.dropna(subset=["nmr", "r30"]).copy()
    A["nb"] = pd.cut(A.nmr, [0, 0.25, 0.5, 0.75, 1.01])
    for h in [5, 10, 20]:
        out[f"r30_vs_fwd_by_nmr_bucket_h{h}"] = A[A.h == h].groupby("nb").apply(lambda g: corr(g, "r30"))
    return out

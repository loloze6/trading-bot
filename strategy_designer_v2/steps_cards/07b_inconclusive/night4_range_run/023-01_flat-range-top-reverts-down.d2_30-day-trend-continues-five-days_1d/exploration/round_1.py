def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    hs = [1, 3, 5, 10, 20]
    # drift per coin per horizon
    for coin, ws in bars.items():
        for h in hs:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rr), np.std(rr))
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
            for h in hs:
                for i in range(0, len(c) - h, h):
                    fr = c[i + h] / c[i] - 1 - drift[(coin, h)][0]
                    rows.append(dict(coin=coin, w=w, year=yr[i], h=h, f=f[i], reg=df["regime"].iloc[i],
                                     nmr=nmr[i], r30=r30[i], fr=fr, z=fr / drift[(coin, h)][1]))
    R = pd.DataFrame(rows)
    out = {}
    def corr(g, x="f"):
        g = g.dropna(subset=[x, "fr"])
        if len(g) < 10: return pd.Series({"n": len(g), "r": np.nan, "t": np.nan})
        r = np.corrcoef(g[x], g["fr"])[0, 1]
        n = len(g); t = r * np.sqrt((n - 2) / (1 - r * r))
        return pd.Series({"n": n, "r": r, "t": t})
    T = R[(R.f != 0)]
    out["by_horizon_trending"] = T.groupby("h").apply(corr)
    T5 = T[T.h == 5].copy()
    T5["sgn_move"] = np.sign(T5.f) * T5.fr
    out["by_coin_h5"] = T5.groupby("coin").apply(corr)
    out["by_year_h5"] = T5.groupby("year").apply(corr)
    out["by_side_h5"] = T5.groupby(np.sign(T5.f)).apply(lambda g: pd.Series({"n": len(g), "mean_dir_move": g.sgn_move.mean(), "t": g.sgn_move.mean() / (g.sgn_move.std() / np.sqrt(len(g)))}))
    T5["fq"] = pd.qcut(T5.f.abs(), 4, labels=False)
    out["by_absf_quartile_h5"] = T5.groupby("fq").apply(lambda g: pd.Series({"n": len(g), "absf": g.f.abs().mean(), "mean_dir_move": g.sgn_move.mean(), "t": g.sgn_move.mean() / (g.sgn_move.std() / np.sqrt(len(g)))}))
    # all bars: r30 vs forward, by nmr bucket (brief's flat regime too)
    A = R.dropna(subset=["nmr", "r30"]).copy()
    A["nb"] = pd.cut(A.nmr, [0, 0.25, 0.5, 0.75, 1.01])
    out["r30_vs_fwd_by_nmr_bucket_h5"] = A[A.h == 5].groupby("nb").apply(lambda g: corr(g, "r30"))
    out["r30_vs_fwd_by_nmr_bucket_h10"] = A[A.h == 10].groupby("nb").apply(lambda g: corr(g, "r30"))
    out["r30_vs_fwd_by_nmr_bucket_h20"] = A[A.h == 20].groupby("nb").apply(lambda g: corr(g, "r30"))
    return out

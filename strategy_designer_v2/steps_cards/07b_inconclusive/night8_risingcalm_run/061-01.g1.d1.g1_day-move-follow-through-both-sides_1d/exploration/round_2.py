def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            f = b["forecast"].astype(float)
            for h in (2, 3, 4, 5, 7, 10):
                fwd = c.shift(-h) / c - 1
                for off in range(h):
                    idx = np.arange(off, len(b) - h, h)
                    for i in idx:
                        recs.append((coin, w, h, off, f.iloc[i], sd30.iloc[i], fwd.iloc[i], abs(r.iloc[i]) / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan))
    df = pd.DataFrame(recs, columns=["coin", "w", "h", "off", "f", "sd30", "fwd", "absz"])
    df["ex"] = df["fwd"] - df.groupby(["coin", "h", "off"])["fwd"].transform("mean")
    med = df[(df.h == 2) & (df.off == 0)].groupby("coin")["sd30"].median()
    df = df.dropna(subset=["sd30", "f", "ex"])
    df["agit"] = np.where(df["sd30"] > df["coin"].map(med), "agitated", "calm")

    def sl(g):
        if len(g) < 30 or g.f.std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        res = stats.linregress(g.f, g.ex)
        return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope / res.stderr))
    per = df.groupby(["h", "agit", "off"]).apply(sl).reset_index()
    out = {}
    out["t_over_offsets"] = per.groupby(["h", "agit"]).agg(n=("n", "mean"), mean_slope=("slope", "mean"),
                                                         mean_t=("t", "mean"), min_t=("t", "min"), max_t=("t", "max"),
                                                         share_pos=("slope", lambda s: (s > 0).mean()))
    # graded check in calm, h5, all offsets pooled: quintiles of |forecast|, signed excess
    d = df[(df.h == 5)].copy()
    d["sx"] = np.sign(d.f) * d.ex
    d["q"] = d.groupby("agit")["f"].transform(lambda s: pd.qcut(s.abs(), 5, labels=False, duplicates="drop"))
    out["h5_quintiles_signed_ex"] = d.groupby(["agit", "q"])["sx"].agg(["count", "mean"])
    # calm, by window, offset-averaged slope t at h5
    pw = d[d.agit == "calm"].groupby(["w", "off"]).apply(sl).reset_index()
    out["h5_calm_by_window"] = pw.groupby("w").agg(mean_slope=("slope", "mean"), mean_t=("t", "mean"))
    return out

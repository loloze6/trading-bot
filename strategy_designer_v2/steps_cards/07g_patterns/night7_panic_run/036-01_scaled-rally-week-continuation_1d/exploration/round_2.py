def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame(dict(coin=coin, win=w, pos=np.arange(len(b)),
                                   s1=r1 / sd, s3=(c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                                   s7=(c / c.shift(7) - 1) / (sd * np.sqrt(7)),
                                   s14=(c / c.shift(14) - 1) / (sd * np.sqrt(14)),
                                   r60=c / c.shift(60) - 1,
                                   fwd7=c.shift(-7) / c - 1, fwd1=c.shift(-1) / c - 1, r1=r1,
                                   wd=ts.dt.weekday, yr=ts.dt.year, day=ts.dt.normalize(),
                                   bk=b["postRebalance_total_value"].astype(float).pct_change().shift(-1),
                                   alloc=b["postRebalance_current_allocation"].astype(float)))
            recs.append(df)
    A = pd.concat(recs, ignore_index=True)
    # drift per coin from offset-0 grid
    g0 = A[A["pos"] % 7 == 0].dropna(subset=["fwd7"])
    drift = g0.groupby("coin")["fwd7"].mean()
    A["u7"] = A["fwd7"] - A["coin"].map(drift)
    out = {}
    def cl_t(df, col):
        s = df.groupby("day")[col].apply(lambda v: (v - df[col].mean()).sum())
        G = len(s); m = df[col].mean()
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / len(df)
        return m, m / se, G
    # slopes per offset grid
    rows = []
    for off in range(7):
        G = A[A["pos"] % 7 == off].dropna(subset=["u7", "s1", "s3", "s7", "s14"])
        for f in ["s1", "s3", "s7", "s14"]:
            s = stats.linregress(G[f], G["u7"])
            rows.append(dict(off=off, f=f, slope=s.slope, t=s.slope / s.stderr, n=len(G)))
    R = pd.DataFrame(rows)
    out["slope u7 on feature, by grid offset (mean over offsets)"] = R.groupby("f")[["slope", "t", "n"]].mean()
    out["t of slope per offset"] = R.pivot(index="off", columns="f", values="t")
    # top-quintile s7 vs rest, all offsets pooled per offset 0
    rows = []
    for off in range(7):
        G = A[A["pos"] % 7 == off].dropna(subset=["u7", "s7"]).copy()
        G["q"] = pd.qcut(G["s7"], 5, labels=False)
        for q, gg in G.groupby("q"):
            rows.append(dict(off=off, q=q, mean=gg["u7"].mean()))
    out["u7 by s7 quintile, mean over offsets"] = pd.DataFrame(rows).groupby("q")["mean"].agg(["mean", "std"])
    # s7 slope by trend
    rows = []
    for off in range(7):
        G = A[A["pos"] % 7 == off].dropna(subset=["u7", "s7", "r60"]).copy()
        G["tr"] = np.where(G["r60"] > 0.1, "rising", np.where(G["r60"] < -0.1, "falling", "choppy"))
        for tr, gg in G.groupby("tr"):
            s = stats.linregress(gg["s7"], gg["u7"]); rows.append(dict(off=off, tr=tr, slope=s.slope, t=s.slope / s.stderr, n=len(gg)))
    out["s7 slope by trend (mean over offsets)"] = pd.DataFrame(rows).groupby("tr")[["slope", "t", "n"]].mean()
    # s7 slope by year (offset 0..6 mean)
    rows = []
    for off in range(7):
        G = A[A["pos"] % 7 == off].dropna(subset=["u7", "s7"])
        for y, gg in G.groupby("yr"):
            if len(gg) > 20:
                s = stats.linregress(gg["s7"], gg["u7"]); rows.append(dict(off=off, yr=y, slope=s.slope, t=s.slope / s.stderr, n=len(gg)))
    out["s7 slope by year"] = pd.DataFrame(rows).groupby("yr")[["slope", "t", "n"]].mean()
    # weekday of next-day return (all days), clustered by day
    B = A.dropna(subset=["fwd1"])
    rows = []
    for wd, gg in B.groupby("wd"):
        m, t, G = cl_t(gg, "fwd1"); rows.append(dict(wd=wd, mean=m, t=t, days=G))
    out["next-day coin return by weekday of signal bar"] = pd.DataFrame(rows)
    # weekday by year for the friday-ish effect
    rows = []
    for (y, wd), gg in B.groupby(["yr", "wd"]):
        rows.append(dict(yr=y, wd=wd, mean=gg["fwd1"].mean()))
    out["next-day return by year x weekday"] = pd.DataFrame(rows).pivot(index="yr", columns="wd", values="mean")
    # next-day after scaled 1d move deciles (all bars, clustered)
    C = A.dropna(subset=["fwd1", "s1"]).copy()
    C["q"] = pd.qcut(C["s1"], 10, labels=False)
    rows = []
    for q, gg in C.groupby("q"):
        m, t, G = cl_t(gg, "fwd1"); rows.append(dict(q=q, mid=gg["s1"].median(), mean=m, t=t, days=G))
    out["next-day return by s1 decile"] = pd.DataFrame(rows)
    # book: gain on in-position bars by s7 tercile
    D = A.dropna(subset=["bk", "s7"]).copy()
    D["q"] = pd.qcut(D["s7"], 3, labels=["low", "mid", "high"])
    out["book bar return by s7 tercile"] = D.groupby("q")[["bk", "alloc"]].mean()
    return out

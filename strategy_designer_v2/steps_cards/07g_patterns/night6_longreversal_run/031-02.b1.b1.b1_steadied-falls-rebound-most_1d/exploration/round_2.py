def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}

    def cstats(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for p in range(0, len(c) - h, h):
                rs.append(c[p + h] / c[p] - 1)
        rs = np.array(rs); return rs.mean(), rs.std(ddof=1)

    def build(h, L):
        rows = []
        for coin in bars:
            dh, sh = cstats(coin, h); dL, sL = cstats(coin, L)
            for w, df in bars[coin].items():
                c = df["close"].values; ts = pd.to_datetime(df["timestamp"]).values
                for p in range(0, len(c) - h, h):
                    if p - L < 0: continue
                    past = c[p] / c[p - L] - 1; fwd = c[p + h] / c[p] - 1
                    rows.append(dict(coin=coin, w=w, day=ts[p], year=pd.Timestamp(ts[p]).year,
                                     z=(past - dL) / sL, ex=(fwd - dh) / sh))
        return pd.DataFrame(rows)

    def day_t(d):
        # per-case contribution z*ex demeaned; sign-strength = sign(z)*ex summed per day
        d = d.copy(); d["s"] = np.sign(d.z) * d.ex
        g = d.groupby("day").s.sum()
        return g.mean() / (g.std(ddof=1) / np.sqrt(len(g))), len(g), d.s.mean()

    summ = []
    for h, L in [(1, 1), (1, 3), (3, 7), (7, 30), (14, 30), (30, 30)]:
        d = build(h, L)
        t, nd, m = day_t(d)
        # graded: within sign, slope of ex on |z|*sign
        r = stats.linregress(d.z, d.ex)
        summ.append(dict(h=h, L=L, n=len(d), days=nd, mean_signed_strength=m, day_t=t, slope=r.slope))
        if (h, L) in [(1, 1), (7, 30), (30, 30)]:
            d["s"] = np.sign(d.z) * d.ex
            yy = d.groupby("year").s.agg(["size", "mean"])
            out[f"by year h{h} L{L} signed strength"] = yy.round(4)
            cc = d.groupby("coin").s.mean()
            out[f"coins positive h{h} L{L}"] = f"{(cc>0).sum()} of {len(cc)}"
        if (h, L) == (1, 1):
            d["aq"] = pd.qcut(d.z.abs(), 5, labels=False)
            out["h1 L1 by size of |move| quintile"] = d.groupby("aq").agg(n=("s", "size"), absz=("z", lambda x: x.abs().mean()), signed=("s", "mean")).round(4)
            out["h1 L1 up vs down move"] = d.groupby(np.sign(d.z)).s.agg(["size", "mean"]).round(4)
    out["signed strength, day-clustered t (sign(past)*fwd excess)"] = pd.DataFrame(summ).round(4)

    # weekday: day-level mean across coins, t over days, by year sign
    wd = []
    for coin in bars:
        for w, df in bars[coin].items():
            ts = pd.to_datetime(df["timestamp"]); c = df["close"].values
            wd.append(pd.DataFrame(dict(day=ts.values[1:], wd=ts.dt.dayofweek.values[1:], year=ts.dt.year.values[1:], r=c[1:] / c[:-1] - 1)))
    wd = pd.concat(wd)
    dm = wd.groupby(["day", "wd", "year"]).r.mean().reset_index()
    allm = dm.r.mean()
    g = dm.groupby("wd").r.agg(["size", "mean", "std"]); g["t_vs_all"] = (g["mean"] - allm) / (g["std"] / np.sqrt(g["size"]))
    out["weekday, day-level mean over coins"] = g.round(5)
    out["weekday by year (day-level mean, %)"] = (dm.pivot_table(index="year", columns="wd", values="r", aggfunc="mean") * 100).round(3)
    return out

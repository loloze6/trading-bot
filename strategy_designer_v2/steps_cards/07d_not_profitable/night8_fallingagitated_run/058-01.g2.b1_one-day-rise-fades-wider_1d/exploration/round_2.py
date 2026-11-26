def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        for h in [3, 5]:
            g = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    g.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(g); drift[(coin, h, "sd")] = np.std(g, ddof=1)
    rows = []; tr = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std(); z = r1 / sd
            r60 = c.pct_change(60)
            prev_up = (r1.shift(1) > 0)
            r3p = c.pct_change(3).shift(1)  # 3-day return before today
            prof = (df["regime"] == "unknown").values
            alloc = df["postRebalance_current_allocation"].fillna(0).values
            n = len(df)
            for h in [3, 5]:
                for i in range(0, n - h, h):
                    fr = c.iloc[i + h] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, z=z.iloc[i], prof=prof[i], fc=df["forecast"].iloc[i],
                                     ex=fr - drift[(coin, h)], usual=drift[(coin, h, "sd")],
                                     prev_up=prev_up.iloc[i], r60=r60.iloc[i], r3p=r3p.iloc[i],
                                     zprev=z.iloc[i-1] if i > 0 else np.nan,
                                     day=str(pd.Timestamp(df["timestamp"].iloc[i]).date())))
            # book's gain per bar by position state
            g = alloc[:-1] * (c.values[1:] / c.values[:-1] - 1)
            for i in range(n - 1):
                if alloc[i] != 0:
                    tr.append(dict(coin=coin, w=w, gain=g[i], z_today=z.iloc[i], fc=df["forecast"].iloc[i], alloc=alloc[i]))
    R = pd.DataFrame(rows).dropna(subset=["z"])
    out = {}
    def summ(g):
        n = len(g)
        if n < 3: return pd.Series(dict(n=n, mean_ex=g.ex.mean(), t=np.nan, strength=np.nan))
        d = g.groupby("day").ex.sum()
        return pd.Series(dict(n=n, days=len(d), mean_ex=g.ex.mean(),
                              t_day=d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) * 1.0,
                              strength=(g.ex / g.usual).mean()))
    P = R[R.prof & (R.h == 3)]
    out["h3 prof: forecast<0 cases by z"] = P[P.fc < 0].groupby(pd.cut(P[P.fc < 0].z, [0, 0.5, 1, 99])).apply(summ)
    out["h3 prof: share of fc<0 by z"] = P.groupby(pd.cut(P.z, [-99, 0, 0.5, 1, 99]), observed=True).fc.apply(lambda s: (s < 0).mean())
    U = P[P.z > 0.5]
    out["h3 prof z>0.5 by prev day up"] = U.groupby("prev_up").apply(summ)
    out["h3 prof z>0.5 by prior 3d ret>0"] = U.groupby(U.r3p > 0).apply(summ)
    out["h3 prof z>0.5 by r60 depth"] = U.groupby(pd.cut(U.r60, [-1, -0.3, -0.1])).apply(summ)
    D0 = P[(P.z <= 0.5)]
    out["h3 prof z<=0.5 by r60 depth (condition alone)"] = D0.groupby(pd.cut(D0.r60, [-1, -0.3, -0.1])).apply(summ)
    P5 = R[R.prof & (R.h == 5)]; U5 = P5[P5.z > 0.5]
    out["h5 prof z>0.5"] = summ(U5)
    out["h3 prof z>0.5 all"] = summ(U)
    T = pd.DataFrame(tr)
    T["state"] = np.where(T.fc < 0, "signal bar", "held after")
    out["bar gains by state"] = T.groupby("state").agg(n=("gain", "size"), mean=("gain", "mean"), sum=("gain", "sum"))
    T2 = T[T.fc < 0]
    out["signal-bar gains by z"] = T2.groupby(pd.cut(T2.z_today, [-99, 0, 0.5, 1, 99]), observed=True).agg(n=("gain", "size"), mean=("gain", "mean"), sum=("gain", "sum"))
    out["mean |alloc| by state"] = T.groupby("state").alloc.apply(lambda s: s.abs().mean())
    return out

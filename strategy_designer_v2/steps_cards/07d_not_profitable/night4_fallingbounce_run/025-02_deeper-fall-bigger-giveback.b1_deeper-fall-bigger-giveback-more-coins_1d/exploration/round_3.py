def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift1 = {}; drift5 = {}; usual1 = {}
    for coin, ws in bars.items():
        a1 = []; a5 = []
        for w, df in ws.items():
            c = df["close"].values
            a1 += list(c[1:] / c[:-1] - 1)
            a5 += [c[i + 5] / c[i] - 1 for i in range(0, len(c) - 5, 5)]
        drift1[coin] = np.mean(a1); usual1[coin] = np.std(a1); drift5[coin] = np.mean(a5)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            z = r1 / r1.rolling(20).std().shift(1)
            n = len(df)
            mr = (df.regime == "mean_reversion").values
            fd = df.get("debug_info.components.fall_depth.last_history_value")
            for i in range(n - 5):
                if not mr[i]:
                    continue
                f1 = c.iat[i + 1] / c.iat[i] - 1
                f2 = c.iat[i + 2] / c.iat[i] - 1
                f25 = c.iat[i + 5] / c.iat[i + 1] - 1
                rows.append(dict(coin=coin, w=w, z=z.iat[i], r90=fd.iat[i] if fd is not None else np.nan,
                                 ex1=f1 - drift1[coin], s1=(f1 - drift1[coin]) / usual1[coin],
                                 ex2=f2 - 2 * drift1[coin], ex25=f25 - 4 * drift1[coin],
                                 r1=r1.iat[i], year=pd.Timestamp(df.timestamp.iat[i]).year))
    d = pd.DataFrame(rows)
    def summ(g):
        def t(x):
            x = x.dropna(); return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(dict(n=len(g), ex1=g.ex1.mean(), t1=t(g.ex1), ex2=g.ex2.mean(), t2=t(g.ex2),
                              ex25=g.ex25.mean(), t25=t(g.ex25), s1=g.s1.mean()))
    out = {}
    out["mr bars: day1 vs days2-5"] = summ(d).to_frame().T
    dz = d.dropna(subset=["z"])
    out["by bounce size z"] = dz.groupby(pd.cut(dz.z, [-10, 2, 2.5, 3, 4, 100])).apply(summ)
    lr = stats.linregress(dz.z.clip(upper=8), dz.s1)
    out["s1 on z"] = pd.Series(dict(slope=lr.slope, t=lr.slope / lr.stderr, n=len(dz)))
    dr = d.dropna(subset=["r1"])
    lr2 = stats.linregress(dr.r1.clip(upper=0.5), dr.ex1)
    out["ex1 on bounce return r1"] = pd.Series(dict(slope=lr2.slope, t=lr2.slope / lr2.stderr, n=len(dr)))
    dd = d.dropna(subset=["r90"])
    out["day1 by r90 tercile"] = dd.groupby(pd.qcut(dd.r90, 3)).apply(summ)
    out["day1 by year"] = d.groupby("year").apply(summ)
    # book: gain by bars since entry
    rr = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df.close; a = df.postRebalance_current_allocation.fillna(0)
            g = a * (c.shift(-1) / c - 1)
            k = 0; ks = []
            for i in range(len(df)):
                k = k + 1 if a.iat[i] != 0 else 0
                ks.append(k)
            rr.append(pd.DataFrame(dict(k=ks, g=g, a=a)))
    R = pd.concat(rr); R = R[R.a != 0]
    out["position gain by bar since entry"] = R.groupby(pd.cut(R.k, [0, 1, 2, 5, 10, 30, 10000])).agg(
        n=("g", "size"), mean_g=("g", "mean"), sum_g=("g", "sum"))
    return out

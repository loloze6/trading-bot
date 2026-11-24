def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]

    def tclust(d, col="ex"):
        g = d.groupby("day")[col].sum()
        G = len(g)
        if G < 3: return np.nan
        m = d[col].sum() / len(d)
        cnt = d.groupby("day").size()
        se = np.sqrt((g - m * cnt).pow(2).sum() * G / (G - 1)) / len(d)
        return m / se if se > 0 else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for p in range(0, n, 30):
                if p + 30 >= n: continue
                rows.append(dict(coin=coin, win=w, pos=p, ret=c[p+30]/c[p]-1, fc=f[p],
                                 day=ts.iloc[p].normalize(), year=ts.iloc[p].year,
                                 p30=(c[p]/c[p-30]-1) if p >= 30 else np.nan,
                                 p10=(c[p]/c[p-10]-1) if p >= 10 else np.nan,
                                 dd=c[p]/c[:p+1].max()-1))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby("coin")["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    S = R[R.fc > 0].copy()
    out = {}
    out["share_fc_at_cap"] = float((S.fc >= 19.999).mean())
    res = []
    for name, m in [("p30_down", S.p30 < 0), ("p30_up", S.p30 > 0), ("p10_down", S.p10 < 0), ("p10_up", S.p10 > 0)]:
        d = S[m]
        res.append(dict(group=name, n=len(d), days=d.day.nunique(), mean=d.ex.mean(), t=tclust(d)))
    out["grid_inreg_splits"] = pd.DataFrame(res)
    # all grid cells (in or out of regime) split by past 30-day return, as a graded check
    Rk = R.dropna(subset=["p30"]).copy()
    Rk["q"] = Rk.groupby("coin")["p30"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["allgrid_by_p30_quintile"] = Rk.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), p30=("p30", "mean"))
    out["allgrid_q0_t"] = tclust(Rk[Rk.q == 0])
    out["allgrid_q4_t"] = tclust(Rk[Rk.q == 4])

    # every in-regime bar, overlapping, descriptive
    allr = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            for p in range(30, len(df) - 30):
                if f[p] > 0:
                    allr.append(dict(coin=coin, win=w, r=c[p+30]/c[p]-1, p30=c[p]/c[p-30]-1, p10=c[p]/c[p-10]-1))
    A = pd.DataFrame(allr)
    A["ex"] = A["r"] - A["coin"].map(R.groupby("coin")["ret"].mean())
    A["p30q"] = pd.qcut(A["p30"], 4, labels=False)
    out["allbars_inreg_by_p30_quartile"] = A.groupby("p30q").agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                             p30=("p30", "mean"), wins=("win", "nunique"))
    A["p10q"] = pd.qcut(A["p10"], 4, labels=False)
    out["allbars_inreg_by_p10_quartile"] = A.groupby("p10q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), p10=("p10", "mean"))
    out["allbars_inreg_p30down_by_coin"] = A[A.p30 < 0].groupby("coin")["ex"].agg(["count", "mean"])
    out["allbars_inreg_p30up_by_coin"] = A[A.p30 > 0].groupby("coin")["ex"].agg(["count", "mean"])
    return out

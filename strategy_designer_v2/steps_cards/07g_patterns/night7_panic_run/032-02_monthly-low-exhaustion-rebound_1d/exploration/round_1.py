def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            n = len(df)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            prevlow = c.shift(1).rolling(30, min_periods=30).min()
            prevhigh = c.shift(1).rolling(30, min_periods=30).max()
            dlow = c / prevlow - 1
            dhigh = c / prevhigh - 1
            ret5 = c / c.shift(5) - 1
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for h in (1, 3):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, fwd=fwd[i], r1z=(r1[i] / vol30[i]) if vol30[i] > 0 else np.nan,
                                     dlow=dlow[i], dhigh=dhigh[i], ret5z=ret5[i] / (vol30[i] * np.sqrt(5)) if vol30[i] > 0 else np.nan,
                                     regime=df["regime"].iloc[i], wd=ts[i].dayofweek, yr=ts[i].year, vol=vol30[i],
                                     usual=np.nan))
    S = pd.DataFrame(rows).dropna(subset=["fwd"])
    def summ(g):
        return pd.Series({"n": len(g), "mean%": 100 * g.fwd.mean(), "t": g.fwd.mean() / (g.fwd.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    S3 = S[S.h == 3].copy(); S1 = S[S.h == 1].copy()
    S3["prof"] = np.where(S3.regime == "chop", "outside", "fallagit")
    S3["brk"] = np.where(S3.dlow < 0, "newlow", np.where(S3.dhigh > 0, "newhigh", "inside"))
    out["3d by profile x break"] = S3.groupby(["prof", "brk"]).apply(summ)
    S3["r1zq"] = pd.qcut(S3.r1z, 5, labels=False)
    out["3d by 1d-move z quintile"] = S3.groupby("r1zq").apply(summ)
    out["3d by 1d-move z quintile x prof"] = S3.groupby(["prof", "r1zq"]).apply(summ)
    S3["r5q"] = pd.qcut(S3.ret5z, 5, labels=False)
    out["3d by 5d-ret z quintile"] = S3.groupby("r5q").apply(summ)
    S3["volq"] = S3.groupby("coin").vol.transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["3d by vol tercile x brk"] = S3.groupby(["volq", "brk"]).apply(summ)
    nl = S3[S3.dlow < 0].copy()
    nl["dq"] = pd.qcut(nl.dlow, 3, labels=False)
    out["3d newlow depth tercile x prof"] = nl.groupby(["prof", "dq"]).apply(summ)
    out["1d by weekday"] = S1.groupby("wd").apply(summ)
    out["3d by year x brk"] = S3[S3.brk != "inside"].groupby(["yr", "brk"]).apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    if len(T):
        T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 3, labels=False)
        out["trades by entry forecast tercile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), f=("entry_forecast", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
        out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"))
    return out

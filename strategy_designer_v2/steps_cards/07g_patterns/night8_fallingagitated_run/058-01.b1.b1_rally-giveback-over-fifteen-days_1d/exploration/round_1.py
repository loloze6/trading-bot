def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = pd.Series(c) / pd.Series(c).shift(3) - 1
            s3 = r3 / (sd30 * np.sqrt(3))
            inprof = (df["regime"] == "unknown").values
            alloc = df["postRebalance_current_allocation"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            for h in (3, 15):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, s3=s3.iloc[i], r3=r3.iloc[i],
                                     prof=inprof[i], fwd=c[i+h]/c[i]-1, alloc=alloc[i],
                                     wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year,
                                     sd=sd30.iloc[i]))
    R = pd.DataFrame(rows).dropna(subset=["s3"])
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.fwd.mean(), t=g.fwd.mean()/(g.fwd.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    for h in (3, 15):
        Rh = R[R.h == h].copy()
        drift = Rh.groupby("coin").fwd.transform("mean")
        Rh["ex"] = Rh.fwd - drift
        Rh["q"] = pd.qcut(Rh.s3, 5, labels=False)
        g = Rh.groupby(["prof", "q"]).apply(lambda g: pd.Series(dict(n=len(g), s3=g.s3.mean(), ex=g.ex.mean(),
              t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))))))
        out[f"h{h} excess by profile x s3 quintile"] = g.round(4)
        for p in (True, False):
            sub = Rh[Rh.prof == p]
            sl = stats.linregress(sub.s3, sub.ex)
            out[f"h{h} prof={p} slope ex~s3"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(sub)}"
        out[f"h{h} excess by year (in profile)"] = Rh[Rh.prof].groupby("year").apply(lambda g: pd.Series(dict(n=len(g), ex=g.ex.mean(), corr=g.s3.corr(g.ex)))).round(3)
    # book daily
    D = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["coin return by weekday"] = D.groupby("wd").coin_return.agg(["count", "mean", "std"]).round(4)
    T = []
    for coin, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): d = df.copy(); d["coin"] = coin; T.append(d)
    T = pd.concat(T)
    out["trades by side"] = T.groupby("side").net_profit_loss_percent.agg(["count", "mean", "median", "std"]).round(3)
    out["trades by coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count", "mean"]).round(3)
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            g = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    g.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(g) if g else np.nan
            drift[(coin, h, "sd")] = np.std(g, ddof=1) if len(g) > 2 else np.nan
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = r1 / sd
            r3 = c.pct_change(3)
            sd3 = sd * np.sqrt(3)
            z3 = r3 / sd3
            inprof = (df["regime"] == "unknown").values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    fr = c.iloc[i + h] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, i=i, z=z.iloc[i], z3=z3.iloc[i],
                                     prof=inprof[i], fc=df["forecast"].iloc[i],
                                     ex=(fr - drift[(coin, h)]), fr=fr,
                                     usual=drift[(coin, h, "sd")], year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows).dropna(subset=["z"])
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g.ex.mean(), t_ex=g.ex.mean() / (g.ex.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_total=g.fr.mean(), strength=(g.ex / g.usual).mean()))
    R["zb"] = pd.cut(R.z, [-99, 0, 0.5, 1, 1.5, 2, 99])
    R["z3b"] = pd.cut(R.z3, [-99, 0, 0.5, 1, 1.5, 2, 99])
    for h in H:
        sub = R[R.h == h]
        out[f"h{h} in profile by 1d z"] = sub[sub.prof].groupby("zb", observed=True).apply(summ)
        out[f"h{h} out of profile by 1d z"] = sub[~sub.prof].groupby("zb", observed=True).apply(summ)
    sub = R[(R.h == 3) & R.prof]
    out["h3 in profile by 3d z"] = sub.groupby("z3b", observed=True).apply(summ)
    sub = R[(R.h == 5) & R.prof]
    out["h5 in profile by 3d z"] = sub.groupby("z3b", observed=True).apply(summ)
    sub = R[(R.h == 3) & R.prof & (R.z > 0)]
    out["h3 prof up by year"] = sub.groupby("year").apply(summ)
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): T.append(t.assign(coin=coin, w=w))
    T = pd.concat(T)
    out["trades"] = pd.Series(dict(n=len(T), gross=T.profit_loss_percent.mean(), net=T.net_profit_loss_percent.mean(),
                                   days=T.duration_minutes.mean() / 1440, short_share=(T.side == "SHORT").mean()))
    T["dur"] = (T.duration_minutes / 1440).round()
    out["trades by duration"] = T.groupby(pd.cut(T.dur, [0, 3, 5, 10, 30, 999])).agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    T["fq"] = pd.qcut(T.entry_forecast.abs(), 4, duplicates="drop")
    out["trades by entry forecast"] = T.groupby("fq", observed=True).agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # book by window
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    out["book by window"] = D.groupby("w").agg(mean_book=("book_return", "mean"), mean_coin=("coin_return", "mean"), n=("book_return", "size"))
    return out

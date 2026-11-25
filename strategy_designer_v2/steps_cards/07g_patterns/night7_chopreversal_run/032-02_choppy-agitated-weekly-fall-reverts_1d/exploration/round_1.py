def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 30: continue
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            for i in range(0, n - 7, 7):
                if i < 7: continue
                past = c[i] / c[i - 7] - 1
                fwd = c[i + 7] / c[i] - 1
                tr60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                rows.append(dict(coin=coin, win=w, i=i, past=past, fwd=fwd, tr60=tr60,
                                 vol30=vol30.iloc[i], inprof=(b["regime"].iloc[i] == "unknown"),
                                 fc=float(b["forecast"].iloc[i]) if pd.notna(b["forecast"].iloc[i]) else 0.0,
                                 ts=pd.Timestamp(b["timestamp"].iloc[i])))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    df["usual"] = df.groupby("coin")["fwd"].transform("std")
    df["pz"] = df["past"] / df["usual"]
    df["ez"] = df["ex"] / df["usual"]
    df["vrank"] = df.groupby("coin")["vol30"].rank(pct=True)

    def reg(g):
        g = g.dropna(subset=["pz", "ez"])
        if len(g) < 10: return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["pz"], g["ez"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr, mean_ex=g["ex"].mean()))

    out = {}
    out["all_slope"] = reg(df)
    out["by_inprof"] = df.groupby("inprof").apply(reg)
    df["tb"] = pd.cut(df["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["by_trend"] = df.groupby("tb").apply(reg)
    df["vb"] = pd.cut(df["vrank"], [0, 0.33, 0.66, 1], labels=["lowvol", "mid", "highvol"])
    out["by_vol"] = df.groupby("vb").apply(reg)
    out["by_trend_vol"] = df.groupby(["tb", "vb"]).apply(reg)
    df["side"] = np.where(df["past"] < 0, "fell", "rose")
    out["by_side"] = df.groupby("side").apply(reg)
    df["pq"] = df.groupby("coin")["pz"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd_by_past_quintile"] = df.groupby("pq").agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                       mean_ez=("ez", "mean"),
                                                       t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["by_coin"] = df.groupby("coin").apply(reg)
    out["by_year"] = df.groupby(df["ts"].dt.year).apply(reg)
    out["by_window"] = df.groupby("win").apply(reg)
    # weekday of daily returns, all bars
    dr = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; dr.append(d)
    D = pd.concat(dr)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin_ret_by_weekday"] = D.groupby("wd")["coin_return"].agg(["size", "mean",
                        lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    # 1-day return after large 1-day moves
    D["prev"] = D.groupby(["coin"])["coin_return"].shift(1)
    D["pz"] = D.groupby("coin")["prev"].transform(lambda x: (x - x.mean()) / x.std())
    D["pb"] = pd.cut(D["pz"], [-99, -2, -1, 1, 2, 99])
    out["next_day_by_prev_day_z"] = D.groupby("pb")["coin_return"].agg(["size", "mean",
                        lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    return out

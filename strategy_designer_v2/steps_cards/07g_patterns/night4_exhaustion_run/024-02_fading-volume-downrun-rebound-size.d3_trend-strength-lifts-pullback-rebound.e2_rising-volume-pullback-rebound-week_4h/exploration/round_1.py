def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    H = 42
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(c)
            if n < 200: continue
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            ret180 = pd.Series(c).pct_change(180).values
            ret6 = pd.Series(c).pct_change(6).values
            ret18 = pd.Series(c).pct_change(18).values
            vol = pd.Series(r1).rolling(180, min_periods=60).std().values
            # streaks
            sgn = np.sign(np.r_[0, np.diff(c)])
            streak = np.zeros(n)
            for i in range(1, n):
                streak[i] = streak[i-1]+sgn[i] if (sgn[i] == np.sign(streak[i-1]) and sgn[i] != 0) else sgn[i]
            vratio = pd.Series(v).rolling(6).mean().values / pd.Series(v).rolling(180, min_periods=60).mean().values
            ts = pd.to_datetime(df["timestamp"])
            fc = df["forecast"].values.astype(float)
            reg = df["regime"].astype(str).values
            for i in range(0, n-H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, fc=fc[i], reg=reg[i],
                                 ret180=ret180[i], ret6=ret6[i], ret18=ret18[i], vol=vol[i],
                                 streak=streak[i], vratio=vratio[i], wd=ts.iloc[i].weekday()))
    G = pd.DataFrame(rows)
    drift = G.groupby("coin")["fwd"].transform("mean")
    G["ex"] = G["fwd"] - drift
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["fwd7d_by_regime"] = G.groupby("reg").apply(summ)
    G["fcb"] = pd.cut(G["fc"], [-0.01, 0.001, 2, 5, 10, 21], labels=["0", "0-2", "2-5", "5-10", "10+"])
    out["fwd7d_by_forecast"] = G.groupby("fcb").apply(summ)
    G["q180"] = G.groupby("coin")["ret180"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd7d_by_30d_ret_quintile"] = G.groupby("q180").apply(summ)
    G["q18"] = G.groupby("coin")["ret18"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd7d_by_3d_ret_quintile"] = G.groupby("q18").apply(summ)
    G["q6"] = G.groupby("coin")["ret6"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd7d_by_1d_ret_quintile"] = G.groupby("q6").apply(summ)
    G["qv"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fwd7d_by_vol_tercile"] = G.groupby("qv").apply(summ)
    G["qvr"] = G.groupby("coin")["vratio"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fwd7d_by_volume_ratio_tercile"] = G.groupby("qvr").apply(summ)
    G["stb"] = pd.cut(G["streak"], [-99, -4, -2, 0, 2, 4, 99])
    out["fwd7d_by_streak"] = G.groupby("stb").apply(summ)
    # book: drift vs timing, by window
    br = []
    for coin in days:
        for w, d in days[coin].items():
            br.append(d.assign(coin=coin, w=w))
    D = pd.concat(br)
    # allocation per day: mean of bars' allocation per day
    al = []
    for coin in bars:
        for w, df in bars[coin].items():
            t = pd.to_datetime(df["timestamp"]).dt.floor("D")
            a = df.groupby(t)["postRebalance_current_allocation"].mean()
            al.append(pd.DataFrame({"day": a.index, "alloc": a.values, "coin": coin, "w": w}))
    A = pd.concat(al)
    D["day"] = pd.to_datetime(D["day"]).dt.floor("D")
    D = D.merge(A, on=["day", "coin", "w"], how="left")
    cm = D.groupby("coin")["coin_return"].transform("mean")
    D["drift_gain"] = D["alloc"]*cm
    out["book_split_%perday"] = pd.Series({"book_mean": 100*D["book_return"].mean(),
                                         "drift_part": 100*D["drift_gain"].mean(),
                                         "mean_alloc": D["alloc"].mean(),
                                         "share_days_in": (D["alloc"].abs() > 0.01).mean()})
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", lambda x: 100*x.mean()), coin_=("coin_return", lambda x: 100*x.mean()), alloc=("alloc", "mean"))
    D["wd"] = D["day"].dt.weekday
    out["coin_ret_by_weekday"] = D.groupby("wd")["coin_return"].agg(lambda x: pd.Series([100*x.mean(), x.mean()/(x.std()/np.sqrt(x.count()))]).round(3).tolist())
    # hour effect on 4h bars
    hr = []
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].values.astype(float)
            r = np.r_[c[1:]/c[:-1]-1, np.nan]
            hr.append(pd.DataFrame({"h": pd.to_datetime(df["timestamp"]).dt.hour, "r": r}))
    Hh = pd.concat(hr).dropna()
    out["bar_ret_by_hour"] = Hh.groupby("h")["r"].agg(n="count", mean_bp=lambda x: 1e4*x.mean(), t=lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
    return out

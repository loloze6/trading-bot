def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    # per-coin close series keyed by timestamp, per window, for market proxy
    closes = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            s = pd.Series(df["close"].values, index=pd.to_datetime(df["timestamp"]))
            closes[(coin, w)] = s
    rows = []
    for coin, wins in bars.items():
        allr = np.concatenate([df["close"].values[1:]/df["close"].values[:-1]-1 for df in wins.values()])
        mu = np.nanmean(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"]); n = len(df)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            sma50 = pd.Series(c).rolling(50, min_periods=30).mean().values
            ret20 = pd.Series(c).pct_change(20).values
            hi20 = pd.Series(c).shift(1).rolling(20, min_periods=20).max().values
            last = -99
            for i in range(n):
                if f[i] >= 10 and i - last > 5:
                    last = i
                    if i + 5 >= n: continue
                    t0, t5 = ts[i], ts[i+5]
                    mk = []
                    for oc in bars:
                        if oc == coin: continue
                        s = closes[(oc, w)]
                        if t0 in s.index and t5 in s.index:
                            mk.append(s[t5]/s[t0]-1)
                    mkt5 = np.mean(mk) if mk else np.nan
                    rows.append(dict(coin=coin, year=t0.year,
                        ex5=c[i+5]/c[i]-1-5*mu, raw5=c[i+5]/c[i]-1,
                        ex25=c[i+5]/c[i+1]-1-4*mu, mkt5=mkt5,
                        above50=(c[i] > sma50[i]) if not np.isnan(sma50[i]) else np.nan,
                        r20=ret20[i], brk=(c[i] > hi20[i]) if not np.isnan(hi20[i]) else np.nan,
                        clv=(c[i]-l[i])/(h[i]-l[i]) if h[i] > l[i] else np.nan))
    E = pd.DataFrame(rows)
    E["rel5"] = E["raw5"] - E["mkt5"]
    def summ(g, col="ex5"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), hit=(x > 0).mean(),
                              t=x.mean()/x.std(ddof=1)*np.sqrt(len(x)) if len(x) > 2 else np.nan))
    out = {}
    out["rel5_all"] = summ(E, "rel5").to_frame().T
    out["mkt5_all"] = summ(E, "mkt5").to_frame().T
    out["corr_ex5_mkt5"] = float(E[["raw5", "mkt5"]].corr().iloc[0, 1])
    E["r20pos"] = E["r20"] > 0
    E["r20q"] = pd.qcut(E["r20"], 3, labels=["low", "mid", "high"])
    out["by_r20q_rel5"] = E.groupby("r20q").apply(lambda g: summ(g, "rel5"))
    out["by_r20q_ex25"] = E.groupby("r20q").apply(lambda g: summ(g, "ex25"))
    out["by_breakout20"] = E.groupby("brk").apply(summ)
    out["by_breakout20_rel5"] = E.groupby("brk").apply(lambda g: summ(g, "rel5"))
    out["by_r20pos"] = E.groupby("r20pos").apply(summ)
    H = E[E.r20q == "high"]
    out["high_r20_by_year"] = H.groupby("year").apply(summ)
    out["high_r20_by_coin"] = H.groupby("coin").apply(summ)
    B = E[E.brk == True]
    out["breakout_by_year"] = B.groupby("year").apply(summ)
    out["breakout_by_coin"] = B.groupby("coin").apply(summ)
    E["clvq"] = pd.cut(E["clv"], [-0.01, 0.6, 0.85, 1.01], labels=["lowclose", "mid", "nearhigh"])
    out["by_close_location"] = E.groupby("clvq").apply(summ)
    out["breakout_trim"] = pd.DataFrame({"median": [B.ex5.median()], "trim5": [stats.trim_mean(B.ex5, 0.05)],
                                         "nonbrk_trim5": [stats.trim_mean(E[E.brk == False].ex5, 0.05)]})
    return out

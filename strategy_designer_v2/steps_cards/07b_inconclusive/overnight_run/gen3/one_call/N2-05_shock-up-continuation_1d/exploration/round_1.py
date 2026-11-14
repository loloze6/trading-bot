def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    # BTC daily returns by timestamp for market context
    btc = {}
    for w, df in bars["BTCUSD"].items():
        c = df["close"].values
        r = np.r_[np.nan, c[1:]/c[:-1]-1]
        for t, x in zip(pd.to_datetime(df["timestamp"]), r):
            btc[t] = x
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            absr = pd.Series(np.abs(r1))
            vol20 = absr.shift(1).rolling(20, min_periods=20).mean().values
            sma50 = pd.Series(c).rolling(50, min_periods=30).mean().values
            ret20 = pd.Series(c).pct_change(20).values
            last = -99
            for i in range(n):
                if f[i] >= 10 and i - last > 5:
                    last = i
                    if i + 5 >= n: continue
                    rows.append(dict(coin=coin, win=int(w[1:]), year=ts[i].year,
                        ex5=c[i+5]/c[i]-1-5*mu, ex1=c[i+1]/c[i]-1-mu,
                        ex25=c[i+5]/c[i+1]-1-4*mu,
                        z=r1[i]/vol20[i] if vol20[i] > 0 else np.nan,
                        above50=(c[i] > sma50[i]) if not np.isnan(sma50[i]) else np.nan,
                        r20=ret20[i], vol=vol20[i],
                        btc=btc.get(ts[i], np.nan),
                        btc5=np.nan, f=f[i], wd=ts[i].weekday()))
    E = pd.DataFrame(rows)
    def summ(g):
        x = g["ex5"]
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(),
                              hit=(x > 0).mean(), t=x.mean()/x.std(ddof=1)*np.sqrt(len(x)) if len(x) > 2 else np.nan))
    out = {}
    out["all"] = summ(E).to_frame().T
    out["by_coin"] = E.groupby("coin").apply(summ)
    out["by_year"] = E.groupby("year").apply(summ)
    E["zq"] = pd.qcut(E["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["by_z_quartile"] = E.groupby("zq").apply(summ)
    out["by_above50"] = E.groupby("above50").apply(summ)
    E["r20q"] = pd.qcut(E["r20"], 3, labels=["low", "mid", "high"])
    out["by_prior20d_ret"] = E.groupby("r20q").apply(summ)
    E["volq"] = E.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_vol_tercile"] = E.groupby("volq").apply(summ)
    E["btcup"] = pd.cut(E["btc"], [-1, 0, 0.03, 1], labels=["btc_down", "btc_0_3", "btc_gt3"])
    out["by_btc_same_day"] = E[E.coin != "BTCUSD"].groupby("btcup").apply(summ)
    out["ex1_ex25"] = pd.DataFrame({"ex1_mean": [E.ex1.mean()], "ex1_t": [stats.ttest_1samp(E.ex1, 0).statistic],
                                   "ex25_mean": [E.ex25.mean()], "ex25_t": [stats.ttest_1samp(E.ex25, 0).statistic],
                                   "ex5_skew": [stats.skew(E.ex5)], "ex5_trim5pct_mean": [stats.trim_mean(E.ex5, 0.05)]})
    return out

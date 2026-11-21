def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    book = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            f = b["forecast"].astype(float).fillna(0)
            raw = b.get("debug_info.components.support_touches.last_history_value")
            raw = raw.astype(float) if raw is not None else pd.Series(np.nan, index=b.index)
            fwd = c.shift(-5) / c - 1
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            ma50 = c.rolling(50, min_periods=20).mean()
            lo90 = b["low"].astype(float).rolling(90, min_periods=20).min()
            vol = np.log(c).diff().rolling(20, min_periods=10).std()
            vol60 = np.log(c).diff().rolling(60, min_periods=20).std()
            idx = np.arange(0, len(b) - 5, 5)
            for i in idx:
                rows.append(dict(coin=coin, win=w, fwd=fwd[i], f=f[i], raw=raw[i],
                                 r5=r5[i], r20=r20[i], trend=c[i] / ma50[i] - 1 if ma50[i] == ma50[i] else np.nan,
                                 dlo=c[i] / lo90[i] - 1, vr=vol[i] / vol60[i] if vol60[i] else np.nan,
                                 year=pd.Timestamp(b["timestamp"][i]).year))
            d = data["days"][coin][w]
            book.append(pd.DataFrame(dict(coin=coin, win=w, br=d["book_return"], cr=d["coin_return"])))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = df.groupby("coin")["fwd"].mean()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    df["act"] = df["f"] > 0
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=stats.ttest_1samp(g["ex"], 0).statistic if len(g) > 2 else np.nan, mean_fwd=g["fwd"].mean()))
    out = {}
    out["active_vs_not"] = df.groupby("act").apply(summ)
    a = df[df.act].copy()
    a["trend_q"] = pd.qcut(a["trend"], 4, labels=False, duplicates="drop")
    out["active_by_trend_q"] = a.groupby("trend_q").apply(summ).join(a.groupby("trend_q")["trend"].mean().rename("trend_mean"))
    a["r20_q"] = pd.qcut(a["r20"], 4, labels=False, duplicates="drop")
    out["active_by_r20_q"] = a.groupby("r20_q").apply(summ).join(a.groupby("r20_q")["r20"].mean().rename("r20_mean"))
    a["r5_q"] = pd.qcut(a["r5"], 4, labels=False, duplicates="drop")
    out["active_by_r5_q"] = a.groupby("r5_q").apply(summ).join(a.groupby("r5_q")["r5"].mean().rename("r5_mean"))
    a["dlo_q"] = pd.qcut(a["dlo"], 4, labels=False, duplicates="drop")
    out["active_by_dist_90d_low_q"] = a.groupby("dlo_q").apply(summ).join(a.groupby("dlo_q")["dlo"].mean().rename("dlo_mean"))
    a["f_q"] = pd.qcut(a["f"].rank(method="first"), 4, labels=False)
    out["active_by_forecast_q"] = a.groupby("f_q").apply(summ)
    a["vr_q"] = pd.qcut(a["vr"], 3, labels=False, duplicates="drop")
    out["active_by_volratio_q"] = a.groupby("vr_q").apply(summ)
    out["active_by_year"] = a.groupby("year").apply(summ)
    out["active_by_coin"] = a.groupby("coin").apply(summ)
    # inactive falls: all bars with r5<0 trend quartiles, as benchmark
    nf = df[(~df.act) & (df.r5 < 0)].copy()
    nf["trend_q"] = pd.qcut(nf["trend"], 4, labels=False, duplicates="drop")
    out["inactive_falls_by_trend_q"] = nf.groupby("trend_q").apply(summ)
    bk = pd.concat(book).dropna()
    out["book_by_win"] = bk.groupby("win").agg(book_mean=("br", "mean"), coin_mean=("cr", "mean")).T
    return out

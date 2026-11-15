def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    mu = {}
    for c in bars:
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].values
            al = df["postRebalance_current_allocation"].values
            n = len(df); yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n-20, 20):
                r60 = cl[i]/cl[i-60]-1 if i >= 60 else np.nan
                r20 = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                ex = cl[i+20]/cl[i]-1-20*mu[c]
                rows.append(dict(coin=c, win=w, year=yr[i], f=f[i], al=al[i], r60=r60, r20=r20, ex=ex, wex=al[i]*ex))
    R = pd.DataFrame(rows)
    A = R[R.f > 0].copy()
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), med=x.median(), t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out["active_ex_robust"] = pd.Series(dict(
        mean=A.ex.mean(), trim5=stats.trim_mean(A.ex, 0.05), mean_exZEC=A[A.coin != "ZECUSD"].ex.mean(),
        t_exZEC=tt(A[A.coin != "ZECUSD"].ex)["t"], top5_share_of_sum=A.ex.nlargest(5).sum()/A.ex.sum()))
    out["wex_by_coin"] = A.groupby("coin")["wex"].apply(tt).unstack()
    A["m60"] = pd.cut(A["r60"], [-10, 0, 0.2, 0.5, 100])
    out["h20_by_r60_bin"] = A.groupby("m60")["ex"].apply(tt).unstack()
    A["m20"] = pd.cut(A["r20"], [-10, -0.05, 0.05, 0.2, 100])
    out["h20_by_r20_bin"] = A.groupby("m20")["ex"].apply(tt).unstack()
    out["r60pos_by_coin"] = A[A.r60 > 0].groupby("coin")["ex"].apply(tt).unstack()
    out["r60pos_by_year"] = A[A.r60 > 0].groupby("year")["ex"].apply(tt).unstack()
    # book: market vs timing
    bk = []
    for c in bars:
        md = pd.concat([d["coin_return"].dropna() for d in days[c].values()]).mean()
        for w, df in bars[c].items():
            d = df.copy(); d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            pos = d.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = days[c][w].copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day"); dd["pos"] = pos
            dd["mkt"] = dd["pos"]*md
            dd["coin"] = c
            bk.append(dd[["book_return", "mkt", "coin"]])
    B = pd.concat(bk).dropna()
    out["book_mean_vs_market_part"] = pd.Series(dict(book_mean=B.book_return.mean(), market_part=B.mkt.mean(), timing=B.book_return.mean()-B.mkt.mean()))
    return out

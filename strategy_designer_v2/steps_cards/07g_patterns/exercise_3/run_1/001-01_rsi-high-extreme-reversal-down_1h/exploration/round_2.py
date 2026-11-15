def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows1 = []; rowsH = {24: [], 72: []}
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]  # forward 1-bar
            vol = pd.Series(np.r_[np.nan, c[1:]/c[:-1]-1]).rolling(168).std().values
            for i in range(n-1):
                rows1.append((coin, w, ts.iloc[i].hour, ts.iloc[i].weekday(), r1[i]))
            for H in rowsH:
                p72 = np.full(n, np.nan); p72[72:] = c[72:]/c[:-72]-1
                p168 = np.full(n, np.nan); p168[168:] = c[168:]/c[:-168]-1
                fwd = np.full(n, np.nan); fwd[:-H] = c[H:]/c[:-H]-1
                for i in range(0, n-H, H):
                    rowsH[H].append(dict(coin=coin, w=w, fwd=fwd[i], p72=p72[i], p168=p168[i],
                                         z72=p72[i]/(vol[i]*np.sqrt(72)) if vol[i] > 0 else np.nan))
    R = pd.DataFrame(rows1, columns=["coin","w","hour","wd","r"])
    R["ex"] = R["r"] - R.groupby("coin")["r"].transform("mean")
    def summ(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x)))))
    hr = R.groupby(["hour","coin"])["ex"].apply(summ).unstack([1,2])
    out["1h fwd ex by hour"] = hr
    out["1h fwd ex by weekday"] = R.groupby(["wd","coin"])["ex"].apply(summ).unstack([1,2])
    for H, rr in rowsH.items():
        g = pd.DataFrame(rr)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        for col in ["p72","z72","p168"]:
            g["q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
            out[f"fwd{H} ex by {col} q"] = g.groupby(["q","coin"])["ex"].apply(summ).unstack([1,2])
            out[f"spearman {col} fwd{H}"] = g.dropna(subset=[col,"fwd"]).groupby("coin").apply(lambda d: pd.Series(dict(n=len(d), rho=stats.spearmanr(d[col], d.fwd)[0])))
    # book: market part vs timing
    res = []
    for coin in bars:
        mu = pd.concat([days[coin][w]["coin_return"] for w in days[coin]]).mean()
        for w, df in bars[coin].items():
            df = df.copy(); df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            a = df.groupby("day")["postRebalance_current_allocation"].mean()
            res.append(dict(coin=coin, w=w, alloc=a.mean(), mu=mu))
    B = pd.DataFrame(res); B["market_part"] = B.alloc*B.mu
    out["book market part"] = B.groupby("coin")[["alloc","mu","market_part"]].mean()
    # coin return on the book's best/worst days
    D = pd.concat([days[c][w].assign(coin=c) for c in days for w in days[c]]).dropna(subset=["book_return"])
    D["bq"] = D.groupby("coin")["book_return"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["coin ret by book-day quintile"] = D.groupby(["coin","bq"])[["book_return","coin_return"]].mean()
    return out

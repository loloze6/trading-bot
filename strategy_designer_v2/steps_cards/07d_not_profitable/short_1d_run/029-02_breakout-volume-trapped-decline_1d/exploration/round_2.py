def explore(data):
    import numpy as np, pandas as pd
    rows = []
    bk = []
    for coin, wins in data["bars"].items():
        r5all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            r5all += list(c[idx + 5] / c[idx] - 1)
        drift = np.mean(r5all); usual = np.std(r5all)
        dmean = []
        for w, d in data["days"][coin].items():
            dmean += list(d["coin_return"].dropna())
        dm = np.mean(dmean)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]
            r20 = c / c.shift(20) - 1
            r1 = c / c.shift(1) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            hi20 = h.rolling(20).max()
            depth = c / hi20 - 1
            f = b["forecast"].fillna(0).values
            n = len(b)
            for start in range(0, n, 5):
                cell = [i for i in range(start, min(start + 5, n)) if f[i] < 0]
                if not cell: continue
                i = cell[0]
                if i + 5 >= n: continue
                ret = c.iloc[i + 5] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, su=-(ret - drift), st=-ret,
                                 r20=r20.iloc[i], vratio=vol20.iloc[i] / vol60.iloc[i],
                                 vol20=vol20.iloc[i], depth_v=depth.iloc[i] / vol20.iloc[i]))
        for w, d in data["days"][coin].items():
            b = wins[w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.merge(alloc.rename("alloc").reset_index(), on="day", how="left")
            dd["mkt"] = dd["alloc"] * dm
            dd["coin"] = coin
            bk.append(dd)
    R = pd.DataFrame(rows)
    B = pd.concat(bk)
    def summ(g):
        x = g["su"]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              total=g["st"].mean()))
    out = {}
    R["r20_hi"] = R["r20"] > R["r20"].median()
    R["vol_hi"] = R["vol20"] > R["vol20"].median()
    out["r20_x_vol"] = R.groupby(["r20_hi", "vol_hi"]).apply(summ)
    out["by_r20_tercile"] = R.groupby(pd.qcut(R["r20"], 3)).apply(summ)
    out["by_vratio"] = R.groupby(pd.qcut(R["vratio"], 3)).apply(summ)
    out["by_depth_v"] = R.groupby(pd.qcut(R["depth_v"], 3)).apply(summ)
    out["corr"] = R[["su", "r20", "vratio", "depth_v"]].corr()["su"]
    act = B[B["alloc"].abs() > 1e-6]
    out["book_split"] = pd.Series(dict(book_mean=B["book_return"].mean(), mkt_part=B["mkt"].fillna(0).mean(),
                                       timing=B["book_return"].mean() - B["mkt"].fillna(0).mean(),
                                       share_days_in=len(act) / len(B), mean_alloc_in=act["alloc"].mean(),
                                       in_day_book=act["book_return"].mean(), in_day_coin=act["coin_return"].mean()))
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin drift over 5 bars, non-overlapping, all windows
        r5all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            r5all += list(c[idx + 5] / c[idx] - 1)
        drift = np.mean(r5all); usual = np.std(r5all)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; v = b["volume"]
            ph = h.shift(1).rolling(20).max()
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            hi20 = h.rolling(20).max()
            lo20 = b["low"].rolling(20).min()
            pos = (c - lo20) / (hi20 - lo20)
            vr = v / v.rolling(20).mean()
            r1 = c / c.shift(1) - 1
            vol20 = r1.rolling(20).std()
            f = b["forecast"].fillna(0).values
            n = len(b)
            for start in range(0, n, 5):
                cell = [i for i in range(start, min(start + 5, n)) if f[i] < 0]
                if not cell: continue
                i = cell[0]
                if i + 5 >= n: continue
                ret = c.iloc[i + 5] / c.iloc[i] - 1
                # did a new 20-day high come within next 5 bars
                newhigh = (c.iloc[i+1:i+6].values > hi20.iloc[i]).any()
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 short_unusual=-(ret - drift), short_total=-ret, strength=-(ret-drift)/usual,
                                 fc=abs(f[i]), r20=r20.iloc[i], r60=r60.iloc[i], pos=pos.iloc[i],
                                 r1=r1.iloc[i], vol20=vol20.iloc[i], newhigh=newhigh,
                                 depth=c.iloc[i] / hi20.iloc[i] - 1))
        for w, d in data["days"][coin].items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            daily.append(dd)
    R = pd.DataFrame(rows)
    D = pd.concat(daily)
    def summ(g):
        x = g["short_unusual"]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                              total=g["short_total"].mean(), hit=(g["short_total"]>0).mean()))
    out = {}
    out["all"] = summ(R)
    out["by_coin"] = R.groupby("coin").apply(summ)
    out["by_year"] = R.groupby("year").apply(summ)
    for col in ["fc", "r20", "r60", "pos", "r1", "vol20", "depth"]:
        q = pd.qcut(R[col], 4, duplicates="drop")
        out["by_" + col] = R.groupby(q).apply(summ)
    out["newhigh_share"] = R["newhigh"].mean()
    out["by_r60_sign"] = R.groupby(R["r60"] > 0).apply(summ)
    out["corr_unusual"] = R[["short_unusual","fc","r20","r60","pos","r1","vol20","depth"]].corr()["short_unusual"]
    # book daily by year
    Dg = D.groupby(["year"]).agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","count"))
    out["book_by_year"] = Dg
    # book by in-position vs coin return
    return out

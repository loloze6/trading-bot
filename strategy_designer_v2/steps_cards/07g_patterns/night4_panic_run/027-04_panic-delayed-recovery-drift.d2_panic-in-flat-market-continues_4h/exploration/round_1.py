def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            r6 = c / c.shift(6) - 1
            rng = b["high"].rolling(6).max() / b["low"].rolling(6).min() - 1
            usual = r1.rolling(180, min_periods=60).std() * np.sqrt(6)
            urng = rng.rolling(180, min_periods=60).mean()
            z6 = r6 / usual
            panic = (-z6).clip(lower=0) * (rng / urng)
            vol30 = r1.rolling(30, min_periods=20).std()
            vrank = vol30.rolling(180, min_periods=60).rank(pct=True)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for h in (6, 18, 42, 78):
                idx = np.arange(0, n - h, h)
                f = c.shift(-h) / c - 1
                for i in idx:
                    rows.append((coin, w, h, i, f.iloc[i], z6.iloc[i], panic.iloc[i],
                                 vrank.iloc[i], r1.iloc[i] / (vol30.iloc[i] if vol30.iloc[i] else np.nan),
                                 ts.iloc[i].weekday(), ts.iloc[i].hour, b["regime"].iloc[i]))
    D = pd.DataFrame(rows, columns=["coin","w","h","i","fwd","z6","panic","vrank","z1","wd","hr","regime"])
    D["drift"] = D.groupby(["coin","h"])["fwd"].transform("mean")
    D["un"] = D["fwd"] - D["drift"]
    out = {}
    def summ(g):
        x = g["un"].dropna()
        return pd.Series({"n": len(x), "mean_un": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "mean_tot": g["fwd"].mean()})
    # 24h z-return quintiles vs forward unusual move, by horizon
    D["zq"] = D.groupby(["coin","h"])["z6"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["z6 quintile x horizon"] = D.groupby(["h","zq"]).apply(summ).reset_index()
    # panic score: zero vs positive tertiles, horizon 78 and 42
    P = D[D["h"].isin([42,78])].copy()
    P["pq"] = np.where(P["panic"]>0, P.groupby(["coin","h"])["panic"].transform(lambda s: pd.qcut(s.where(s>0), 3, labels=False, duplicates="drop")), -1)
    out["panic tertile (-1=none) x h"] = P.groupby(["h","pq"]).apply(summ).reset_index()
    out["panic tertile x regime h78"] = P[P.h==78].assign(flat=P["regime"]=="mean_reversion").groupby(["flat","pq"]).apply(summ).reset_index()
    # vol level vs forward
    D["vq"] = pd.cut(D["vrank"], [0,.2,.4,.6,.8,1.0], labels=False, include_lowest=True)
    out["vol rank quintile x h"] = D[D.h.isin([6,42,78])].groupby(["h","vq"]).apply(summ).reset_index()
    # after large 4h moves, next day
    E = D[D.h==6].copy()
    E["z1b"] = pd.cut(E["z1"], [-99,-3,-2,-1,1,2,3,99])
    out["4h z-move bin -> next 24h"] = E.groupby("z1b").apply(summ).reset_index()
    out["hour -> next 24h"] = E.groupby("hr").apply(summ).reset_index()
    out["weekday -> next 24h"] = E.groupby("wd").apply(summ).reset_index()
    out["coin x z6 extremes h78"] = D[(D.h==78)&(D.zq.isin([0,4]))].groupby(["coin","zq"]).apply(summ).reset_index()
    # book
    br = []
    for coin, ws in days.items():
        for w, d in ws.items():
            br.append(d.assign(coin=coin, w=w))
    B = pd.concat(br)
    out["book by coin"] = B.groupby("coin").agg(mean_book=("book_return","mean"), sd=("book_return","std"), mean_coin=("coin_return","mean")).reset_index()
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    allret = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < H + 2:
                continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # signed streak
            st = np.zeros(n)
            for i in range(1, n):
                if r1[i] > 0:
                    st[i] = st[i-1] + 1 if st[i-1] > 0 else 1
                elif r1[i] < 0:
                    st[i] = st[i-1] - 1 if st[i-1] < 0 else -1
                else:
                    st[i] = 0
            fwd = np.full(n, np.nan)
            fwd[:n-H] = c[H:] / c[:-H] - 1
            past5 = np.full(n, np.nan); past5[H:] = c[H:] / c[:-H] - 1
            past20 = np.full(n, np.nan); past20[20:] = c[20:] / c[:-20] - 1
            vol20 = pd.Series(r1).rolling(20).std().values
            vol60 = pd.Series(r1).rolling(60).std().values
            ts = pd.to_datetime(b["timestamp"])
            alloc = b["postRebalance_current_allocation"].astype(float).values
            for i in range(0, n, H):
                if np.isnan(fwd[i]):
                    continue
                rows.append(dict(coin=coin, win=w, streak=st[i], r1=r1[i], fwd=fwd[i],
                                 past5=past5[i], past20=past20[i], vol20=vol20[i], vol60=vol60[i],
                                 wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year, alloc=alloc[i],
                                 fc=float(b["forecast"].iloc[i]), day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd"].transform("mean")
    sd = d.groupby("coin")["fwd"].transform("std")
    d["unus"] = d["fwd"] - drift
    d["z"] = d["unus"] / sd
    def summ(g):
        x = g["unus"]
        return pd.Series({"n": len(x), "mean_unus": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "mean_z": g["z"].mean()})
    out = {}
    d["sb"] = d["streak"].clip(-5, 5)
    out["by_streak"] = d.groupby("sb").apply(summ)
    out["by_streak_coin_corr"] = d.groupby("coin").apply(lambda g: pd.Series({"corr_streak": stats.spearmanr(g["streak"], g["unus"])[0], "n": len(g)}))
    # past returns scaled by vol
    d["p5z"] = d["past5"] / (d["vol60"] * np.sqrt(5))
    d["p20z"] = d["past20"] / (d["vol60"] * np.sqrt(20))
    d["r1z"] = d["r1"] / d["vol60"]
    for col in ["r1z", "p5z", "p20z"]:
        dd = d.dropna(subset=[col])
        dd = dd.assign(q=dd.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop")))
        out["by_" + col + "_quintile"] = dd.groupby("q").apply(summ)
    # vol regime
    dd = d.dropna(subset=["vol20", "vol60"]).copy()
    dd["vr"] = dd["vol20"] / dd["vol60"]
    dd["q"] = dd.groupby("coin")["vr"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_volratio_tercile"] = dd.groupby("q").apply(summ)
    dd["q2"] = dd.groupby("coin")["vol60"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_vol60_tercile"] = dd.groupby("q2").apply(summ)
    out["by_weekday"] = d.groupby("wd").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    # book daily by year
    days = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            days.append(t.assign(coin=coin, win=w))
    D = pd.concat(days)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out

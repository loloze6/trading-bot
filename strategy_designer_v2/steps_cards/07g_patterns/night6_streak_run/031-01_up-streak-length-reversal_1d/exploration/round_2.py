def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol60 = pd.Series(r1).rolling(60).std().values
            ts = pd.to_datetime(b["timestamp"])
            alloc = b["postRebalance_current_allocation"].astype(float).values
            for H in (1, 3, 5):
                fwd = np.full(n, np.nan)
                if n > H:
                    fwd[:n-H] = c[H:] / c[:-H] - 1
                for i in range(0, n, H):
                    if np.isnan(fwd[i]):
                        continue
                    recs.append(dict(H=H, coin=coin, win=w, r1z=r1[i] / vol60[i] if vol60[i] > 0 else np.nan,
                                     fwd=fwd[i], wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year,
                                     alloc=alloc[i], nxt=(c[i+1]/c[i]-1) if i+1 < n else np.nan))
    d = pd.DataFrame(recs)
    d["unus"] = d["fwd"] - d.groupby(["H", "coin"])["fwd"].transform("mean")
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series({"n": len(x), "mean_unus": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    d1 = d[d.H == 1]
    out["wd_H1"] = d1.groupby("wd").apply(summ)
    out["wd_H1_MonTue_vs_rest_by_coin"] = d1.assign(mt=d1.wd.isin([0, 1])).groupby(["coin", "mt"])["unus"].mean().unstack()
    out["wd_H1_MonTue_vs_rest_by_year"] = d1.assign(mt=d1.wd.isin([0, 1])).groupby(["year", "mt"])["unus"].mean().unstack()
    dd = d.dropna(subset=["r1z"]).copy()
    dd["q"] = dd.groupby(["H", "coin"])["r1z"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["r1z_q_by_H"] = dd.groupby(["H", "q"]).apply(summ)
    top = dd[dd.q == 4]
    out["r1z_top_H5_by_coin"] = top[top.H == 5].groupby("coin").apply(summ)
    out["r1z_top_H5_by_year"] = top[top.H == 5].groupby("year").apply(summ)
    # book: position vs drift
    out["mean_alloc_by_coin"] = d1.groupby("coin")["alloc"].mean()
    days = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            days.append(t.assign(coin=coin))
    D = pd.concat(days)
    Dm = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book_daily_corr_with_coins"] = float(Dm.corr().iloc[0, 1])
    out["book_mean_daily"] = float(Dm["book_return"].mean())
    # gain from position*drift vs timing
    d1 = d1.dropna(subset=["nxt"])
    mu = d1.groupby("coin")["nxt"].transform("mean")
    out["drift_part"] = float((d1["alloc"] * mu).mean())
    out["timing_part"] = float((d1["alloc"] * (d1["nxt"] - mu)).mean())
    return out

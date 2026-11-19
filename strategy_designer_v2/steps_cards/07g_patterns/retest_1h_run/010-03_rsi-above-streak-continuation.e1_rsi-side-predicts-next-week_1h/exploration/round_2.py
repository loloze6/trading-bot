def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    def grid(h, lb):
        rows = []
        for coin in bars:
            for w, b in bars[coin].items():
                c = b["close"].values; n = len(c)
                ts = pd.to_datetime(b["timestamp"].values)
                lr = np.r_[np.nan, np.diff(np.log(c))]
                for i in range(0, n - h, h):
                    if i < lb: continue
                    vol = np.nanstd(lr[max(1,i-168):i+1])
                    rows.append(dict(coin=coin, w=w, past=c[i]/c[i-lb]-1, fut=c[i+h]/c[i]-1, vol=vol, hour=ts[i].hour))
        d = pd.DataFrame(rows)
        d["ex"] = d["fut"] - d.groupby("coin")["fut"].transform("mean")
        d["z"] = d["past"]/(d["vol"]*np.sqrt(lb))
        return d
    res = {}
    for h, lb in [(24,24),(24,72),(72,72),(168,168),(24,168),(6,6)]:
        d = grid(h, lb)
        for coin, g in d.groupby("coin"):
            r, p = stats.pearsonr(g["z"], g["ex"])
            res[(h, lb, coin)] = dict(corr=r, n=len(g), t=r*np.sqrt((len(g)-2)/(1-r**2)))
        r, p = stats.pearsonr(d["z"], d["ex"])
        res[(h, lb, "all")] = dict(corr=r, n=len(d), t=r*np.sqrt((len(d)-2)/(1-r**2)))
    out["past_z_vs_future_ex"] = pd.DataFrame(res).T
    d = grid(24, 24)
    d["zq"] = d.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["fut24_by_past24z_quintile"] = d.groupby("zq")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d["vq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["rev24_corr_by_volterc"] = d.groupby("vq").apply(lambda g: pd.Series(dict(corr=g["z"].corr(g["ex"]), n=len(g))))
    # weekday on daily coin returns
    D = pd.concat([x.assign(coin=c, w=w) for c in days for w, x in days[c].items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["coin_daily_by_weekday"] = D.groupby("wd")["coin_return"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["book_daily_by_weekday"] = D.groupby("wd")["book_return"].agg(["mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # book: gross vs fee daily; market vs timing
    hb = []
    for coin in bars:
        mret = np.concatenate([np.r_[b["close"].values[1:]/b["close"].values[:-1]-1] for b in bars[coin].values()]).mean()
        for w, b in bars[coin].items():
            c = b["close"].values; a = b["postRebalance_current_allocation"].values
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            fee = (b["total_portfolio_value"].values - b["postRebalance_total_value"].values)/b["total_portfolio_value"].values
            ch = np.abs(a - b["previous_allocation"].values)
            hb.append(pd.DataFrame(dict(coin=coin, gross=a*r1, mkt=a*mret, fee=fee, ch=ch, a=a)))
    H = pd.concat(hb)
    out["per_day_gross_mkt_fee"] = H.groupby("coin")[["gross","mkt","fee"]].mean()*24
    H["chq"] = pd.cut(H["ch"], [-1e-12, 1e-9, 0.01, 0.05, 0.2, 10])
    out["fee_share_by_change_size"] = H.groupby("chq")["fee"].agg(["sum","count"]).assign(share=lambda x: x["sum"]/x["sum"].sum())
    out["mean_abs_alloc"] = H.groupby("coin")["a"].apply(lambda s: s.abs().mean())
    return out

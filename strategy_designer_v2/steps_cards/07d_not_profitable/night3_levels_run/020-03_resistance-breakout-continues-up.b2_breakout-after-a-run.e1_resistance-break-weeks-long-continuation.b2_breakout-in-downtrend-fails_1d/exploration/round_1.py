def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            f = b["forecast"].values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            f30 = b.get("debug_info.components.fall30.last_history_value")
            brk = b.get("debug_info.components.break.last_history_value")
            # entries: allocation goes from >=0 to <0
            for t in range(n):
                if alloc[t] < 0 and prev[t] >= 0 and t + 20 < n:
                    r20 = c[t+20]/c[t]-1
                    r1 = c[t]/c[t-1]-1 if t>=1 else np.nan
                    r10b = c[t]/c[t-10]-1 if t>=10 else np.nan
                    r60b = c[t]/c[t-60]-1 if t>=60 else np.nan
                    hi = c[max(0,t-60):t+1].max()
                    lo = c[max(0,t-60):t+1].min()
                    pos = (c[t]-lo)/(hi-lo) if hi>lo else np.nan
                    vol = np.std(np.diff(np.log(c[max(0,t-30):t+1])))
                    rows.append(dict(coin=coin, w=w, yr=yr[t], r20=r20, short_gain=-r20,
                                     f30=f30.iloc[t] if f30 is not None else np.nan,
                                     brk=brk.iloc[t] if brk is not None else np.nan,
                                     r1=r1, r10b=r10b, r60b=r60b, pos=pos, vol=vol,
                                     fc=f[t]))
    df = pd.DataFrame(rows)
    out["n_entries"] = len(df)
    def summ(g):
        return pd.Series({"n": len(g), "mean_short_gain": g.short_gain.mean(),
                          "t": g.short_gain.mean()/(g.short_gain.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                          "share_win": (g.short_gain>0).mean()})
    out["all"] = summ(df)
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("yr").apply(summ)
    for col in ["f30","brk","r1","r10b","r60b","pos","vol"]:
        d = df.dropna(subset=[col])
        if len(d) > 20:
            q = pd.qcut(d[col], 4, labels=False, duplicates="drop")
            g = d.groupby(q).apply(summ)
            g["mean_feat"] = d.groupby(q)[col].mean()
            out["q_"+col] = g
            out["rho_"+col] = stats.spearmanr(d[col], d.short_gain)[0]
    # coin drift per 20 days, by year (non-overlapping)
    dr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values; yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0, len(c)-20, 20):
                dr.append(dict(yr=yr[i], r=c[i+20]/c[i]-1))
    dr = pd.DataFrame(dr)
    out["drift20_by_year"] = dr.groupby("yr").r.agg(["mean","count"])
    # book daily by year and window
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["w"] = w; d["coin"]=coin
            d["yr"] = pd.to_datetime(d["day"]).dt.year
            dd.append(d)
    dd = pd.concat(dd)
    day = dd.groupby(["w","day"]).agg(book=("book_return","mean"), coin=("coin_return","mean"), yr=("yr","first")).dropna()
    out["book_by_window"] = day.groupby("w").agg(book_mean=("book","mean"), coin_mean=("coin","mean"), n=("book","size"))
    out["book_by_year"] = day.groupby("yr").agg(book_mean=("book","mean"), coin_mean=("coin","mean"), n=("book","size"))
    return out

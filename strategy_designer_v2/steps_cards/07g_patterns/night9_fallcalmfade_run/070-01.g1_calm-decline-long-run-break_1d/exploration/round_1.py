def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); o = b["open"].values.astype(float)
            h = b["high"].values.astype(float); l = b["low"].values.astype(float)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            n1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            n3 = np.r_[c[3:]/c[:-3]-1, [np.nan]*3]
            # down run length before t (ending t-1), up run length
            dr = np.zeros(len(c)); ur = np.zeros(len(c))
            for i in range(1, len(c)):
                if r[i] < 0: dr[i] = dr[i-1]+1; ur[i]=0
                elif r[i] > 0: ur[i] = ur[i-1]+1; dr[i]=0
            prev_dr = np.r_[0, dr[:-1]]; prev_ur = np.r_[0, ur[:-1]]
            vol = pd.Series(r).rolling(20, min_periods=10).std().shift(1).values
            rng = (h-l)/c
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D").values,
                               "wd": ts.dt.weekday.values, "yr": ts.dt.year.values,
                               "fc": b["regime"].eq("unknown").values,
                               "r": r, "n1x": n1-mu, "n3x": n3-3*mu, "pdr": prev_dr, "pur": prev_ur,
                               "rz": r/vol, "clpos": (c-l)/np.where(h-l>0,h-l,np.nan),
                               "fcst": b["forecast"].values})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    def summ(g, col="n1x"):
        x = g[col].dropna()
        n = len(x)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n))})
    out = {}
    up = D[(D.r > 0)]
    brk = up[up.pdr >= 1].copy()
    brk["runcls"] = np.clip(brk.pdr, 1, 5)
    out["break_next1_by_run_fc"] = brk.groupby(["fc", "runcls"]).apply(summ).round(4)
    out["break_next3_by_run_fc"] = brk.groupby(["fc", "runcls"]).apply(lambda g: summ(g, "n3x")).round(4)
    # break-day size in falling calm, run>=2
    b2 = brk[brk.fc].copy()
    b2["szq"] = pd.qcut(b2.rz, 3, labels=["small", "mid", "large"])
    out["fc_break_by_upsize"] = b2.groupby(["szq"]).apply(summ).round(4)
    b2["clq"] = pd.cut(b2.clpos, [0, .5, .8, 1.01], labels=["lowclose", "mid", "highclose"])
    out["fc_break_by_closepos"] = b2.groupby("clq").apply(summ).round(4)
    # down days after down runs in falling calm (continuation?)
    dn = D[(D.r < 0)].copy(); dn["runcls"] = np.clip(dn.pdr, 0, 4)
    out["down_day_next1_by_prior_downrun_fc"] = dn.groupby(["fc", "runcls"]).apply(summ).round(4)
    # mirror: down day ending up run
    dbrk = D[(D.r < 0) & (D.pur >= 1)].copy(); dbrk["runcls"] = np.clip(dbrk.pur, 1, 5)
    out["downbreak_of_uprun_next1_fc"] = dbrk.groupby(["fc", "runcls"]).apply(summ).round(4)
    # big moves by regime
    D["zq"] = pd.cut(D.rz, [-99, -2, -1, 1, 2, 99])
    out["next1_by_rz_fc"] = D.groupby(["fc", "zq"]).apply(summ).round(4)
    out["next1_by_weekday_fc"] = D[D.fc].groupby("wd").apply(summ).round(4)
    out["share_fc_by_year"] = D.groupby("yr").fc.mean().round(3)
    out["fc_break_run2p_by_year"] = brk[brk.fc & (brk.pdr >= 2)].groupby("yr").apply(summ).round(4)
    # book daily
    bk = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; bk.append(d)
    B = pd.concat(bk); B["day"] = pd.to_datetime(B["day"])
    bd = B.groupby("day").book_return.mean().dropna()
    out["book_by_year"] = bd.groupby(bd.index.year).agg(["count", "mean", "std", lambda x: (x != 0).mean()]).round(5)
    out["book_top_loss_days_share"] = pd.Series({"sum_all": bd.sum(), "sum_worst10": bd.nsmallest(10).sum(), "sum_best10": bd.nlargest(10).sum()}).round(4)
    return out

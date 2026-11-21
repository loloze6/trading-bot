def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    # daily returns per window, z by coin over all windows, forward returns inside window
    rows = []
    for c in days:
        allr = pd.concat([d["coin_return"] for d in days[c].values()]).dropna()
        mu, sd = allr.mean(), allr.std()
        for w, d in days[c].items():
            d = d.reset_index(drop=True)
            r = d["coin_return"].values
            cl = d["close"].values
            n = len(d)
            # 20-day vol before
            for i in range(1, n):
                if np.isnan(r[i]): continue
                f1 = r[i+1] if i+1 < n else np.nan
                f3 = cl[i+3]/cl[i]-1 if i+3 < n else np.nan
                f5 = cl[i+5]/cl[i]-1 if i+5 < n else np.nan
                v20 = np.nanstd(r[max(1,i-19):i+1]) if i >= 10 else np.nan
                zv = r[i]/v20 if v20 and not np.isnan(v20) and v20 > 0 else np.nan
                rows.append(dict(coin=c, win=w, i=i, r=r[i], z=(r[i]-mu)/sd, zv=zv, f1=f1, f3=f3, f5=f5,
                                 year=pd.Timestamp(d["day"].values[i]).year,
                                 wd=pd.Timestamp(d["day"].values[i]).weekday(),
                                 br=d["book_return"].values[i]))
    D = pd.DataFrame(rows)
    D["zb"] = pd.cut(D["z"], [-99,-3,-2,-1,1,2,3,99])
    def tm(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out["f1_by_z"] = D.groupby("zb")["f1"].apply(tm).unstack()
    out["f3_by_z"] = D.groupby("zb")["f3"].apply(tm).unstack()
    out["f5_by_z"] = D.groupby("zb")["f5"].apply(tm).unstack()
    # vol-scaled z
    D["zvb"] = pd.cut(D["zv"], [-99,-3,-2,-1,1,2,3,99])
    out["f1_by_volz"] = D.groupby("zvb")["f1"].apply(tm).unstack()
    out["f3_by_volz"] = D.groupby("zvb")["f3"].apply(tm).unstack()
    # big down days (z<=-2): next-day by coin and by year, demeaned by coin mean
    cm = D.groupby("coin")["f1"].transform("mean")
    D["f1x"] = D["f1"] - cm
    big = D[D["z"] <= -2]
    out["bigdown_f1x_by_coin"] = big.groupby("coin")["f1x"].apply(tm).unstack()
    out["bigdown_f1x_by_year"] = big.groupby("year")["f1x"].apply(tm).unstack()
    up = D[D["z"] >= 2]
    out["bigup_f1x_by_coin"] = up.groupby("coin")["f1x"].apply(tm).unstack()
    out["bigup_f1x_by_year"] = up.groupby("year")["f1x"].apply(tm).unstack()
    # graded: spearman of z vs f1 within |z|>1
    s = D[(D["z"].abs() > 1)].dropna(subset=["f1"])
    r_, p_ = stats.spearmanr(s["z"], s["f1"]); out["tail_spearman_z_f1"] = f"rho={r_:.3f} p={p_:.4f} n={len(s)}"
    s = D[(D["z"] < -1)].dropna(subset=["f1"])
    r_, p_ = stats.spearmanr(s["z"], s["f1"]); out["down_tail_spearman"] = f"rho={r_:.3f} p={p_:.4f} n={len(s)}"
    # weekday t
    D["f0x"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    out["weekday_coin_x"] = D.groupby("wd")["f0x"].apply(tm).unstack()
    out["weekday_sat_by_year"] = D[D["wd"]==5].groupby("year")["f0x"].apply(tm).unstack()
    # book: worst days and context
    out["book_by_year"] = D.groupby("year")["br"].agg(["count","mean","std"])
    q = D["br"].quantile([0.01, 0.99])
    out["book_worst1pct_by_year"] = D[D["br"] <= q.iloc[0]].groupby("year")["br"].agg(["count","mean"])
    out["book_worst1pct_by_coin"] = D[D["br"] <= q.iloc[0]].groupby("coin")["br"].agg(["count","mean"])
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]
    # per coin decomposition of bar gains
    rows = []; allg = []
    for c in bars:
        segs = []
        for w, b in bars[c].items():
            b = b.copy()
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            segs.append(b)
        B = pd.concat(segs)
        mu = B["r1"].mean()
        a = B["postRebalance_current_allocation"].fillna(0)
        g = a * B["r1"]
        mkt = a * mu
        B["g"] = g; B["mkt"] = mkt; B["a"] = a; B["coin"] = c
        allg.append(B)
        rows.append({"coin": c, "mean_gain_bp": g.mean()*1e4, "market_part_bp": mkt.mean()*1e4,
                     "timing_bp": (g-mkt).mean()*1e4, "share_in_pos": (a.abs()>1e-6).mean(),
                     "coin_mu_bp": mu*1e4, "mean_alloc_in_pos": a[a.abs()>1e-6].mean()})
    out["by_coin"] = pd.DataFrame(rows).set_index("coin").round(3)
    G = pd.concat(allg)
    out["by_year"] = G.groupby("year").agg(gain_bp=("g", lambda x: x.mean()*1e4),
                                          mkt_bp=("mkt", lambda x: x.mean()*1e4),
                                          coin_r_bp=("r1", lambda x: x.mean()*1e4),
                                          in_pos=("a", lambda x: (x.abs()>1e-6).mean())).round(2)
    # gain by regime state: in trending regime vs not; split by allocation-held bars by ret60 terciles
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    net = T["net_profit_loss_percent"]
    s = net.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": net.mean(), "median_net": net.median(),
                               "win_share": (net>0).mean(), "top5pct_share_of_sum": s.head(max(1,len(s)//20)).sum()/s.sum(),
                               "sum_net": s.sum(), "sum_without_top10": s.iloc[10:].sum(),
                               "mean_dur_days": (T["duration_minutes"]/1440).mean(),
                               "median_dur_days": (T["duration_minutes"]/1440).median()}).round(3)
    T["durd"] = T["duration_minutes"]/1440
    T["durbin"] = pd.cut(T["durd"], [0,3.5,6.5,10.5,20.5,1e4])
    out["trades_by_duration"] = T.groupby("durbin").agg(n=("net_profit_loss_percent","size"),
                                 mean_net=("net_profit_loss_percent","mean"),
                                 sum_net=("net_profit_loss_percent","sum")).round(3)
    # forward returns non-overlapping, by state
    res = []
    for h in [1,3,5,10,20]:
        recs = []
        for c in bars:
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                cl = b["close"]
                rng = (b["high"]-b["low"])/cl
                rm = rng / rng.rolling(20).mean()
                r5 = cl/cl.shift(5)-1
                r20 = cl/cl.shift(20)-1
                fwd = cl.shift(-h)/cl-1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({"fwd": fwd.iloc[idx].values, "trend": (b["regime"].iloc[idx]=="trending").values,
                                  "rm": rm.iloc[idx].values, "r5": r5.iloc[idx].values, "r20": r20.iloc[idx].values,
                                  "coin": c})
                recs.append(d)
        D = pd.concat(recs).dropna(subset=["fwd"])
        mu = D.groupby("coin")["fwd"].transform("mean")
        D["ex"] = D["fwd"] - mu
        tr = D[D.trend]; nt = D[~D.trend]
        t1 = stats.ttest_ind(tr["ex"], nt["ex"], equal_var=False).statistic
        tt = tr.dropna(subset=["rm"])
        hi = tt[tt.rm > tt.rm.median()]; lo = tt[tt.rm <= tt.rm.median()]
        t2 = stats.ttest_ind(hi["ex"], lo["ex"], equal_var=False).statistic
        tr5 = tr.dropna(subset=["r5"])
        h5 = tr5[tr5.r5 > tr5.r5.median()]; l5 = tr5[tr5.r5 <= tr5.r5.median()]
        t3 = stats.ttest_ind(h5["ex"], l5["ex"], equal_var=False).statistic
        allr20 = D.dropna(subset=["r20"])
        up = allr20[allr20.r20>0]; dn = allr20[allr20.r20<=0]
        t4 = stats.ttest_ind(up["ex"], dn["ex"], equal_var=False).statistic
        res.append({"h": h, "n_trend": len(tr), "ex_trend_pct": tr["ex"].mean()*100,
                    "ex_notrend_pct": nt["ex"].mean()*100, "t_trend_minus_not": t1,
                    "rm_hi_minus_lo_pct": (hi["ex"].mean()-lo["ex"].mean())*100, "t_rm": t2,
                    "r5_hi_minus_lo_pct": (h5["ex"].mean()-l5["ex"].mean())*100, "t_r5": t3,
                    "r20up_minus_dn_pct": (up["ex"].mean()-dn["ex"].mean())*100, "t_r20": t4, "n_r20": len(allr20)})
    out["fwd_by_state"] = pd.DataFrame(res).set_index("h").round(3)
    # book daily: mean over coins
    days = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            days.append(d.assign(coin=c, w=w))
    DD = pd.concat(days)
    bk = DD.groupby(["w","day"])["book_return"].mean().dropna()
    hd = DD.groupby(["w","day"])["coin_return"].mean().dropna()
    out["book_by_window_mean_bp"] = (bk.groupby(level=0).mean()*1e4).round(2).describe().round(2)
    out["book_sharpe"] = float(bk.mean()/bk.std()*np.sqrt(365))
    out["hold_sharpe"] = float(hd.mean()/hd.std()*np.sqrt(365))
    return out

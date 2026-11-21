def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]
    # ---- book daily returns, market part vs timing
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["bv"] = b["postRebalance_total_value"]
            b["bret"] = b["total_portfolio_value"].shift(-1) / b["postRebalance_total_value"].shift(0) - 1
            # book return over bar incl next fee approx: use total value chain
            b["bret2"] = b["total_portfolio_value"].pct_change()
            b["coin"] = c; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["i"] = np.arange(len(b))
            rows.append(b[["coin","win","year","i","timestamp","close","ret1","pos","bret2","forecast",
                           "debug_info.components.break_touches.last_history_value"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["ret1"].mean()
    B["mu"] = B["coin"].map(mu)
    B["gain"] = B["pos"] * B["ret1"]
    B["mkt"] = B["pos"] * B["mu"]
    B["timing"] = B["gain"] - B["mkt"]
    # per-day mean across coins
    B["day"] = pd.to_datetime(B["timestamp"]).dt.floor("D")
    D = B.groupby(["win","day"])[["gain","mkt","timing","ret1"]].mean()
    out["book_parts_daily_mean"] = D.mean()
    out["book_parts_t"] = D.apply(lambda s: s.mean()/ (s.std()/np.sqrt(s.count())))
    out["mean_pos"] = B["pos"].mean()
    # by coin
    bc = B.groupby("coin").agg(gain=("gain","mean"), mkt=("mkt","mean"), timing=("timing","mean"),
                               pos=("pos","mean"), hold=("ret1","mean"))
    out["by_coin"] = bc.round(5)
    out["by_year"] = B.groupby("year").agg(gain=("gain","mean"), mkt=("mkt","mean"),
                                           timing=("timing","mean"), hold=("ret1","mean"), n=("gain","size")).round(5)
    # ---- trades concentration
    T = pd.concat([t.assign(coin=c) for c in trades for w,t in trades[c].items() if len(t)], ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades_summary"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(),
        "win_share": (p>0).mean(), "top5pct_sum_share": p.head(max(1,len(p)//20)).sum()/p.sum(),
        "sum_without_top5pct": p.iloc[len(p)//20:].sum(), "dur_days_median": T["duration_minutes"].median()/1440})
    # ---- event study: entry bars (forecast from 0 to >0)
    ev = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            r1 = cl/np.roll(cl,1)-1; r1[0]=np.nan
            n=len(cl)
            hi20 = pd.Series(cl).rolling(20).max().shift(1).values
            for i in range(1,n):
                d = {"coin":c,"win":w,"brk": f[i]>0 and f[i-1]<=0, "r1":r1[i],
                     "nh20": cl[i]>hi20[i] if not np.isnan(hi20[i]) else np.nan, "f":f[i]}
                for h in (1,3,5,10,20):
                    d["f%d"%h] = cl[i+h]/cl[i]-1 if i+h<n else np.nan
                ev.append(d)
    E = pd.DataFrame(ev)
    for h in (1,3,5,10,20):
        E["u%d"%h] = E["f%d"%h] - E.groupby("coin")["f%d"%h].transform("mean")
    def summ(g):
        r={}
        for h in (1,3,5,10,20):
            s=g["u%d"%h].dropna(); r["u%d"%h]=s.mean(); r["t%d"%h]=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        r["n"]=len(g); return pd.Series(r)
    out["breaks_vs_rest"] = E.groupby("brk").apply(summ).round(4)
    # control: non-break closes with same-size day return (bins of r1) & new 20d high
    E["r1bin"] = pd.qcut(E["r1"], 5, labels=False, duplicates="drop")
    out["by_r1bin_brk"] = E.groupby(["r1bin","brk"]).apply(lambda g: pd.Series({"u5":g["u5"].mean(),"u10":g["u10"].mean(),"u20":g["u20"].mean(),"n":len(g)})).round(4)
    out["by_newhigh20_brk"] = E.groupby(["nh20","brk"]).apply(lambda g: pd.Series({"u5":g["u5"].mean(),"u10":g["u10"].mean(),"u20":g["u20"].mean(),"n":len(g)})).round(4)
    out["break_forecast_values"] = E.loc[E.brk,"f"].describe().round(2)
    return out

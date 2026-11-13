def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    trows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            f = b["forecast"].fillna(0).values
            v = b["postRebalance_total_value"].values
            peak = np.maximum.accumulate(v)
            dd = v/peak - 1
            # bars since forecast became positive
            since = np.zeros(len(f)); k = 0
            for i in range(len(f)):
                k = k+1 if f[i] > 0 else 0
                since[i] = k
            for i in range(len(c)-1):
                rows.append((coin, w, f[i], alloc[i], c[i+1]/c[i]-1, dd[i], since[i]))
        for w, td in data["trades"][coin].items():
            if len(td):
                td = td.copy(); td["coin"] = coin; td["win"] = w
                td["last_in_win"] = pd.to_datetime(td.exit_time) >= pd.to_datetime(wins[w]["timestamp"].iloc[-1])
                trows.append(td)
    df = pd.DataFrame(rows, columns=["coin","win","f","alloc","r1","dd","since"])
    df["pnl"] = df.alloc*df.r1
    act = df[df.f > 0].copy()
    # alloc by forecast bucket and pnl contribution
    act["fb"] = pd.cut(act.f, [0,5,10,15,19.99,20.01])
    g = act.groupby("fb", observed=True)
    out["alloc_pnl_by_fbucket"] = pd.DataFrame({"mean_alloc": g.alloc.mean(), "pnl_bp": g.pnl.mean()*1e4, "pnl_sum": g.pnl.sum(), "r1_std_bp": g.r1.std()*1e4, "sharpe_d": g.pnl.mean()/g.pnl.std()})
    # pnl by age of the above-SMA episode
    act["age"] = pd.cut(act.since, [0,5,20,60,150,1e5])
    ga = act.groupby("age", observed=True)
    out["by_episode_age"] = pd.DataFrame({"n": ga.size(), "mean_f": ga.f.mean(), "mean_alloc": ga.alloc.mean(), "pnl_bp": ga.pnl.mean()*1e4, "r1_bp": ga.r1.mean()*1e4, "pnl_sum": ga.pnl.sum()})
    # drawdown state
    df["ddb"] = pd.cut(df.dd, [-1,-0.5,-0.3,-0.15,-0.05,0.0001])
    gd = df.groupby("ddb", observed=True)
    out["by_book_drawdown"] = pd.DataFrame({"n": gd.size(), "share_active": gd.f.apply(lambda x:(x>0).mean()), "mean_alloc": gd.alloc.mean()})
    # biggest daily losses: share at alloc>1
    lo = df[df.pnl < df.pnl.quantile(0.05)]
    out["worst5pct_days"] = pd.Series({"n": len(lo), "mean_alloc": lo.alloc.mean(), "share_alloc_gt1": (lo.alloc>1).mean(), "share_f20": (lo.f>=19.99).mean(), "sum_pnl": lo.pnl.sum(), "total_pnl": df.pnl.sum()})
    T = pd.concat(trows)
    T["days"] = T.duration_minutes/1440
    out["trades_end_of_window"] = pd.Series({"n_closed_by_window_end": int(T.last_in_win.sum()), "gross_closed_by_end": T[T.last_in_win].profit_loss_percent.mean(), "gross_other": T[~T.last_in_win].profit_loss_percent.mean()})
    T["ef"] = pd.cut(T.entry_forecast, [-0.01,2,5,10,20.01])
    ge = T.groupby("ef", observed=True)
    out["trades_by_entry_forecast"] = pd.DataFrame({"n": ge.size(), "mean_gross": ge.profit_loss_percent.mean(), "win": ge.profit_loss_percent.apply(lambda x:(x>0).mean()), "median_days": ge.days.median()})
    out["fee_vs_gross"] = pd.Series({"total_commission": T.total_commission.sum(), "gross_minus_net_pct_sum": (T.profit_loss_percent-T.net_profit_loss_percent).sum(), "trades_per_coin_window": len(T)/df.groupby(["coin","win"]).ngroups})
    return out

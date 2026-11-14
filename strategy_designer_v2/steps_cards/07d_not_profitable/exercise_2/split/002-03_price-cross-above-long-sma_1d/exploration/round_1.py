def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; trows = []; brows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            r = np.r_[np.diff(c)/c[:-1], np.nan]
            f = b["forecast"].fillna(0).values
            fwd20 = pd.Series(c).shift(-20).values/c - 1
            # coin regime: 50d trend and vol within window
            ret = pd.Series(c).pct_change()
            vol = ret.rolling(20).std().values
            tr = pd.Series(c).pct_change(20).values
            for i in range(len(c)-1):
                rows.append((coin, w, int(w[1:]), pd.Timestamp(b["timestamp"].iloc[i]).year, f[i], alloc[i], r[i+0] if False else (c[i+1]/c[i]-1), fwd20[i], vol[i], tr[i]))
        t = data["trades"][coin]
        for w, td in t.items():
            if len(td):
                td = td.copy(); td["coin"]=coin; td["win"]=w; trows.append(td)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; brows.append(d)
    df = pd.DataFrame(rows, columns=["coin","win","wn","year","f","alloc","r1","fwd20","vol","tr20"])
    df["pnl"] = df.alloc*df.r1
    act = df[df.f>0]
    out["active_share_and_alloc"] = pd.Series({"share_active": (df.f>0).mean(), "mean_alloc_active": act.alloc.mean(), "mean_f_active": act.f.mean(), "corr_f_alloc": act[["f","alloc"]].corr().iloc[0,1]})
    # forecast buckets
    act = act.copy()
    act["fb"] = pd.cut(act.f, [0,5,10,15,19.99,20.01])
    g = act.groupby("fb", observed=True)
    out["by_forecast_bucket"] = pd.DataFrame({"n": g.size(), "mean_r1_bp": g.r1.mean()*1e4, "mean_fwd20": g.fwd20.mean(), "hit20": g.fwd20.apply(lambda x:(x>0).mean()), "mean_vol": g.vol.mean()})
    out["flat_vs_active_r1_bp"] = pd.Series({"flat": df[df.f<=0].r1.mean()*1e4, "active": df[df.f>0].r1.mean()*1e4, "all": df.r1.mean()*1e4, "flat_fwd20": df[df.f<=0].fwd20.mean(), "active_fwd20": df[df.f>0].fwd20.mean()})
    # by year
    gy = df.groupby("year")
    out["by_year"] = pd.DataFrame({"pnl_bp_day": gy.pnl.mean()*1e4, "hold_bp_day": gy.r1.mean()*1e4, "share_active": gy.f.apply(lambda x:(x>0).mean()), "mean_alloc": gy.alloc.mean()})
    # vol terciles
    df["vt"] = pd.qcut(df.vol, 3, labels=["calm","mid","volatile"])
    df["mkt"] = np.where(df.tr20>0, "rising20", "falling20")
    gv = df.groupby(["vt","mkt"], observed=True)
    out["by_vol_trend"] = pd.DataFrame({"n": gv.size(), "pnl_bp": gv.pnl.mean()*1e4, "hold_bp": gv.r1.mean()*1e4, "share_active": gv.f.apply(lambda x:(x>0).mean()), "pnl_sum": gv.pnl.sum()})
    gc = df.groupby("coin")
    out["by_coin"] = pd.DataFrame({"pnl_bp": gc.pnl.mean()*1e4, "hold_bp": gc.r1.mean()*1e4, "share_active": gc.f.apply(lambda x:(x>0).mean())})
    # trades
    T = pd.concat(trows)
    T["days_held"] = T.duration_minutes/1440
    out["trades_summary"] = pd.Series({"n": len(T), "long_share": (T.side=="LONG").mean(), "median_days": T.days_held.median(), "mean_days": T.days_held.mean(), "mean_gross_pct": T.profit_loss_percent.mean(), "mean_net_pct": T.net_profit_loss_percent.mean(), "sum_gross": T.profit_loss_percent.sum(), "sum_net": T.net_profit_loss_percent.sum(), "win_rate_gross": (T.profit_loss_percent>0).mean(), "mean_win": T.profit_loss_percent[T.profit_loss_percent>0].mean(), "mean_loss": T.profit_loss_percent[T.profit_loss_percent<=0].mean()})
    T["db"] = pd.cut(T.days_held, [-1,1,3,10,30,1e5])
    gt = T.groupby("db", observed=True)
    out["trades_by_duration"] = pd.DataFrame({"n": gt.size(), "mean_gross": gt.profit_loss_percent.mean(), "mean_net": gt.net_profit_loss_percent.mean(), "sum_gross": gt.profit_loss_percent.sum()})
    # allocation changes per bar
    out["rebalance"] = pd.Series({"mean_abs_alloc_change": df.groupby(["coin","win"]).alloc.apply(lambda x: x.diff().abs().mean()).mean()})
    # drawdown of book per coin-window
    D = pd.concat(brows)
    dd = []
    for (c,w), d in D.groupby(["coin","win"]):
        v = d.book_value.values; h = d.close.values
        dd.append((c, v.min()/np.maximum.accumulate(v).max() if False else (v/np.maximum.accumulate(v)-1).min(), (h/np.maximum.accumulate(h)-1).min(), v[-1]/v[0]-1, h[-1]/h[0]-1))
    dd = pd.DataFrame(dd, columns=["coin","book_mdd","hold_mdd","book_ret","hold_ret"])
    out["window_dd"] = dd[["book_mdd","hold_mdd","book_ret","hold_ret"]].describe().loc[["mean","50%","min"]]
    out["book_vs_hold_window_ret_corr"] = float(dd.book_ret.corr(dd.hold_ret))
    return out

def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; dd = []; trows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["ret1"] = b["close"].pct_change().shift(-1)
            v = b["postRebalance_total_value"].astype(float)
            b["bookret1"] = v.shift(-1) / v - 1
            b["dist"] = b["debug_info.components.above_ma.last_history_value"].astype(float)
            b["coin"] = coin
            b["gross1"] = b["alloc"] * b["ret1"]
            rows.append(b[["coin","forecast","alloc","ret1","bookret1","dist","gross1"]])
            peak = v.cummax(); mdd = (v / peak - 1).min()
            c = b["close"].astype(float); cmdd = (c / c.cummax() - 1).min()
            tot = v.iloc[-1] / v.iloc[0] - 1; ctot = c.iloc[-1] / c.iloc[0] - 1
            dd.append(dict(coin=coin, win=w, book_mdd=mdd, coin_mdd=cmdd, book_tot=tot, coin_tot=ctot, maxalloc=b["alloc"].max()))
            t = data["trades"][coin][w].copy(); t["coin"] = coin; trows.append(t)
    B = pd.concat(rows, ignore_index=True)
    D = pd.DataFrame(dd); T = pd.concat(trows, ignore_index=True)
    out["window_dd_summary"] = D[["book_mdd","coin_mdd","book_tot","coin_tot","maxalloc"]].describe()
    out["share_windows_book_beats_coin"] = (D["book_tot"] > D["coin_tot"]).mean()
    # raw distance buckets for active bars, and all bars
    db = pd.cut(B["dist"], [-10, -0.2, -0.05, 0, 0.05, 0.1, 0.2, 0.4, 10])
    out["by_raw_distance"] = B.groupby(db).agg(n=("ret1","size"), coin_ret=("ret1","mean"), coin_sd=("ret1","std"),
                                               alloc=("alloc","mean"), gross=("gross1","mean"))
    # alloc vs leverage: per-unit-allocation return on active bars by alloc bucket
    act = B[B["alloc"] > 1e-9].copy()
    ab = pd.qcut(act["alloc"], 4)
    out["active_by_alloc_q"] = act.groupby(ab).agg(n=("ret1","size"), coin_ret=("ret1","mean"), coin_sd=("ret1","std"),
                                                    gross=("gross1","mean"), gross_sd=("gross1","std"))
    # unit-exposure comparison: Sharpe of coin on active vs flat bars
    flat = B[B["alloc"] <= 1e-9]
    out["sharpe_daily_coin"] = pd.Series({"active": act["ret1"].mean()/act["ret1"].std(),
                                          "flat": flat["ret1"].mean()/flat["ret1"].std(),
                                          "all": B["ret1"].mean()/B["ret1"].std(),
                                          "book_gross": B["gross1"].mean()/B["gross1"].std(),
                                          "t_active_minus_flat": stats.ttest_ind(act["ret1"].dropna(), flat["ret1"].dropna(), equal_var=False).statistic})
    # trades: entry forecast buckets and exit cause
    T["eb"] = pd.cut(T["entry_forecast"], [-0.01, 2, 5, 10, 20.01])
    out["trades_by_entry_forecast"] = T.groupby("eb").agg(n=("profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
                                                         win=("profit_loss_percent", lambda s: (s>0).mean()),
                                                         dur=("duration_minutes", lambda s: s.mean()/1440))
    out["trades_per_coin"] = T.groupby("coin").agg(n=("profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
                                                   median=("profit_loss_percent","median"))
    # gross pnl contribution share: top 10% trades
    s = T["profit_loss_percent"].sort_values(ascending=False)
    out["top_trade_share"] = pd.Series({"sum_all": s.sum(), "sum_top5pct": s.iloc[:int(len(s)*0.05)].sum(), "sum_losers": s[s<0].sum()})
    return out

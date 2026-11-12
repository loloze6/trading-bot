def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; trows = []; dd = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["ret1"] = b["close"].pct_change().shift(-1)
            b["fwd20"] = b["close"].shift(-20) / b["close"] - 1
            v = b["postRebalance_total_value"].astype(float)
            b["bookret1"] = v.shift(-1) / v - 1
            b["gross1"] = b["alloc"] * b["ret1"]
            b["dist"] = b["debug_info.components.above_ma.last_history_value"].astype(float)
            on = (b["forecast"] > 0).astype(int)
            grp = (on != on.shift()).cumsum()
            b["age"] = on.groupby(grp).cumcount() + 1
            b.loc[on == 0, "age"] = 0
            b["past60"] = b["close"] / b["close"].shift(60) - 1
            b["coin"] = coin
            rows.append(b[["coin","forecast","alloc","ret1","fwd20","bookret1","gross1","dist","age","past60"]])
            # drawdown episode attribution: worst drawdown, book vs alloc during it
            peak = v.cummax(); ddser = v / peak - 1
            i_tr = ddser.idxmin(); i_pk = v.loc[:i_tr].idxmax()
            seg = b.loc[i_pk:i_tr]
            dd.append(dict(dd=ddser.min(), len=len(seg), alloc_mean=seg["alloc"].mean(),
                           coin_move=seg["close"].iloc[-1] / seg["close"].iloc[0] - 1 if len(seg) > 0 else np.nan))
            t = data["trades"][coin][w].copy(); t["coin"] = coin; trows.append(t)
    B = pd.concat(rows, ignore_index=True); T = pd.concat(trows, ignore_index=True); D = pd.DataFrame(dd)
    out["dist_quantiles"] = B["dist"].describe()
    pos = B[B["forecast"] > 0]
    out["active_by_dist_quintile"] = pos.groupby(pd.qcut(pos["dist"], 5)).agg(n=("ret1","size"), fwd20=("fwd20","mean"),
        hit=("fwd20", lambda s: (s > 0).mean()), coin_sd=("ret1","std"), alloc=("alloc","mean"), gross=("gross1","mean"))
    ab = pd.cut(pos["age"], [0, 5, 20, 60, 120, 10000])
    out["active_by_age"] = pos.groupby(ab).agg(n=("ret1","size"), fwd20=("fwd20","mean"),
        hit=("fwd20", lambda s: (s > 0).mean()), alloc=("alloc","mean"), gross=("gross1","mean"), coin_sd=("ret1","std"))
    B["mkt60"] = np.where(B["past60"] > 0, "up60", "down60")
    act = B[B["alloc"] > 1e-9]
    out["active_by_mkt60"] = act.groupby("mkt60").agg(n=("ret1","size"), gross=("gross1","mean"), coin=("ret1","mean"),
        alloc=("alloc","mean"), gross_sum=("gross1","sum"))
    out["worst_dd_episodes"] = D.describe()
    # trade size vs leverage: gross pnl of trades weighted by alloc not available; churn: trades per active run
    T["dur"] = T["duration_minutes"] / 1440
    out["short_trades_share"] = pd.Series({"share_le5d": (T["dur"] <= 5).mean(),
        "sum_gross_le5d": T.loc[T["dur"] <= 5, "profit_loss_percent"].sum(),
        "sum_gross_gt20d": T.loc[T["dur"] > 20, "profit_loss_percent"].sum(),
        "sum_comm_le5d": T.loc[T["dur"] <= 5, "total_commission"].sum(),
        "sum_comm_all": T["total_commission"].sum()})
    out["unit_sharpe_by_alloc_ann"] = pd.Series({
        "book_gross_ann": B["gross1"].mean() / B["gross1"].std() * np.sqrt(365),
        "hold_ann": B["ret1"].mean() / B["ret1"].std() * np.sqrt(365),
        "active_coin_ann": act["ret1"].mean() / act["ret1"].std() * np.sqrt(365)})
    return out

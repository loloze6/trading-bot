import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars, trades = data["bars"], data["trades"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["ret1"] = b["close"].pct_change().shift(-1)
            b["fwd20"] = b["close"].shift(-20)/b["close"]-1
            b["bookret1"] = b["postRebalance_total_value"].pct_change().shift(-1)
            b["mom20"] = b["close"]/b["close"].shift(20)-1
            d = b["debug_info.components.above_ma.last_history_value"]
            b["sma"] = b["close"]/(1+d/100)
            b["slope20"] = b["sma"]/b["sma"].shift(20)-1
            v = b["postRebalance_total_value"]
            b["dd"] = v/v.cummax()-1
            b["coin"]=c; b["win"]=w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["alloc"]=B["postRebalance_current_allocation"]
    B["active"]=B["alloc"]>0
    A = B[B.active].copy()
    A["slope"]=np.where(A["slope20"]>0,"sma_up","sma_down")
    A["mom"]=np.where(A["mom20"]>0,"up20","down20")
    A["fcb"]=pd.cut(A["forecast"],[0,5,12,20.01])
    out["active_by_slope"]=A.groupby("slope").agg(n=("ret1","size"),ret1=("ret1","mean"),book1=("bookret1","mean"),fwd20=("fwd20","mean"),hit20=("fwd20",lambda s:(s>0).mean()))
    out["active_by_slope_fc"]=A.groupby(["slope","fcb"],observed=True).agg(n=("ret1","size"),book1=("bookret1","mean"),fwd20=("fwd20","mean"))
    out["active_by_mom_fc"]=A.groupby(["mom","fcb"],observed=True).agg(n=("ret1","size"),book1=("bookret1","mean"),fwd20=("fwd20","mean"))
    # contribution sum
    out["book_sum_by_slope_mom"]=A.groupby(["slope","mom"]).agg(n=("ret1","size"),sum_book=("bookret1","sum"),mean_book=("bookret1","mean"))
    # drawdown per window: max dd book vs coin
    g = B.groupby(["coin","win"])
    dd = g.apply(lambda x: pd.Series({"book_mdd":x["dd"].min(),"coin_mdd":(x["close"]/x["close"].cummax()-1).min(),"book_ret":x["postRebalance_total_value"].iloc[-1]/x["postRebalance_total_value"].iloc[0]-1,"coin_ret":x["close"].iloc[-1]/x["close"].iloc[0]-1}))
    out["window_dd_summary"]=dd.describe()
    out["worst_dd_by_win"]=dd.groupby(level="win")[["book_mdd","coin_mdd","book_ret","coin_ret"]].mean().sort_values("book_mdd").head(8)
    # trades: entry slope
    T=pd.concat([t.assign(coin=c,win=w) for c in trades for w,t in trades[c].items()],ignore_index=True)
    T["days"]=T["duration_minutes"]/1440
    out["trade_entry_fc"]=T.assign(efb=pd.cut(T["entry_forecast"],[-0.01,2,5,10,20.01])).groupby("efb",observed=True).agg(n=("days","size"),days=("days","median"),gross=("profit_loss_percent","mean"),win=("profit_loss_percent",lambda s:(s>0).mean()))
    out["trades_per_coin_window"]=T.groupby(["coin","win"]).size().describe()
    return out

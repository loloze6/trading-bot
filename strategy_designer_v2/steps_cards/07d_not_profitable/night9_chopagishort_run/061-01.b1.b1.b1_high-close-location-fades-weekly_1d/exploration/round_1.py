def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # book daily returns: per window per day mean across coins
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    eq = (1+B["book"]).cumprod().values
    peak = np.maximum.accumulate(eq); dd_ = eq/peak-1
    B["dd"] = dd_
    out["book by window"] = B.groupby("wn").agg(n=("book","size"), book_sum=("book","sum"), hold_sum=("hold","sum"), worst_dd=("dd","min"))
    # deepest fall
    i_min = int(np.argmin(dd_)); i_peak = int(np.argmax(eq[:i_min+1]))
    out["deepest fall"] = pd.Series({"depth": dd_[i_min], "days": i_min - i_peak, "win_peak": B["wn"].iloc[i_peak], "win_trough": B["wn"].iloc[i_min]})
    # per-bar cases with features
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            rng = (b["high"]-b["low"])
            cl = (b["close"]-b["low"])/rng.replace(0,np.nan)
            r1 = b["close"].pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            f = pd.DataFrame({"coin":c,"w":w,"cl":cl,"r1":r1,
                              "r5p": b["close"]/b["close"].shift(5)-1,
                              "rngv": (rng/b["close"])/vol20,
                              "r1v": r1/vol20,
                              "fwd5": b["close"].shift(-5)/b["close"]-1,
                              "regime": b["regime"], "alloc": b["postRebalance_current_allocation"],
                              "prev": b["previous_allocation"], "pos": np.arange(len(b))})
            feats.append(f)
    F = pd.concat(ignore_index=True, objs=feats)
    drift = F[F["pos"]%5==0].groupby("coin")["fwd5"].mean()
    F["un"] = -(F["fwd5"] - F["coin"].map(drift))
    F["tot"] = -F["fwd5"]
    out["regime counts"] = F["regime"].value_counts()
    sig = F[(F["regime"]=="mean_reversion")].dropna(subset=["fwd5"])
    nos = F[(F["regime"]=="unknown")].dropna(subset=["fwd5"])
    def summ(g):
        return pd.Series({"n":len(g),"mean_un":g["un"].mean(),"mean_tot":g["tot"].mean(),"t":g["un"].mean()/(g["un"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan, "hit":(g["tot"]>0).mean()})
    out["signal vs inprofile-no-signal (short side)"] = pd.DataFrame({"signal":summ(sig),"inprof_nosig":summ(nos)})
    sig = sig.copy()
    sig["r1v_q"] = pd.qcut(sig["r1v"], 4, labels=False, duplicates="drop")
    out["signal by day return/vol quartile"] = sig.groupby("r1v_q").apply(summ)
    sig["r5p_q"] = pd.qcut(sig["r5p"], 4, labels=False, duplicates="drop")
    out["signal by prior 5d return quartile"] = sig.groupby("r5p_q").apply(summ)
    sig["rng_q"] = pd.qcut(sig["rngv"], 4, labels=False, duplicates="drop")
    out["signal by range/vol quartile"] = sig.groupby("rng_q").apply(summ)
    out["signal by window"] = sig.assign(wn=sig["w"].str[1:].astype(int)).groupby("wn").apply(summ)
    out["signal by coin"] = sig.groupby("coin").apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c in trades for w, t in trades[c].items() if len(t)], ignore_index=True)
    out["trades summary"] = pd.Series({"n":len(T),"mean_net":T["net_profit_loss_percent"].mean(),"mean_gross":T["profit_loss_percent"].mean(),
                                       "median_net":T["net_profit_loss_percent"].median(),"worst":T["net_profit_loss_percent"].min(),
                                       "best":T["net_profit_loss_percent"].max(),"mean_days":(T["duration_minutes"]/1440).mean(),
                                       "share_loss":(T["net_profit_loss_percent"]<0).mean(),
                                       "worst10_sum":T["net_profit_loss_percent"].nsmallest(10).sum(),"total_sum":T["net_profit_loss_percent"].sum()})
    T["dur_d"] = (T["duration_minutes"]/1440).round()
    out["trades by duration"] = T.groupby(pd.cut(T["dur_d"],[0,4,5,6,8,15,100])).agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"))
    # alloc size on signal bars
    out["alloc on held bars"] = F.loc[F["alloc"]<0,"alloc"].describe()
    return out

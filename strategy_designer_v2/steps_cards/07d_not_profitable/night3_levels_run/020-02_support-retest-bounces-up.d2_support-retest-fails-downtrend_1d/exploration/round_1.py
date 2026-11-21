def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    br, cr, pos_mkt = [], [], []
    coin_mean = {}
    for c in data["days"]:
        allr = pd.concat([d["coin_return"] for d in data["days"][c].values()]).dropna()
        coin_mean[c] = allr.mean()
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            d = d.copy(); d["coin"] = c; d["w"] = w
            rows.append(d)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return","mean"), coin=("coin_return","mean"))
    out["book_by_year"] = D.groupby("year").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","count"))
    # cases on active bars, grid 5
    cs = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            alloc = b["postRebalance_current_allocation"].values
            for i in range(0, n-5, 5):
                f = b["forecast"].iloc[i]
                r = cl[i+5]/cl[i]-1
                cs.append(dict(coin=c, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                               active=(f<0), f=f, r=r,
                               r90=b.get("debug_info.components.fall90.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                               touch=b.get("debug_info.components.touch_s.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                               short=alloc[i]<0,
                               ret20=(cl[i]/cl[i-20]-1) if i>=20 else np.nan,
                               ret5=(cl[i]/cl[i-5]-1) if i>=5 else np.nan))
    C = pd.DataFrame(cs)
    C["ex"] = C["r"] - C["coin"].map(lambda c: C.loc[C.coin==c,"r"].mean())
    def summ(g):
        return pd.Series(dict(n=len(g), r=g["r"].mean(), ex=g["ex"].mean(), t=stats.ttest_1samp(g["r"],0).statistic if len(g)>2 else np.nan))
    A = C[C.active]
    out["active_vs_not"] = C.groupby("active").apply(summ)
    A = A.copy()
    A["q90"] = pd.qcut(A["r90"], 4, labels=False, duplicates="drop")
    out["active_by_r90_quart"] = A.groupby("q90").apply(summ).join(A.groupby("q90")["r90"].mean())
    A["qt"] = pd.qcut(A["touch"].rank(method="first"), 4, labels=False)
    out["active_by_touch_quart"] = A.groupby("qt").apply(summ).join(A.groupby("qt")["touch"].mean())
    out["active_by_year"] = A.groupby("year").apply(summ)
    A["q20"] = pd.qcut(A["ret20"], 4, labels=False, duplicates="drop")
    out["active_by_ret20_quart"] = A.groupby("q20").apply(summ).join(A.groupby("q20")["ret20"].mean())
    # all bars: 5-day fall graded, unconditional
    C["q5"] = pd.qcut(C["ret5"], 5, labels=False, duplicates="drop")
    out["all_by_ret5_quint"] = C.groupby(["q5","active"]).apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent","count"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur_h=("duration_minutes", lambda x: x.mean()/60))
    return out

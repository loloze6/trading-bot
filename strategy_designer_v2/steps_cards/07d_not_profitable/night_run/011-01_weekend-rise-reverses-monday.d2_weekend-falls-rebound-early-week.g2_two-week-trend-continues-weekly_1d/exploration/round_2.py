def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            last = b.groupby("day").last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.merge(last[["postRebalance_current_allocation"]], left_on="day", right_index=True, how="left")
            dd["pos_prev"] = dd["postRebalance_current_allocation"].shift(1)
            r = dd["coin_return"]
            dd["vol20_prev"] = r.rolling(20).std().shift(1)
            dd["ret60_prev"] = (dd["close"]/dd["close"].shift(60)-1).shift(1)
            dd["ret30_prev"] = (dd["close"]/dd["close"].shift(30)-1).shift(1)
            dd["coin"] = c; dd["window"] = w
            dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows, ignore_index=True)
    D["side"] = np.sign(D["pos_prev"])
    # coin mean daily return over all windows
    cm = D.groupby("coin")["coin_return"].mean()
    D["market_part"] = D["pos_prev"]*D["coin"].map(cm)
    D["timing"] = D["book_return"] - D["market_part"]
    x = D.dropna(subset=["book_return","pos_prev"])
    out["side_decomp"] = x.groupby("side").agg(mean=("book_return","mean"), market=("market_part","mean"), timing=("timing","mean"), n=("book_return","size"), abspos=("pos_prev", lambda s: s.abs().mean()))
    # book falls: daily book series, find deepest drawdown episodes
    book = x.groupby(["wn","day"]).agg(br=("book_return","mean")).reset_index().sort_values(["wn","day"])
    eq = (1+book["br"]).cumprod(); book["dd"] = (eq/eq.cummax()-1).values
    book["in_dd"] = book["dd"] < -0.15
    # contribution of short and long legs to book returns in deep-drawdown days vs others
    x2 = x.merge(book[["wn","day","dd","in_dd"]], on=["wn","day"])
    x2["long_c"] = np.where(x2["side"]>0, x2["book_return"], 0)
    x2["short_c"] = np.where(x2["side"]<0, x2["book_return"], 0)
    g = x2.groupby(["wn","day"]).agg(long_c=("long_c","mean"), short_c=("short_c","mean"), shortshare=("side", lambda s:(s<0).mean()), in_dd=("in_dd","first"))
    out["legs_by_dd_state"] = g.groupby("in_dd")[["long_c","short_c","shortshare"]].mean()
    # sum of each leg's daily contributions over losing days of the book (falls)
    gl = g.copy(); gl["tot"]=gl.long_c+gl.short_c
    out["legs_on_book_loss_days"] = pd.Series({"long_sum_on_loss_days": gl.loc[gl.tot<0,"long_c"].sum(), "short_sum_on_loss_days": gl.loc[gl.tot<0,"short_c"].sum(),
        "long_sum_all": gl.long_c.sum(), "short_sum_all": gl.short_c.sum()})
    # short leg by coin's 60-day return (the slow trend) and by 30-day
    s = x[x.side<0].dropna(subset=["ret60_prev"]).copy()
    s["r60q"] = pd.qcut(s["ret60_prev"],5)
    out["short_by_ret60"] = s.groupby("r60q").agg(mean=("book_return","mean"), timing=("timing","mean"), n=("book_return","size"))
    l = x[x.side>0].dropna(subset=["ret60_prev"]).copy()
    l["r60q"] = pd.qcut(l["ret60_prev"],5)
    out["long_by_ret60"] = l.groupby("r60q").agg(mean=("book_return","mean"), timing=("timing","mean"), n=("book_return","size"))
    # short leg by coin
    out["side_by_coin"] = x.groupby(["coin","side"])["book_return"].mean().unstack()
    # t of short leg mean
    sv = x.loc[x.side<0,"book_return"]
    out["short_t"] = float(sv.mean()/(sv.std()/np.sqrt(len(sv))))
    # simulate long-only book (shorts set to zero) daily: max dd & yearly
    x3 = x.copy(); x3["lo"] = np.where(x3.side>0, x3.book_return, 0.0)
    b2 = x3.groupby(["wn","day"])["lo"].mean().reset_index().sort_values(["wn","day"])
    e2 = (1+b2["lo"]).cumprod()
    out["long_only_approx"] = pd.Series({"mean":b2.lo.mean(),"sharpe":b2.lo.mean()/b2.lo.std()*np.sqrt(365),"maxdd":(e2/e2.cummax()-1).min(),"yearly":e2.iloc[-1]**(365/len(b2))-1})
    # short kept only when ret60 < 0
    x3["cond"] = np.where((x3.side>0)|((x3.side<0)&(x3.ret60_prev<0)), x3.book_return, 0.0)
    b3 = x3.groupby(["wn","day"])["cond"].mean().reset_index().sort_values(["wn","day"])
    e3 = (1+b3["cond"]).cumprod()
    out["short_only_in_60d_down_approx"] = pd.Series({"mean":b3.cond.mean(),"sharpe":b3.cond.mean()/b3.cond.std()*np.sqrt(365),"maxdd":(e3/e3.cummax()-1).min(),"yearly":e3.iloc[-1]**(365/len(b3))-1})
    return out

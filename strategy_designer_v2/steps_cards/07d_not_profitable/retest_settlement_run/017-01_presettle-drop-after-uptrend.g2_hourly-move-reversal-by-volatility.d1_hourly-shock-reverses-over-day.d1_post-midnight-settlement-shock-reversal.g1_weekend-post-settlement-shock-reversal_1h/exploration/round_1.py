def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # book daily returns: mean across coins per (window, day)
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["wn","day"])
    v = (1+B["book_return"]).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["dd_by_window"] = B.groupby("wn").agg(n=("dd","size"), book_mean=("book_return","mean"),
        book_sum=("book_return","sum"), coin_sum=("coin_return","sum"), min_dd=("dd","min"))
    out["by_year"] = B.groupby("year").agg(n=("dd","size"), book_sum=("book_return","sum"),
        sd=("book_return","std"), coin_sum=("coin_return","sum"), min_dd=("dd","min"))
    # deepest drawdown episode
    i_trough = int(np.argmin(dd.values)); peak_val = v.values[:i_trough+1].max()
    i_peak = int(np.argmax(v.values[:i_trough+1]))
    out["deepest_dd"] = pd.Series({"depth": dd.values[i_trough], "days_peak_to_trough": i_trough-i_peak,
        "window_peak": B["wn"].iloc[i_peak], "window_trough": B["wn"].iloc[i_trough]})
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if len(t)==0: continue
            t = t.copy(); t["coin"]=c; t["w"]=w; T.append(t)
    T = pd.concat(T)
    T["absf"] = T["entry_forecast"].abs()
    T["fq"] = pd.qcut(T["absf"].rank(method="first"), 5, labels=False)
    g = lambda x: pd.Series({"n":len(x),"gross":x["profit_loss_percent"].mean(),"net":x["net_profit_loss_percent"].mean(),
        "net_t":x["net_profit_loss_percent"].mean()/(x["net_profit_loss_percent"].std()/np.sqrt(len(x))),
        "dur_h":x["duration_minutes"].mean()/60, "worst":x["net_profit_loss_percent"].min()})
    out["trades_side"] = T.groupby("side").apply(g)
    out["trades_coin"] = T.groupby("coin").apply(g)
    out["trades_absf_quint"] = T.groupby("fq").apply(g)
    # case-level: weekend 00:00 bars with features
    C = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            r1 = b["close"].pct_change()
            vol24 = r1.rolling(24).std()
            vol720 = r1.rolling(720, min_periods=200).std()
            ret24p = b["close"]/b["close"].shift(24)-1
            ret168p = b["close"]/b["close"].shift(168)-1
            fwd = b["close"].shift(-24)/b["close"]-1
            m = (ts.dt.hour==0)
            df = pd.DataFrame({"coin":c,"w":w,"wd":ts.dt.weekday,"year":ts.dt.year,"r1":r1,"vol24":vol24,
                "volratio":vol24/vol720,"z":r1/vol24,"ret24p":ret24p,"ret168p":ret168p,"fwd":fwd,
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})[m]
            C.append(df)
    C = pd.concat(C).dropna(subset=["fwd","z"])
    # non-overlap: 00:00 bars daily are 24 apart already
    mu = C.groupby("coin")["fwd"].transform("mean")
    C["ex"] = C["fwd"]-mu
    C["sig"] = -np.sign(C["z"])
    C["cap"] = C["sig"]*C["fwd"]
    W = C[C["wd"].isin([5,6])].copy()
    def s(x):
        return pd.Series({"n":len(x),"cap_mean":x["cap"].mean(),"t":x["cap"].mean()/(x["cap"].std()/np.sqrt(len(x))),
                          "cap_sd":x["cap"].std()})
    W["zq"] = pd.qcut(W["z"].abs().rank(method="first"),5,labels=False)
    out["wkend_by_absz_quint"] = W.groupby("zq").apply(s)
    W["vrq"] = pd.qcut(W["volratio"].rank(method="first"),4,labels=False)
    out["wkend_by_volratio_q"] = W.groupby("vrq").apply(s)
    W["with_trend24"] = np.sign(W["ret24p"])==W["sig"]
    out["wkend_fade_with_trend24"] = W.groupby("with_trend24").apply(s)
    W["with_trend168"] = np.sign(W["ret168p"])==W["sig"]
    out["wkend_fade_with_trend168"] = W.groupby("with_trend168").apply(s)
    out["wkend_side"] = W.groupby("sig").apply(s)
    out["wkend_year"] = W.groupby("year").apply(s)
    out["wkend_day"] = W.groupby("wd").apply(s)
    return out

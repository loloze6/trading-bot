def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])["book_return"].mean().dropna().reset_index().sort_values(["wn","day"])
    v = (1+B["book_return"]).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    out["book by window"] = B.groupby("wn")["book_return"].agg(["count","mean","std","min"]).assign(sum=B.groupby("wn")["book_return"].sum())
    imin = int(np.argmin(dd.values))
    peak = int(np.argmax(v.values[:imin+1]))
    out["deepest fall"] = pd.Series({"depth": dd.values[imin], "peak_w": B["wn"].iloc[peak], "trough_w": B["wn"].iloc[imin], "days": imin-peak})
    out["worst 10 days share of losses"] = pd.Series({"worst10_sum": B["book_return"].nsmallest(10).sum(), "all_neg_sum": B["book_return"][B["book_return"]<0].sum(), "total_sum": B["book_return"].sum()})
    # cases: bars with short allocation
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            b["r1"] = cl.pct_change()
            b["nxt"] = cl.shift(-1)/cl-1
            rng = (b["high"]-b["low"])/cl
            b["rngratio"] = (b["high"]-b["low"])/(b["high"]-b["low"]).rolling(20,min_periods=10).mean()
            b["loc"] = (cl-b["low"])/(b["high"]-b["low"])
            b["ret5"] = cl/cl.shift(5)-1
            b["ret20"] = cl/cl.shift(20)-1
            b["gap_hi20"] = cl/b["high"].rolling(20,min_periods=10).max()-1
            b["upstreak"] = (b["r1"]>0).astype(int).groupby(((b["r1"]<=0)).cumsum()).cumsum()
            b["coin"]=c; b["w"]=w
            s = b[b["postRebalance_current_allocation"]<-0.01].copy()
            s["alloc"] = s["postRebalance_current_allocation"]
            cs.append(s)
    S = pd.concat(cs).dropna(subset=["nxt"])
    S["pnl"] = -S["nxt"]
    S["bookc"] = S["pnl"]*(-S["alloc"])
    out["cases"] = pd.Series({"n":len(S),"mean_pnl":S["pnl"].mean(),"t":stats.ttest_1samp(S["pnl"],0)[0],"mean_alloc":S["alloc"].mean(),"worst":S["pnl"].min(),"share_pnl<-5%":(S["pnl"]<-0.05).mean()})
    def grp(col, q=4):
        g = pd.qcut(S[col], q, duplicates="drop")
        return S.groupby(g, observed=True).agg(n=("pnl","size"), mean=("pnl","mean"), med=("pnl","median"), loss_tail=("pnl", lambda x:(x<-0.05).mean()), bookc=("bookc","sum"))
    for col in ["r1","rngratio","loc","ret5","ret20","gap_hi20","alloc"]:
        out["by "+col] = grp(col)
    out["by upstreak"] = S.groupby(S["upstreak"].clip(upper=3)).agg(n=("pnl","size"), mean=("pnl","mean"), loss_tail=("pnl", lambda x:(x<-0.05).mean()))
    out["by coin"] = S.groupby("coin").agg(n=("pnl","size"), mean=("pnl","mean"), bookc=("bookc","sum"))
    out["by weekday"] = S.groupby(pd.to_datetime(S["timestamp"]).dt.weekday).agg(n=("pnl","size"), mean=("pnl","mean"))
    # worst 15 cases features
    out["worst 15 features"] = S.nsmallest(15,"pnl")[["coin","w","r1","rngratio","loc","ret5","ret20","gap_hi20","alloc","pnl"]].reset_index(drop=True)
    return out

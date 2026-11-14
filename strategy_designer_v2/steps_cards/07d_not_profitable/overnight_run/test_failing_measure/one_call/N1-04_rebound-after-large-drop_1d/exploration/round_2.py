import pandas as pd, numpy as np

def explore(data):
    out = {}
    B = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["r"] = b.close.pct_change()
            b["fwd"] = b.close.shift(-1) / b.close - 1
            b["sma50"] = b.close / b.close.rolling(50).mean() - 1
            b["r5"] = b.close.shift(1) / b.close.shift(6) - 1
            b["vol20"] = b.r.abs().rolling(20).mean()
            b["alloc"] = b.postRebalance_current_allocation
            b["coin"] = c; b["w"] = w
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            B.append(b[["coin","w","day","r","fwd","sma50","r5","vol20","forecast","alloc"]])
    B = pd.concat(B)
    B["vrel"] = B.vol20 / B.groupby("coin").vol20.transform("median")
    cm = B.groupby("coin").fwd.mean()
    B["ex"] = B.fwd - B.coin.map(cm)
    A = B[(B.forecast > 0) & B.fwd.notna()].copy()
    out["alloc_desc_active"] = A.alloc.abs().describe().round(4)
    out["alloc_by_fbin"] = A.groupby(pd.cut(A.forecast,[0,5,12,16,20.01])).alloc.mean().round(4)
    # book-level daily return contributions: pnl = alloc*fwd per coin / ncoins
    A["pnl"] = A.alloc * A.fwd
    big = A[A.forecast >= 16]
    out["big_by_sma50"] = big.groupby(pd.cut(big.sma50,[-9,-0.2,-0.1,0,0.1,9])).agg(n=("ex","size"),hit=("fwd",lambda x:(x>0).mean()),mean_ex=("ex","mean"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))),q05=("fwd",lambda x:x.quantile(0.05)),pnl_sum=("pnl","sum")).round(4)
    big2 = big.copy()
    big2["vlow"] = big2.vrel < 1
    out["big_by_vlow"] = big2.groupby("vlow").agg(n=("ex","size"),hit=("fwd",lambda x:(x>0).mean()),mean_ex=("ex","mean"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))),q05=("fwd",lambda x:x.quantile(0.05)),pnl_sum=("pnl","sum")).round(4)
    # small positions (0,16): contribution
    sm = A[A.forecast < 16]
    out["small_vs_big_pnl"] = pd.Series({"small_pnl_sum": sm.pnl.sum(), "small_pnl_q05": sm.pnl.quantile(0.05), "big_pnl_sum": big.pnl.sum(), "big_pnl_q05": big.pnl.quantile(0.05), "small_n": len(sm), "big_n": len(big)}).round(4)
    # book drawdown episodes
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["w"]=w; rows.append(t)
    D = pd.concat(rows); D["day"]=pd.to_datetime(D["day"])
    book = D.groupby(["w","day"]).agg(br=("book_return","mean")).reset_index().dropna().sort_values(["w","day"])
    book["eq"] = book.groupby("w").br.transform(lambda x:(1+x).cumprod())
    book["dd"] = book.eq / book.groupby("w").eq.cummax() - 1
    indd = book[book.dd < -0.15][["w","day"]]
    # bars held during deep drawdown days (alloc of previous bar producing that day)
    A["nextday"] = A.day + pd.Timedelta(days=1)
    M = A.merge(indd.rename(columns={"day":"nextday"}), on=["w","nextday"])
    out["deep_dd_days_n"] = len(indd)
    out["held_in_dd"] = pd.Series({"n": len(M), "share_big": (M.forecast>=16).mean(), "share_big_all": (A.forecast>=16).mean(), "hit": (M.fwd>0).mean(), "mean_fwd": M.fwd.mean(), "share_sma50_lt_m01": (M.sma50<-0.1).mean(), "share_sma50_lt_m01_all": (A.sma50<-0.1).mean(), "mean_vrel": M.vrel.mean(), "mean_vrel_all": A.vrel.mean(), "share_r5_neg": (M.r5<0).mean(), "share_r5_neg_all": (A.r5<0).mean()}).round(4)
    # streak: big drop after a big drop within last 3 bars
    B = B.sort_values(["coin","w","day"])
    B["bigprev3"] = B.groupby(["coin","w"]).forecast.transform(lambda x:(x.shift(1)>=16).rolling(3,min_periods=1).max())
    big3 = B[(B.forecast>=16)&B.fwd.notna()]
    out["big_after_recent_big"] = big3.groupby("bigprev3").agg(n=("ex","size"),hit=("fwd",lambda x:(x>0).mean()),mean_ex=("ex","mean"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))),q05=("fwd",lambda x:x.quantile(0.05))).round(4)
    return out

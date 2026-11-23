def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    wins = [f"w{i}" for i in range(1,25)]
    coins = list(data["days"].keys())
    # book daily
    recs=[]
    for c in coins:
        for w,d in data["days"][c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=c; recs.append(dd)
    D=pd.concat(recs)
    B=D.groupby(["w","day"]).agg(book=("book_return","mean"),hold=("coin_return","mean")).reset_index()
    B["wn"]=B.w.str[1:].astype(int); B=B.sort_values(["wn","day"]).dropna()
    B["eq"]=(1+B.book).cumprod(); B["peak"]=B.eq.cummax(); B["dd"]=B.eq/B.peak-1
    B["heq"]=(1+B.hold).cumprod(); B["hdd"]=B.heq/B.heq.cummax()-1
    out["book_maxdd"]=float(B.dd.min()); out["hold_maxdd"]=float(B.hdd.min())
    out["book_sharpe"]=float(B.book.mean()/B.book.std()*np.sqrt(365)); out["hold_sharpe"]=float(B.hold.mean()/B.hold.std()*np.sqrt(365))
    out["corr_book_hold"]=float(B.book.corr(B.hold))
    beta=np.polyfit(B.hold,B.book,1); out["beta_book_on_hold"]=float(beta[0]); out["alpha_daily"]=float(beta[1])
    # drawdown by window: min dd within window and window return
    g=B.groupby("wn").agg(book_ret=("book",lambda x:(1+x).prod()-1),hold_ret=("hold",lambda x:(1+x).prod()-1),dd_end=("dd","last"),dd_min=("dd","min"))
    out["by_window"]=g.round(3)
    # bar-level per coin
    rows=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.copy()
            r=b.close.pct_change()
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["vol20"]=r.rolling(20).std()
            b["ret20"]=b.close/b.close.shift(20)-1
            b["ret5"]=b.close/b.close.shift(5)-1
            rng=(b.high-b.low).replace(0,np.nan)
            b["loc"]=(b.high-b.close)/rng
            b["alloc"]=b.postRebalance_current_allocation
            b["pos_gain"]=b.alloc*b.nxt
            b["coin"]=c;b["w"]=w
            rows.append(b[["coin","w","nxt","vol20","ret20","ret5","loc","forecast","alloc","pos_gain"]])
    X=pd.concat(rows).dropna()
    mu=X.groupby("coin").nxt.mean(); X["ex"]=X.nxt-X.coin.map(mu)
    out["mean_alloc"]=float(X.alloc.mean()); out["share_alloc_gt1"]=float((X.alloc>1).mean())
    # trend regime
    X["trend"]=np.where(X.ret20>0,"up20","down20")
    X["lowhalf"]=X["loc"]>0.5
    X["vhi"]=X.groupby("coin").vol20.transform(lambda s:s>s.median())
    def summ(s):
        return pd.Series({"n":len(s),"mean_nxt":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out["nxt_by_trend_lowhalf_vhi"]=X.groupby(["trend","vhi","lowhalf"]).nxt.apply(summ).unstack().round(5)
    out["posgain_by_trend_vhi"]=X.groupby(["trend","vhi"]).agg(n=("nxt","size"),alloc=("alloc","mean"),posgain=("pos_gain","mean"),nxt=("nxt","mean")).round(5)
    # slope by trend
    res={}
    for tr,s in X.groupby("trend"):
        sl=stats.linregress(s.forecast,s.ex); res[tr]=[sl.slope,sl.slope/sl.stderr,len(s)]
    out["slope_ex_on_forecast_by_trend"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # forecast quintile
    X["fq"]=pd.qcut(X.forecast,5,labels=False,duplicates="drop")
    out["by_forecast_q"]=X.groupby("fq").agg(n=("nxt","size"),f=("forecast","mean"),alloc=("alloc","mean"),nxt=("nxt","mean"),posgain=("pos_gain","mean")).round(5)
    # worst book days: what coins showed
    worst=B.nsmallest(int(len(B)*0.05),"book")[["wn","day"]]
    X2=X.copy()
    return out

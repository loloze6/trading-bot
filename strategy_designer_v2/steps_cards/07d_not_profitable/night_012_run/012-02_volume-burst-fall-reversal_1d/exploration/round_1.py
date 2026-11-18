def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns: mean across coins each day per window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    wn = {w:int(w[1:]) for w in D.w.unique()}
    D["wi"]=D.w.map(wn)
    B = D.groupby(["wi","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    out["book_summary"] = pd.Series({"mean_book":B.book_return.mean(),"mean_hold":B.coin_return.mean(),
        "share_days_book_nonzero":(B.book_return.abs()>1e-9).mean(),"n_days":len(B)})
    eq=(1+B.book_return).cumprod(); dd=eq/eq.cummax()-1
    out["maxdd"]=dd.min()
    # per window book return and hold
    pw = B.groupby(level=0).agg(book=("book_return",lambda x:(1+x).prod()-1),hold=("coin_return",lambda x:(1+x).prod()-1))
    out["per_window"]=pw.round(3)
    # bar-level analysis
    recs=[]
    for c, ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b.close; r=cl.pct_change()
            pos=b.postRebalance_current_allocation.fillna(0)
            nxt=cl.shift(-1)/cl-1
            f3=cl.shift(-3)/cl-1
            r10=cl/cl.shift(10)-1
            r30=cl/cl.shift(30)-1
            vol20=r.rolling(20).std()
            vr=b.volume/b.volume.rolling(30).mean()
            wick=(b[["open","close"]].min(axis=1)-b.low)/(b.high-b.low)
            fee=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            recs.append(pd.DataFrame({"coin":c,"w":w,"i":np.arange(len(b)),"fc":b.forecast,"pos":pos,"gain":pos*nxt,
               "nxt":nxt,"f3":f3,"r":r,"r10":r10,"r30":r30,"vol20":vol20,"vr":vr,"wick":wick,"fee":fee,"pr":b.previous_allocation.fillna(0)}))
    X=pd.concat(recs)
    out["exposure"]=pd.Series({"share_bars_pos>0":(X.pos>0).mean(),"mean_pos_when_in":X.pos[X.pos>0].mean(),
        "share_fc>0":(X.fc>0).mean(),"total_gain_sum":X.gain.sum(),"total_fee_sum":X.fee.sum()})
    # holding length: how many bars position stays after forecast>0
    X["in"]=X.pos>0.01
    # gain by bars since signal
    def since(g):
        s=[];k=999
        for f in g.fc.values:
            k=0 if f>0 else k+1; s.append(k)
        return pd.Series(s,index=g.index)
    X["since"]=X.groupby(["coin","w"],group_keys=False).apply(since)
    sx=X[X["in"]].copy(); sx["sinceb"]=sx.since.clip(upper=10)
    out["gain_by_bars_since_signal"]=sx.groupby("sinceb").agg(n=("gain","size"),mean_gain=("gain","mean"),mean_nxt=("nxt","mean"),mean_pos=("pos","mean"))
    # signal bars: forward 3 by prior 30d return quintile
    s=X[X.fc>0].dropna(subset=["r30","f3"]).copy()
    s["q30"]=pd.qcut(s.r30,5,labels=False)
    out["sig_f3_by_r30q"]=s.groupby("q30").agg(n=("f3","size"),r30=("r30","mean"),f3=("f3","mean"),nxt=("nxt","mean"))
    s["q10"]=pd.qcut(s.r10,5,labels=False)
    out["sig_f3_by_r10q"]=s.groupby("q10").agg(n=("f3","size"),r10=("r10","mean"),f3=("f3","mean"))
    s["qf"]=pd.qcut(s.fc.rank(method="first"),5,labels=False)
    out["sig_f3_by_fcq"]=s.groupby("qf").agg(n=("f3","size"),fc=("fc","mean"),f3=("f3","mean"),vr=("vr","mean"))
    # gain by r30 of position bars
    sx=X[X["in"]].dropna(subset=["r30"]).copy()
    sx["q30"]=pd.qcut(sx.r30,5,labels=False)
    out["pos_gain_by_r30q"]=sx.groupby("q30").agg(n=("gain","size"),r30=("r30","mean"),gain=("gain","mean"),nxt=("nxt","mean"))
    out["coin_mean_daily"]=X.groupby("coin").nxt.mean()
    out["gain_by_coin"]=X[X["in"]].groupby("coin").agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean"))
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=pd.Series({"n":len(T),"mean_pl":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),
        "med_dur_days":T.duration_minutes.median()/1440,"mean_comm":T.total_commission.mean()})
    return out

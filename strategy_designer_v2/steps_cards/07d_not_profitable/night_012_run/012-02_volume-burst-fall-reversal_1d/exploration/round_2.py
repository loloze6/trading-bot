def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy().reset_index(drop=True)
            dd["coin"]=c; dd["wi"]=int(w[1:])
            rows.append(dd)
    D = pd.concat(rows, ignore_index=True)
    B = D.groupby(["wi","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    out["book_summary"] = pd.Series({"mean_book":B.book_return.mean(),"mean_hold":B.coin_return.mean(),
        "share_days_book_nonzero":(B.book_return.abs()>1e-9).mean(),"n_days":len(B),
        "book_std":B.book_return.std()})
    eq=(1+B.book_return.values).cumprod(); ddn=eq/np.maximum.accumulate(eq)-1
    out["maxdd"]=float(ddn.min())
    Bw=B.reset_index(); Bw["dd"]=ddn
    out["dd_by_window_min"]=Bw.groupby("wi").agg(book=("book_return",lambda x:(1+x).prod()-1),hold=("coin_return",lambda x:(1+x).prod()-1),min_dd=("dd","min")).round(3)
    recs=[]
    for c, ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b.close; r=cl.pct_change()
            pos=b.postRebalance_current_allocation.fillna(0)
            nxt=cl.shift(-1)/cl-1
            f3=cl.shift(-3)/cl-1
            fc=b.forecast.fillna(0)
            grp=(fc>0).cumsum()
            since=grp.groupby(grp).cumcount()
            since=since.where(grp>0, 999)
            fee=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            recs.append(pd.DataFrame({"coin":c,"wi":int(w[1:]),"fc":fc.values,"pos":pos.values,"gain":(pos*nxt).values,
               "nxt":nxt.values,"f3":f3.values,"r":r.values,"r10":(cl/cl.shift(10)-1).values,"r30":(cl/cl.shift(30)-1).values,
               "vr":(b.volume/b.volume.rolling(30).mean()).values,
               "wick":((b[["open","close"]].min(axis=1)-b.low)/(b.high-b.low)).values,
               "fee":fee.values,"since":since.values,"mean_daily_coin":np.nan}))
    X=pd.concat(recs, ignore_index=True)
    cm=X.groupby("coin").nxt.mean(); X["cm"]=X.coin.map(cm)
    out["coin_mean_daily"]=cm
    X["inp"]=X.pos>0.01
    out["exposure"]=pd.Series({"share_bars_in":X.inp.mean(),"mean_pos_in":X.pos[X.inp].mean(),
        "share_fc>0":(X.fc>0).mean(),"mean_gain_all_bars":X.gain.mean(),"mean_fee_all_bars":X.fee.mean(),
        "market_part":(X.pos*X.cm).mean()})
    sx=X[X.inp].copy(); sx["sb"]=sx.since.clip(upper=10)
    out["gain_by_days_since_signal"]=sx.groupby("sb").agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean"),pos=("pos","mean"))
    s=X[X.fc>0].dropna(subset=["r30","f3"]).copy()
    s["q30"]=pd.qcut(s.r30,5,labels=False)
    out["sig_by_r30q"]=s.groupby("q30").agg(n=("f3","size"),r30=("r30","mean"),f3=("f3","mean"),nxt=("nxt","mean"))
    s["q10"]=pd.qcut(s.r10,5,labels=False)
    out["sig_by_r10q"]=s.groupby("q10").agg(n=("f3","size"),r10=("r10","mean"),f3=("f3","mean"),nxt=("nxt","mean"))
    s["qf"]=pd.qcut(s.fc.rank(method="first"),5,labels=False)
    out["sig_by_fcq"]=s.groupby("qf").agg(n=("f3","size"),fc=("fc","mean"),f3=("f3","mean"),nxt=("nxt","mean"),vr=("vr","mean"))
    s["qw"]=pd.qcut(s.wick.rank(method="first"),5,labels=False)
    out["sig_by_wickq"]=s.groupby("qw").agg(n=("f3","size"),wick=("wick","mean"),f3=("f3","mean"))
    p=X[X.inp].dropna(subset=["r30"]).copy(); p["q30"]=pd.qcut(p.r30,5,labels=False)
    out["posgain_by_r30q"]=p.groupby("q30").agg(n=("gain","size"),r30=("r30","mean"),gain=("gain","mean"),nxt=("nxt","mean"),pos=("pos","mean"))
    # worst book days: what was held
    X["bad"]=X.gain<X.gain[X.inp].quantile(0.05)
    bd=X[X.inp & X.bad]
    out["worst5pct_pos_bars"]=pd.Series({"n":len(bd),"mean_gain":bd.gain.mean(),"mean_since":bd.since.clip(upper=10).mean(),
        "mean_r30":bd.r30.mean(),"mean_r10":bd.r10.mean(),"share_r30_neg":(bd.r30<0).mean(),
        "all_in_mean_r30":X.r30[X.inp].mean(),"all_in_share_r30_neg":(X.r30[X.inp]<0).mean()})
    out["gain_by_coin"]=X[X.inp].groupby("coin").agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean"),fee=("fee","mean"))
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()], ignore_index=True)
    out["trades"]=pd.Series({"n":len(T),"mean_pl":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),
        "med_dur_days":T.duration_minutes.median()/1440,"mean_dur_days":T.duration_minutes.mean()/1440})
    T["db"]=pd.cut(T.duration_minutes/1440,[0,1.5,3.5,7.5,15,1e9])
    out["trades_by_dur"]=T.groupby("db").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"))
    return out

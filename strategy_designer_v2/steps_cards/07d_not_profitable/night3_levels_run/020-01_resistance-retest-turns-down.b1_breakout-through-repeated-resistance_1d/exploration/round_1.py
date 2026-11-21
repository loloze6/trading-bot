def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily series
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
        g["w"]=w; rows.append(g)
    B = pd.concat(rows).dropna(subset=["book"]).reset_index(drop=True)
    eq = (1+B["book"]).cumprod(); dd = eq/eq.cummax()-1
    B["dd"]=dd
    out["book_overall"] = pd.Series({"mean":B.book.mean(),"sharpe":B.book.mean()/B.book.std()*np.sqrt(365),
        "maxdd":dd.min(),"yearly":eq.iloc[-1]**(365/len(B))-1,"hold_maxdd":((1+B.hold.fillna(0)).cumprod()/(1+B.hold.fillna(0)).cumprod().cummax()-1).min()})
    # drawdown episodes
    ep=[]; peak_i=0; i=0; n=len(B)
    ce = eq.values; cm = eq.cummax().values
    in_dd=False
    for k in range(n):
        if ce[k] < cm[k] and not in_dd: in_dd=True; start=k-1 if k>0 else 0
        if in_dd and ce[k]>=cm[k]:
            seg=dd.iloc[start:k]; ep.append((start,int(seg.idxmin()),k,seg.min())); in_dd=False
    if in_dd:
        seg=dd.iloc[start:]; ep.append((start,int(seg.idxmin()),n,seg.min()))
    ep=sorted(ep,key=lambda x:x[3])[:6]
    er=[]
    for s,t,e,m in ep:
        seg=B.iloc[s:t+1]
        er.append({"depth":m,"days_to_trough":t-s,"windows":",".join(sorted(seg.w.unique(),key=lambda x:int(x[1:]))),
                   "year":str(pd.to_datetime(seg.day.iloc[0]).year),"book_sum":seg.book.sum(),"hold_sum":seg.hold.sum()})
    out["worst_falls"]=pd.DataFrame(er)
    # per year book vs hold
    B["year"]=pd.to_datetime(B.day).dt.year
    out["by_year"]=B.groupby("year").agg(book_mean=("book","mean"),hold_mean=("hold","mean"),n=("book","size"),book_min=("book","min"))
    # trades with entry features
    T=[]
    for c in coins:
        for w in trades[c]:
            tr=trades[c][w]; b=bars[c][w]
            if len(tr)==0: continue
            b=b.copy(); b["ts"]=pd.to_datetime(b.timestamp)
            b["r30"]=b.close/b.close.shift(30)-1
            b["r90"]=b.close/b.close.shift(90)-1
            b["vol20"]=np.log(b.close).diff().rolling(20).std()
            b["r1"]=b.close/b.close.shift(1)-1
            b["ma50"]=b.close/b.close.rolling(50).mean()-1
            for _,r in tr.iterrows():
                et=pd.to_datetime(r.entry_time)
                j=b.index[b.ts<=et]
                if len(j)==0: continue
                x=b.loc[j[-1]]
                T.append({"coin":c,"w":w,"net":r.net_profit_loss_percent,"r30":x.r30,"r90":x.r90,"vol20":x.vol20,"r1":x.r1,"ma50":x.ma50,"fc":r.entry_forecast,"alloc":abs(b.loc[j[-1],"postRebalance_current_allocation"]),"dur":r.duration_minutes/1440,"year":et.year})
    T=pd.DataFrame(T)
    out["trades_summary"]=pd.Series({"n":len(T),"mean_net":T.net.mean(),"median_net":T.net.median(),"share_pos":(T.net>0).mean(),"mean_dur_days":T.dur.mean(),"worst":T.net.min()})
    for f in ["r30","r90","vol20","r1","ma50","fc"]:
        q=pd.qcut(T[f],5,duplicates="drop")
        g=T.groupby(q,observed=True).net.agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g.index=[f"{f}_q{i+1}" for i in range(len(g))]
        out["net_by_"+f]=g
    out["net_by_coin"]=T.groupby("coin").net.agg(["mean","count"])
    out["net_by_year"]=T.groupby("year").net.agg(["mean","count"])
    return out

def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    # book chain
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().dropna().sort_index()
        g["win"]=w
        chain.append(g)
    ch = pd.concat(chain).reset_index(drop=True)
    v = (1+ch["book_return"]).cumprod(); dd = v/v.cummax()-1
    ch["dd"]=dd
    out["deepest_fall"]=float(dd.min())
    # windows with largest drawdown contributions
    pw = ch.groupby("win").agg(book=("book_return","sum"),coin=("coin_return","sum"),
                               min_dd=("dd","min"),n=("book_return","size"))
    pw["book_minus_coin"]=pw.book-pw.coin
    out["per_window"]=pw.reindex(wins).round(4)
    # per-coin worst falls
    rows=[]
    for c in coins:
        for w in wins:
            if w not in days[c]: continue
            r = days[c][w]["book_return"].dropna()
            vv=(1+r).cumprod(); rows.append((c,w,float((vv/vv.cummax()-1).min()),float(r.sum())))
    pc=pd.DataFrame(rows,columns=["coin","win","dd","sum"])
    out["coin_dd_summary"]=pc.groupby("coin").agg(worst=("dd","min"),mean_dd=("dd","mean"),total=("sum","sum")).round(4)
    # entry features
    rows=[]
    for c in coins:
        for w in wins:
            if w not in bars[c]: continue
            b=bars[c][w].reset_index(drop=True)
            cl=b["close"].values; a=b["postRebalance_current_allocation"].fillna(0).values
            pa=b["previous_allocation"].fillna(0).values
            lr=np.log(cl)
            ret1=pd.Series(cl).pct_change()
            vol20=ret1.rolling(20).std().values
            vol90=ret1.rolling(90,min_periods=40).std().values
            hi90=pd.Series(cl).rolling(90,min_periods=30).max().values
            raw=b["debug_info.components.res_break.last_history_value"].values
            for t in range(len(b)):
                if a[t]>0 and pa[t]<=0 and t+5<len(b):
                    r5=cl[t+5]/cl[t]-1
                    # path min over the hold
                    mn=cl[t+1:t+6].min()/cl[t]-1
                    rows.append(dict(coin=c,win=w,r5=r5,mn=mn,
                        ret1=cl[t]/cl[t-1]-1 if t>=1 else np.nan,
                        ret5=cl[t]/cl[t-5]-1 if t>=5 else np.nan,
                        ret20=cl[t]/cl[t-20]-1 if t>=20 else np.nan,
                        ret60=cl[t]/cl[t-60]-1 if t>=60 else np.nan,
                        volratio=vol20[t]/vol90[t] if vol90[t]>0 else np.nan,
                        vol20=vol20[t], dist_hi=cl[t]/hi90[t]-1, raw=raw[t], alloc=a[t]))
    e=pd.DataFrame(rows)
    out["n_entries"]=len(e)
    out["entries_r5"]=pd.Series({"mean":e.r5.mean(),"t":stats.ttest_1samp(e.r5,0).statistic,"share_neg":(e.r5<0).mean(),"mean_min_path":e.mn.mean()}).round(4)
    res={}
    for f in ["ret1","ret5","ret20","ret60","volratio","vol20","dist_hi","raw"]:
        s=e[[f,"r5","mn"]].dropna()
        q=pd.qcut(s[f].rank(method="first"),5,labels=False)
        gq=s.groupby(q).agg(x=(f,"median"),r5=("r5","mean"),mn=("mn","mean"),n=("r5","size"))
        for i,row in gq.iterrows():
            res[(f,int(i))]=row
    out["entry_quintiles"]=pd.DataFrame(res).T.round(4)
    out["by_coin"]=e.groupby("coin").agg(r5=("r5","mean"),n=("r5","size"),mn=("mn","mean")).round(4)
    return out

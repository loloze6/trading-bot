def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- pooled book daily returns per window
    wins = {}
    for c, ws in data["days"].items():
        for w, df in ws.items():
            d = df[["day","book_return","coin_return"]].copy(); d["coin"]=c
            wins.setdefault(w, []).append(d)
    # mean allocation per day per coin
    alloc = {}
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            t = pd.to_datetime(b["timestamp"])
            a = pd.DataFrame({"day": t.dt.floor("D"), "al": b["postRebalance_current_allocation"].values})
            alloc.setdefault(w, []).append(a.groupby("day")["al"].mean().rename(c))
    worder = sorted(wins.keys(), key=lambda x:int(x[1:]))
    rows=[]; chain=[]
    for w in worder:
        d = pd.concat(wins[w]); d["day"]=pd.to_datetime(d["day"])
        g = d.groupby("day")[["book_return","coin_return"]].mean().dropna()
        al = pd.concat(alloc[w],axis=1); al.index=pd.to_datetime(al.index)
        g["alloc"]=al.mean(axis=1).reindex(g.index).values
        g["win"]=w
        chain.append(g)
        rows.append({"win":w,"days":len(g),"book_sum":g.book_return.sum(),"hold_sum":g.coin_return.sum(),
                     "mean_alloc":g.alloc.mean(),"book_mdd":(lambda v:(v/v.cummax()-1).min())((1+g.book_return).cumprod())})
    out["per_window"]=pd.DataFrame(rows).set_index("win")
    ch = pd.concat(chain).reset_index(drop=True)
    v=(1+ch.book_return).cumprod(); dd=v/v.cummax()-1
    out["calmar_parts"]={"yearly":float(v.iloc[-1]**(365/len(v))-1),"mdd":float(dd.min())}
    # find top 3 drawdown episodes
    eps=[]; ddc=dd.copy()
    peak_idx = None
    i=0; n=len(dd)
    in_dd=False
    for k in range(n):
        if dd[k]<0 and not in_dd: start=k; in_dd=True
        if dd[k]==0 and in_dd:
            seg=dd[start:k]; eps.append((seg.min(),start,k)); in_dd=False
    if in_dd: eps.append((dd[start:].min(),start,n))
    eps=sorted(eps)[:5]
    er=[]
    for m,s,e in eps:
        trough=s+int(np.argmin(dd[s:e].values))
        seg=ch.iloc[s:trough+1]
        pre=ch.iloc[max(0,s-30):s]
        er.append({"depth":m,"days_to_trough":trough-s+1,"windows":",".join(sorted(seg.win.unique())),
                   "coin_ret_during":(1+seg.coin_return).prod()-1,"book_ret_during":(1+seg.book_return).prod()-1,
                   "alloc_during":seg.alloc.mean(),"coin_ret_30d_before":(1+pre.coin_return).prod()-1,
                   "alloc_before":pre.alloc.mean()})
    out["worst_falls"]=pd.DataFrame(er)
    # book by sign of coin day / by prior 30d trend
    ch["prior30"]=ch.groupby("win")["coin_return"].transform(lambda s:(1+s).rolling(30).apply(np.prod,raw=True).shift(1)-1)
    ch["q"]=pd.qcut(ch.prior30,4,labels=False)
    out["book_by_prior30_quartile"]=ch.groupby("q").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"),alloc=("alloc","mean"),book_sd=("book_return","std"))
    # ---- cases on bars
    H=18; recs=[]
    allr=[]
    for c, ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].values; r=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            idx=np.arange(0,len(cl)-H,H); allr.append(pd.Series(cl[idx+H]/cl[idx]-1).assign if False else pd.DataFrame({"c":c,"r":cl[idx+H]/cl[idx]-1}))
    allr=pd.concat(allr); drift=allr.groupby("c")["r"].mean(); usual=allr.groupby("c")["r"].std()
    for c, ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].values; f=b["forecast"].fillna(0).values; vol=b["volume"].values
            r=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            up=(r>0).astype(int); streak=np.zeros(len(cl),int)
            for k in range(1,len(cl)): streak[k]=streak[k-1]+1 if up[k] else 0
            p30=pd.Series(cl).pct_change(180).values
            p7=pd.Series(cl).pct_change(42).values
            vratio=(pd.Series(vol).rolling(3).mean()/pd.Series(vol).rolling(180).mean()).values
            rv=pd.Series(r).rolling(42).std()/pd.Series(r).rolling(360).std()
            lowf=pd.Series(f).cummin()
            nb=len(cl); last=-99; low=np.inf; taken=set()
            lowsince=0.0
            for k in range(nb):
                lowsince=min(lowsince,f[k])
                if f[k]-lowsince>=2 and k+H<nb:
                    cell=k//H
                    if cell not in taken:
                        taken.add(cell)
                        ret=cl[k+H]/cl[k]-1
                        recs.append({"c":c,"w":w,"f":f[k],"ret":ret,"unus":ret-drift[c],"str":(ret-drift[c])/usual[c],
                                     "streak":streak[k],"p30":p30[k],"p7":p7[k],"vr":vratio[k],"rv":rv.values[k],
                                     "dd1":cl[k+6]/cl[k]-1 if k+6<nb else np.nan})
                    lowsince=f[k]
    cs=pd.DataFrame(recs)
    out["cases_n"]=len(cs)
    def grp(col,qn=4):
        q=pd.qcut(cs[col],qn,labels=False,duplicates="drop")
        g=cs.groupby(q).agg(n=("unus","size"),lo=(col,"min"),hi=(col,"max"),unusual=("unus","mean"),total=("ret","mean"),
                             p10=("ret",lambda x:x.quantile(.1)))
        g["t"]=cs.groupby(q)["unus"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x)))
        return g
    for col in ["p30","p7","vr","rv","f"]:
        out["cases_by_"+col]=grp(col)
    out["cases_by_streak"]=cs.groupby(cs.streak.clip(0,6)).agg(n=("unus","size"),unusual=("unus","mean"),total=("ret","mean"))
    return out

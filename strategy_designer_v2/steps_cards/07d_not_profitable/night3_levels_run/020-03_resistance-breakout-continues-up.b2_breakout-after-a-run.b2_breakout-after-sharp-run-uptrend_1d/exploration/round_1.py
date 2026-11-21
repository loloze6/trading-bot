def explore(data):
    import pandas as pd, numpy as np
    days=data["days"]; bars=data["bars"]; trades=data["trades"]
    coins=list(days.keys())
    wins=sorted({w for c in coins for w in days[c].keys()}, key=lambda s:int(s[1:]))
    rows=[]
    for w in wins:
        frames=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        f=pd.concat(frames)
        g=f.groupby("day").agg(book=("book_return","mean"),hold=("coin_return","mean")).reset_index()
        g["w"]=w; rows.append(g)
    B=pd.concat(rows).dropna(subset=["book"]).reset_index(drop=True)
    eq=(1+B.book).cumprod(); dd=eq/eq.cummax()-1
    B["dd"]=dd.values
    eps=[]; i=0; n=len(B)
    while i<n:
        if dd.iloc[i]<0:
            j=i
            while j<n and dd.iloc[j]<0: j+=1
            seg=dd.iloc[i:j]; k=int(seg.idxmin())
            eps.append((float(seg.min()), B.w.iloc[i], B.w.iloc[j-1], i, k, j-i))
            i=j
        else: i+=1
    eps=sorted(eps)[:5]
    E=pd.DataFrame([{"depth":e[0],"w_start":e[1],"w_trough":B.w.iloc[e[4]],"w_end":e[2],"days_to_trough":e[4]-e[3],"len":e[5],
                     "hold_ret_to_trough":float((1+B.hold.iloc[e[3]:e[4]+1]).prod()-1),
                     "book_ret_to_trough":float((1+B.book.iloc[e[3]:e[4]+1]).prod()-1)} for e in eps])
    yrs=len(B)/365; ann=eq.iloc[-1]**(1/yrs)-1
    W=B.groupby("w",sort=False).agg(book=("book",lambda x:(1+x).prod()-1),hold=("hold",lambda x:(1+x).prod()-1),mindd=("dd","min"))
    tr=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].copy(); b["ts"]=pd.to_datetime(b.timestamp)
            cl=b.close
            b["r60"]=cl/cl.shift(60)-1; b["r10"]=cl/cl.shift(10)-1
            b["vol20"]=np.log(cl).diff().rolling(20).std()*np.sqrt(365)
            b["hi90"]=cl/cl.rolling(90,min_periods=20).max()-1
            b["r1"]=cl.pct_change()
            t=trades[c].get(w)
            if t is None or len(t)==0: continue
            t=t.copy(); t["et"]=pd.to_datetime(t.entry_time)
            m=pd.merge_asof(t.sort_values("et"),b[["ts","r60","r10","vol20","hi90","r1"]].sort_values("ts"),left_on="et",right_on="ts",direction="backward")
            m["coin"]=c; tr.append(m)
    T=pd.concat(tr)
    T=T[T.side=="LONG"]
    def grp(col,q=4):
        x=T.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],q,duplicates="drop")
        return x.groupby("q").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),
            med=("net_profit_loss_percent","median"),worst=("net_profit_loss_percent","min"),
            share_loss_gt10=("net_profit_loss_percent",lambda s:(s<-10).mean()),
            days=("duration_minutes",lambda s:s.mean()/1440))
    out={}
    out["episodes"]=E; out["ann"]=float(ann); out["maxdd"]=float(dd.min()); out["windows"]=W
    out["by_r10"]=grp("r10"); out["by_r60"]=grp("r60"); out["by_vol"]=grp("vol20"); out["by_r1"]=grp("r1"); out["by_hi90"]=grp("hi90")
    out["by_coin"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),worst=("net_profit_loss_percent","min"))
    out["ntr"]=len(T)
    return out

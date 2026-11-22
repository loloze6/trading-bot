def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # ---- book daily returns: per window, mean across coins per day
    recs = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            recs.append(dd)
    D = pd.concat(recs)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    def stats(r):
        eq=(1+r).cumprod(); dd=eq/eq.cummax()-1
        yr=eq.iloc[-1]**(365/len(r))-1
        return pd.Series({"mean":r.mean(),"sharpe":r.mean()/r.std()*np.sqrt(365),"yearly":yr,"maxdd":dd.min(),"calmar":yr/-dd.min()})
    out["book_vs_hold"]=pd.DataFrame({"book":stats(B.book_return),"hold":stats(B.coin_return)})
    # per window
    pw=B.groupby(level=0).agg(book=("book_return","sum"),hold=("coin_return","sum"))
    out["per_window_sum_returns"]=pw.round(4)
    # drawdown episodes of the book
    r=B.book_return.values; eq=np.cumprod(1+r); peak=np.maximum.accumulate(eq); dd=eq/peak-1
    # find top 5 episodes
    eps=[]; i=0; n=len(dd)
    while i<n:
        if dd[i]<0:
            j=i
            while j<n and dd[j]<0: j+=1
            k=i+np.argmin(dd[i:j]); eps.append((dd[k],i,k,j))
            i=j
        else: i+=1
    eps=sorted(eps)[:6]
    wnidx=B.index.get_level_values(0).values
    rows=[]
    hr=B.coin_return.values
    for depth,s,k,e in eps:
        rows.append({"depth":depth,"days_to_trough":k-s+1,"windows":f"w{wnidx[s]}-w{wnidx[k]}",
                     "book_sum":r[s:k+1].sum(),"hold_sum":hr[s:k+1].sum(),
                     "hold_prior30":hr[max(0,s-30):s].sum()})
    out["deepest_falls"]=pd.DataFrame(rows).round(4)
    # ---- trade level: P&L by entry characteristics
    T=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close; hi=b.high; lo=b.low
            ret6=cl.shift(-6)/cl-1
            past=cl/cl.shift(42)-1   # 7-day
            past30=cl/cl.shift(180)-1
            fall24=cl/cl.shift(6)-1
            rng24=hi.rolling(6).max()/lo.rolling(6).min()-1
            avg=rng24.rolling(180).mean()
            f=b.forecast
            alloc=b.postRebalance_current_allocation
            nxt=cl.shift(-1)/cl-1
            df=pd.DataFrame({"coin":c,"f":f,"ret6":ret6,"past7":past,"past30":past30,"fall24":fall24,
                             "rm":rng24/avg,"alloc":alloc,"gain":alloc*nxt,
                             "rise":(f-f.shift(1))})
            df=df.iloc[::6]
            T.append(df)
    T=pd.concat(T).dropna(subset=["ret6"])
    drift=T.groupby("coin").ret6.transform("mean")
    T["ex"]=T.ret6-drift
    A=T[T.f>0].copy()
    def grp(col,q=4):
        A["g"]=pd.qcut(A[col],q,labels=False,duplicates="drop")
        g=A.groupby("g").agg(n=("ex","size"),lo=(col,"min"),hi=(col,"max"),mean_ex=("ex","mean"),mean_ret=("ret6","mean"),sd=("ex","std"))
        g["t"]=g.mean_ex/(g.sd/np.sqrt(g.n)); return g.drop(columns="sd").round(5)
    out["active_by_forecast"]=grp("f")
    out["active_by_past30"]=grp("past30")
    out["active_by_past7"]=grp("past7")
    out["active_by_rangemult"]=grp("rm")
    # book bar gain: active vs not, by past30 sign, overall
    allb=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); cl=b.close
            allb.append(pd.DataFrame({"alloc":b.postRebalance_current_allocation,"nxt":cl.shift(-1)/cl-1,
                       "past30":cl/cl.shift(180)-1,"f":b.forecast}))
    AB=pd.concat(allb).dropna()
    AB["gain"]=AB.alloc*AB.nxt
    AB["state"]=np.where(AB.past30>0,"up30","down30")
    out["bar_gain_by_state"]=AB[AB.alloc.abs()>0].groupby("state").agg(n=("gain","size"),mean_gain=("gain","sum"),mean_alloc=("alloc","mean"),coin_mean=("nxt","mean"))
    out["share_time_in_market"]=float((AB.alloc.abs()>0).mean())
    return out

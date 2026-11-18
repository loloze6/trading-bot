def explore(data):
    import pandas as pd, numpy as np
    days=data["days"]; bars=data["bars"]
    coins=list(days.keys())
    # book daily returns: mean across coins per day within window
    rows=[]
    for c in coins:
        for w,d in days[c].items():
            t=d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["w"]=w; rows.append(t)
    D=pd.concat(rows)
    wn=lambda w:int(w[1:])
    B=D.groupby(["w","day"]).agg(book=("book_return","mean"),hold=("coin_return","mean")).reset_index()
    B["wn"]=B.w.map(wn); B=B.sort_values(["wn","day"]).dropna()
    eq=(1+B.book).cumprod(); dd=eq/eq.cummax()-1
    B["dd"]=dd.values
    perw=B.groupby("wn").agg(book=("book",lambda x:(1+x).prod()-1),hold=("hold",lambda x:(1+x).prod()-1),mindd=("dd","min"))
    # per coin contribution
    pc=D.groupby("coin").agg(book_mean=("book_return","mean"),coin_mean=("coin_return","mean"),book_sd=("book_return","std"))
    # grid analysis: condition on past 5-day return
    g=[]
    for c in coins:
        mu=[]
        for w,b in bars[c].items():
            cl=b.close.values; f=b.forecast.values; v=b.volume.values; al=b.postRebalance_current_allocation.values
            hi=b.high.values; lo=b.low.values
            for i in range(30,len(b)-3,3):
                g.append(dict(coin=c,w=w,f=f[i],fwd=cl[i+3]/cl[i]-1,r5=cl[i]/cl[i-5]-1,r30=cl[i]/cl[i-30]-1,
                    r1=cl[i]/cl[i-1]-1,pos=(cl[i]-lo[i-19:i+1].min())/(hi[i-19:i+1].max()-lo[i-19:i+1].min()+1e-12),al=al[i]))
    G=pd.DataFrame(g)
    G["ex"]=G.fwd-G.groupby("coin").fwd.transform("mean")
    A=G[G.f>0].copy()
    def tab(col,q=4):
        A["b"]=pd.qcut(A[col],q,labels=False,duplicates="drop")
        return A.groupby("b").agg(n=("ex","size"),lo=(col,"min"),hi=(col,"max"),ex=("ex","mean"),
            t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))),alloc=("al","mean"),pnl=("fwd",lambda x:np.nan))
    out={"per_window":perw,"per_coin":pc,"r5_quart":tab("r5"),"r1_quart":tab("r1"),"pos20_quart":tab("pos"),"r30_quart":tab("r30"),
         "f_quart":tab("f"),"zero_f":pd.Series({"n":(G.f==0).sum(),"ex":G[G.f==0].ex.mean()})}
    # worst 5% of book days: what held
    worst=B.nsmallest(20,"book")
    out["worst_days_mean"]=pd.Series({"book":worst.book.mean(),"hold":worst.hold.mean()})
    out["maxdd"]=dd.min()
    return out
